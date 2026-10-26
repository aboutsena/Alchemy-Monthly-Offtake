"""Calculate isolated scratch copies using the reviewed local formula model.

No Node, Codex installation, Excel automation, network or financial publication.
The formula evaluator is the SAME reviewed evaluator used by the planner. This
is not a second independent Excel calculation engine. Separate Decimal checks
validate transaction rows and totals. Unsupported formulas fail closed.
"""
from __future__ import annotations

import argparse
import copy
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import sys
import xml.etree.ElementTree as ET
import zipfile

sys.dont_write_bytecode = True


def require(condition, message):
    if not condition:
        raise ValueError(message)


def sha(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def decimal(value, label="number"):
    require(not isinstance(value, bool) and value is not None, "Invalid " + label)
    try:
        result = Decimal(str(value))
    except (InvalidOperation, ValueError, TypeError) as exc:
        raise ValueError("Invalid " + label) from exc
    require(result.is_finite(), "Non-finite " + label)
    return result


def close(actual, expected, label, tolerance="0.000001"):
    a, b = decimal(actual, label), decimal(expected, label)
    require(abs(a - b) <= Decimal(tolerance), "Calculation mismatch: " + label)


def value_matches(actual, expected):
    if actual in (None, "") or expected in (None, ""):
        return actual in (None, "") and expected in (None, "")
    if isinstance(actual, bool) or isinstance(expected, bool):
        return type(actual) is type(expected) and actual == expected
    if isinstance(actual, (int, float, Decimal)) and isinstance(expected, (int, float, Decimal)):
        return abs(decimal(actual) - decimal(expected)) <= Decimal("0.000001")
    return type(actual) is type(expected) and actual == expected


def engine_modules(engine):
    engine = Path(engine).resolve(strict=True)
    require(engine.is_dir(), "Engine directory is required")
    for directory in (engine, engine / "ingest"):
        if str(directory) not in sys.path:
            sys.path.insert(0, str(directory))
    path = engine / "monthly_workbooks.py"
    spec = importlib.util.spec_from_file_location("_portable_monthly_workbooks", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def independent_rows(job, source_values):
    """Validate actual edits against rows and Decimal arithmetic, not job caches."""
    month = job["month"]
    spec = next(s for s in job["sheets"] if s["name"] == month)
    edits = spec.get("edits", {})
    totals = {key: Decimal(0) for key in ("bottles", "inc_vat", "ex_vat", "rebate")}
    seen = set()
    expected_addresses = set()
    row_results = []
    for item in job.get("rows", []):
        row = item.get("row")
        require(type(row) is int and row not in seen, "Invalid or duplicate transaction row")
        seen.add(row)
        quantity = decimal(item.get("qty"), "bottle quantity")
        price = decimal(item.get("price_decimal", item.get("price")), "unit price")
        rate = decimal(item.get("rebate_rate"), "existing rebate")
        require(Decimal(0) <= rate <= Decimal(1), "Rebate must be an existing finite fraction")
        basis = item.get("price_basis")
        require(basis in {"ex_vat", "inc_vat"}, "VAT basis must be explicit")
        require(edits.get("J" + str(row)) == item.get("wholesaler"), "Wholesaler edit differs from row")
        close(edits.get("N" + str(row)), quantity, "bottle edit")
        selected, other = ("L", "K") if basis == "ex_vat" else ("K", "L")
        close(edits.get(selected + str(row)), price, "price edit")
        require(edits.get(other + str(row)) in (None, ""), "Only one price column is allowed")
        close(source_values.get("P" + str(row)), rate, "preserved rebate parameter")
        gross = quantity * price * (Decimal("1.07") if basis == "ex_vat" else Decimal(1))
        net = (gross / Decimal("1.07")).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        rebate = net * rate
        close(item.get("amount"), quantity * price, "reported line amount", "0.011")
        for key, calculated in (("expected_R", gross), ("expected_S", net), ("expected_T", rebate)):
            close(item.get(key), calculated, key, "0.0001")
        totals["bottles"] += quantity
        totals["inc_vat"] += gross
        totals["ex_vat"] += net
        totals["rebate"] += rebate
        expected_addresses.update(c + str(row) for c in "JKLN")
        row_results.append({"row": row, "R": gross, "S": net, "T": rebate, "N": quantity})
    metadata = set()
    for addition in spec.get("mapping_additions", []):
        for key in addition.get("metadata", {}):
            metadata.add(key if re.fullmatch(r"[A-Z]+\d+", key) else key + str(addition["row"]))
    require(set(edits) - metadata == expected_addresses, "Transaction edit set does not match rows")
    require(seen, "A scratch calculation requires at least one sale row")
    require(set(job.get("totals", {})) == set(totals), "Incomplete transaction totals")
    for key, calculated in totals.items():
        close(job["totals"][key], calculated, "total " + key, "0.011")
    return row_results, totals


def calculate_job(job, engine, staging):
    require(job.get("dry_run") is True, "Only isolated copy calculations are supported")
    require(re.fullmatch(r"job-\d{3,}", str(job.get("id", ""))), "Invalid job ID")
    require(re.fullmatch(r"20\d{2}-(?:0[1-9]|1[0-2])", str(job.get("period", ""))), "Invalid period")
    month = job["period"][-2:]
    require(job.get("month") == month, "Job month differs from period")
    source = Path(job["path"]).resolve(strict=True)
    require(source.is_file() and source.suffix.lower() == ".xlsx", "Input must be an XLSX file")
    require(job.get("output_name") == source.name and Path(job["output_name"]).name == source.name,
            "Scratch output must retain the source basename")
    require(sha(source) == job.get("sha256"), "Input hash changed")
    staging = Path(staging).resolve()
    inputs = source.parent
    require(not staging.is_relative_to(inputs) and not inputs.is_relative_to(staging),
            "Scratch output and workbook inputs must be separate")
    target, proof_path = staging / source.name, staging / (job["id"] + "-stage-manifest.json")
    require(not target.exists() and not proof_path.exists(), "Scratch output must be new")
    names = [s.get("name") for s in job.get("sheets", [])]
    require(len(names) == len(set(names)) and names.count(month) == 1, "Sheet specifications are not unique")
    for spec in job["sheets"]:
        require(not spec.get("parameter_overrides") and not spec.get("formula_overrides"),
                "Portable distribution never changes rebate parameters or original formulas")
        require(not spec.get("clear_cells"), "Clearing existing inputs is not supported")
        require(not (re.fullmatch(r"\d{2}", spec["name"]) and spec["name"] != month and
                     (spec.get("edits") or spec.get("cache_addresses"))), "Cannot change another month")

    workbooks = engine_modules(engine)
    from transaction_period import validate_record_period
    seen_occurrences = set()
    for row in job.get("rows", []):
        require(row.get("source_records"), "Missing source occurrence provenance")
        for record in row["source_records"]:
            occurrence = record.get("record_id")
            require(occurrence and occurrence not in seen_occurrences, "Missing or duplicate source occurrence")
            seen_occurrences.add(occurrence)
            require(validate_record_period(record, job["period"])["valid"],
                    "Source transaction period is not verified for this month")
    model_module, merger = workbooks.components(month)
    util, evaluator = model_module.c, model_module.d
    model = evaluator.Model(source)
    workbooks.load_current_month(model, month, util)
    month_spec = next(s for s in job["sheets"] if s["name"] == month)
    row_results, totals = independent_rows(job, model.values[month])
    with zipfile.ZipFile(source) as original:
        merger.W.update(original=original, current_item=job, month=month)
        merger.inspect_targets = workbooks.inspect_month_targets
        for spec in job["sheets"]:
            require(util.PRESERVE.sheet_part(original, spec["name"]) == spec["sheet_part"], "Wrong native sheet part")
            require(util.digest(original.read(spec["sheet_part"])) == spec["original_sheet_sha256"],
                    "Source sheet hash changed")
            native, _ = workbooks.namespace_view(original.read(spec["sheet_part"]))
            workbooks.inspect_month_targets(native, spec)
            for address, value in merger.all_edits(spec).items():
                model.change(spec["name"], address, value, "Portable current-month input")

        model_module.closure(model, model_module.candidates_for(model, month, set(month_spec["cache_addresses"])),
                             "Portable current-month formula calculation")
        for sheet, anchor, region, expression in model.arrays:
            if sheet == month or not expression or not evaluator.SEP.search(expression):
                continue
            # Expand only the already-reviewed exact same-size literal arrays.
            from openpyxl.utils.cell import range_boundaries, get_column_letter
            match = re.fullmatch("'" + month + r"'!(\$?[A-Z]+\$?\d+:\$?[A-Z]+\$?\d+)", expression)
            require(match is not None, "Unsupported dependent array")
            left, top, right, bottom = range_boundaries(region)
            sx, sy, ex, ey = range_boundaries(match[1])
            require((right-left, bottom-top) == (ex-sx, ey-sy), "Dependent array shape differs")
            # Only changed inputs/formulas can invalidate a saved array cache.
            # Walking every cell and rescanning all array anchors is quadratic.
            for address, value in list(model.modified[month].items()):
                ax, ay, _, _ = range_boundaries(address)
                if sx <= ax <= ex and sy <= ay <= ey:
                    target_address = get_column_letter(left+ax-sx) + str(top+ay-sy)
                    model.change(sheet, target_address, 0 if value in (None, "") else value,
                                 "Portable current-month array")
        candidates = [value for sheet in model.formulas if not re.fullmatch(r"\d{2}", sheet)
                      for value in model_module.candidates_for(model, sheet)]
        model_module.closure(model, candidates, "Portable transitive current-month formula")
        require(not model.mismatch, "Existing formula caches do not match the reviewed evaluator")

        computed = {}
        patches = {}
        for spec in job["sheets"]:
            name = spec["name"]
            values = {}
            for address in spec["cache_addresses"]:
                member = spec.get("array_cache_members", {}).get(address)
                expression = (member["formula"].lstrip("=") if member else model.formulas.get(name, {}).get(address))
                require(expression is not None, "Cache has no verified source formula: " + name + "!" + address)
                ast, _ = model.parse(name, address, expression)
                try:
                    calculated = model_module.formula_scalar(model, ast, True)
                except evaluator.ExcelFormulaError as exc:
                    require(spec.get("allowed_existing_errors", {}).get(address) == exc.code,
                            "Formula error: " + name + "!" + address)
                    calculated = exc.code
                calculated = evaluator.portable(calculated)
                require(value_matches(calculated, spec["expected_values"][address]),
                        "Recalculated cache differs from prepared plan: " + name + "!" + address)
                values[address] = calculated
            computed[name] = values
            native, restore = workbooks.namespace_view(original.read(spec["sheet_part"]))
            text, raw = merger.original_cells(native)
            changed = {}
            _, _, nodes, _ = util.sheet_data(original, name)
            xml = ET.fromstring(native)
            for address, value in merger.all_edits(spec).items():
                cell = raw.get(address)
                if cell is None:
                    style = merger.style_for(address, nodes, xml, spec.get("mapping_additions", []))
                    cell = '<c r="' + address + '"' + (' s="' + style + '"' if style is not None else '') + '/>'
                changed[address] = merger.set_input(cell, value)
            for address, value in values.items():
                changed[address] = util.patch_cell(raw[address], value,
                    array_member=address in spec.get("array_cache_members", {}),
                    cache_error=isinstance(value, str) and value.startswith("#"))
            text = util.CELL_RE.sub(lambda match: changed.get(match[1], match.group()), text)
            text = merger.add_missing_cells(text, {a: v for a, v in changed.items() if a not in raw})
            patches[spec["sheet_part"]] = restore(text.encode("utf-8"))
        for row in row_results:
            for column in "RST":
                close(computed[month][column + str(row["row"])], row[column], "independent row " + column, "0.0001")
        total_row = month_spec["layout"]["total_row"]
        for column, key in (("N", "bottles"), ("R", "inc_vat"), ("S", "ex_vat"), ("T", "rebate")):
            close(computed[month][column + str(total_row)], totals[key], "independent workbook total " + column, "0.011")
        require(sha(source) == job["sha256"], "Source changed during calculation")
        staging.mkdir(parents=True, exist_ok=True)
        with zipfile.ZipFile(target, "x") as output:
            output.comment = original.comment
            for info in original.infolist():
                output.writestr(copy.copy(info), patches.get(info.filename, original.read(info.filename)))
        with zipfile.ZipFile(target) as output:
            require(output.testzip() is None, "Scratch workbook CRC failed")
            for spec in job["sheets"]:
                merger.verify_values(output, spec)
            # This scratch already preserves native formulas, parameters and all
            # unrelated XML. The standard downstream merger audits them again.
            audit = merger.validate_package(original, output, job)
        require(sha(source) == job["sha256"], "Source changed after scratch verification")
    proof = {"id": job["id"], "result": "passed", "dry_run": True,
             "source_path": str(source), "source_sha256": job["sha256"],
             "path": str(target), "sha256": sha(target), "period": job["period"],
             "calculation_backend": "reviewed_python_formula_model",
             "independent_second_formula_engine": False,
             "fresh_formula_cache_checks": sum(len(v) for v in computed.values()),
             "independent_decimal_row_checks": len(row_results),
             "original_formulas_and_rebate_parameters_preserved": True,
             "native_package_audit": audit}
    with proof_path.open("x", encoding="utf-8") as stream:
        json.dump(proof, stream, ensure_ascii=False, indent=2)
        stream.write("\n")
    return proof


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--engine", required=True, help="Reviewed engine distributed with this program")
    parser.add_argument("plan")
    parser.add_argument("staging")
    parser.add_argument("job_id")
    args = parser.parse_args(argv)
    path = Path(args.plan).resolve(strict=True)
    require(path.stat().st_size <= 64 * 1024 * 1024, "Job plan exceeds the local size limit")
    plan = json.loads(path.read_text(encoding="utf-8-sig"))
    require(plan.get("dry_run") is True and plan.get("publishable") is False and len(plan.get("files", [])) == 1,
            "Exactly one non-publishable copy job is required")
    require(plan["files"][0].get("id") == args.job_id, "Wrong job ID")
    proof = calculate_job(plan["files"][0], args.engine, args.staging)
    print("Staged: " + proof["id"])
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print("Scratch calculation blocked: " + str(exc), file=sys.stderr)
        raise SystemExit(2)

# Monthly operating procedure

## 1. Record the request

Record the requested `YYYY-MM`, physical report folder, approved template manifest, destination folder and delivery mode: validation only, validated copies, or separately authorized original-file delivery. Use [the request contract](contracts/run-request.schema.json) as a record. It is not a CLI config, permission token or instruction to execute received files.

Verify the period inside the reports; the folder name alone is not evidence. Inventory and hash current inputs, protect the evidence and create a recoverable backup. Never mix real sources with test outputs or simulations.

## 2. Check the approved workbook base

The existing local implementation is under `Alchemy_AI_DEV/OFFTAKE_MVP`. `automation/template-base.json` records the approved Admin base, its manifest/hashes and last closed period. At this checkpoint that base has 89 outlet files plus one cover and is closed through September 2026. The separate original folder used for the real September delivery has 89 outlet files plus four covers; these are different inventories.

October is the next normal month for that approved base. After accepting a closing, register a newly verified base containing it before moving to the following month. Automatic promotion is not implemented. A different year requires an appropriate verified base.

The launcher accepts the registered base, not an arbitrary workbook folder. If a requested destination differs, review compatibility and the latest file version before delivery. Do not replace manifests just to bypass protection.

## 3. Run preflight

On the existing configured Windows computer:

```powershell
$offtakeProject = Join-Path $env:USERPROFILE 'Alchemy_AI_DEV\OFFTAKE_MVP'
$offtakePython = Join-Path $env:USERPROFILE '.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe'
& $offtakePython -B -X utf8 (Join-Path $offtakeProject 'automation\run_monthly.py') `
  --period 2026-10 `
  --reports 'C:\PATH\Reports\10 October Report' `
  --validate-only
```

Replace the period and report path with real inputs. This example does not claim October has been received or processed. These paths describe the existing installation, not a portable setup script. Another company computer must first receive the reviewed local engine and compatible runtime privately.

Existing visual entry point: `FAZER_OFFTAKE.cmd` in `OFFTAKE_MVP`. Select the month and folder and generate copies. Keep monthly closing independent from any historical action that also refreshes a dashboard.

## 4. Resolve sources, accounts and products

Intake selects compatible readers and creates a source-bound manifest/configuration. The engine reopens physical reports and checks origin, period, units, VAT basis, arithmetic and duplication. Approved reusable format rules apply only when the current physical layout matches. Missing or contradictory evidence creates an exception.

Identify accounts using wholesaler + customer code and documented aliases. Use the filename and C2 as additional checks. Shared accounts and group allocations retain their restrictions; never distribute sales among locations without current-period evidence.

Match product, SKU, size and variant using existing documented mappings. Reuse existing lines and duplicate lines first. Preserve current rebate settings. A historical label match does not prove current-period quantities, prices, VAT, zero sales or account allocation.

## 5. Generate validated copies

After resolving preflight issues, use the same command without `--validate-only`:

```powershell
& $offtakePython -B -X utf8 (Join-Path $offtakeProject 'automation\run_monthly.py') `
  --period 2026-10 `
  --reports 'C:\PATH\Reports\10 October Report'
```

Outputs contain an Excel ZIP/copies, a receipt, a readable result and `PENDENCIAS.csv`. An unchanged fingerprint can reuse an intact result; changed inputs require validation.

| Result | Meaning |
| --- | --- |
| `GERADO` | Copies passed the run's checks |
| `PARCIAL_GERADO` | Only complete eligible outlets are delivered; the full month is not closed |
| `PENDENTE`, `FALHOU`, `ENTRADAS_ALTERADAS` | Review the reason; do not treat it as an approved financial delivery |

Missing reports are not zero sales. Partial totals cover only delivered files.

## 6. Validate results

Check outlet, account code, period, unit, SKU/variant/size, wholesaler, price/VAT basis, discounts, quantities, sales values and the destination sheet's own rebate parameters. Trace amounts to selected source occurrences. Compare with independent evidence where available.

Preserve formulas, shared/array formulas, formatting, validations, objects, named ranges and metadata. Compare all other monthly sheets byte for byte. Recalculate only current-month results and dependent caches. Do not change a current parameter to force an obsolete benchmark to pass.

If a file changes externally, reconcile it and preserve the latest version. Recalculate only the affected candidate when possible. Never automatically restore an old version, reset a controller baseline or rerun the entire batch without a reason.

## 7. Deliver or install separately authorized originals

The normal generator creates copies; `--publish` stays disabled. An explicit original-folder request requires a separate reviewed delivery operation: fresh inventory/backup, exact source/plan/output hashes, exact targets, exclusive locks acquired before writing, stable file identity, durable journal, in-place writes with `fsync`, ownership-limited rollback and final verification of the actual installed files. Covers are handled separately.

That separate procedure was used for the authorized [September run](runs/2026-09/EXECUTION.md). Its frozen scripts, fixed counts, hashes and cleanup operation must not be reused as a generic publication command or future authorization.

## 8. Keep a durable receipt

Keep complete sources, backup, inventory, manifest, plan, ledger, routing, exceptions, calculation proofs, native workbook validation and installed-file validation privately. Publish only sanitized technical receipts and hashes. Update identity evidence in the shared private registry without inserting financial facts into it.

## Known limits

- Some specialist PDF readers remain bound to reviewed September sources. New PDFs, scans without text and unsupported layouts need review.
- The operational launcher historically reported 14 unresolved outlet identities. Valid existing links remain usable; uncertain accounts remain exceptions.
- Source zero/exclusion/allocation decisions do not automatically roll forward.
- Automatic base promotion, cover filling and generic original-file publication are not enabled.
- The separate shared registry is available through a read-only interface; live application migration is not claimed by this documentation.
- A real September run does not certify every future layout, customer or year.

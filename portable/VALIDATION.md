# Portable release validation — 26 October 2026

## Passed

- **35 automated unit tests**: formula calculation, ex-VAT/in-VAT arithmetic, rebate and quantity/price preservation, cache tampering/invalidation after a calculation-code change, source hashes, period checks, duplicate/missing provenance, output traversal/overwrite rejection and installation integrity.
- **24 end-to-end acceptance checks** using a physical synthetic Boozia-layout Excel report and the approved 90-file Admin base. The actual reader/planner/writer path generated one eligible filled outlet copy, with all other outlets kept pending. This is not real October sales data.
- Independent expected-cell comparison of the generated workbook, including SKU/product/size, supplier, quantity, unit price, rebate and calculated totals.
- The other 11 monthly worksheet parts, target formulas and native styles remained exact. The input report and all 90 template copies remained unchanged.
- Repeated identical input reused the verified output, without creating duplicate results. A modified executable file was rejected by the installation integrity check.
- Clean setup and reconfiguration in two different short Windows folders, including preservation of prior activation/audit records.
- Actual Charoenchai PDF reader smoke test: 12 records extracted, 11 reader controls, zero unknown records; the PDF remained unchanged. A PDF can be readable while still requiring stronger physical-period evidence at intake. This test does not approve it for every month.
- **93/93 official production workbook hashes unchanged** across packaging and tests. Existing production/DEV code and baseline were not changed.
- Independent read-only review of the portable interface, calculation stage and documentation found no remaining blocking issue after the relocation fix.

## Problems found and corrected during testing

The first full run from the deeply nested build directory hit the Windows path-length limit. The release uses a shorter output folder and checks that the installation root has at most 60 characters; the complete run then passed from a clean short directory. No Windows settings were changed.

One first acceptance assertion expected a text month, while the actual reader correctly retains a start/end date range. The assertion was corrected to compare the actual source period contract; financial output did not require a change. All 24 final acceptance checks passed.

The first stage test environment lacked a writable default temporary folder. Tests now use an explicit disposable workspace. These setup failures were retained in local evidence rather than represented as first-run success.

## Material limitations

- Tested on this Windows x64 machine in separate clean installation folders. A second physical colleague computer has not yet been tested; company endpoint policies can still require IT review.
- The interpreter is the official Python 3.13.17 Windows x64 embeddable archive, verified against its published SHA-256. Eleven pinned library wheels are bundled with hashes and license files.
- The portable backend uses the reviewed Python formula evaluator plus separate Decimal row/totals checks. It is not independently recalculated by Microsoft Excel or a second spreadsheet engine. Unsupported formulas block generation. Original formulas are preserved and the workbook requests recalculation when opened in Excel.
- Only the supplied 89-outlet template base is validated. Broader historical team scans and the 126-label identity catalogue do not establish full-company current coverage.
- Some specialist PDF layouts remain limited to the exact reviewed September sources. Missing or contradictory period/unit/VAT/identity evidence remains pending; absent data never means zero.
- Automatic cover filling, automatic base promotion, production installation, background monitoring and scheduling remain disabled/not implemented.
- Detailed inherited diagnostic messages may be in Portuguese; the launcher, result summary and installation/configuration guides are English.
- The integrity manifest is unsigned: it detects missing or changed files against the delivered manifest, but does not authenticate a maliciously replaced manifest. Review the source and licenses under company IT policy.

Run focused tests from the extracted complete company package:

```bat
runtime\python.exe -B -m unittest discover -s tests -v
```

Tests create only disposable synthetic workbooks. They must never be used as real reports or imported into analytics.

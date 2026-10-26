# Folder and company configuration

## Layout

```text
AlchemyOfftake/
  INSTALL.cmd                     Verify and configure the private package
  RUN_OFFTAKE.cmd                 Monthly interactive launcher
  offtake.py                      English command-line interface
  portable_stage.py               Local formula-cache calculation and audit
  automation/                    Existing monthly intake/orchestration
  engine/                        Existing readers, planner and native merger
  runtime/                       Portable Python and installed libraries
  wheelhouse/                    Offline library archives
  company/company.json           Private reviewed company configuration
  company/templates-closed-2026-09.zip
  company/shared-company-registry.json
  company/historical-reference/   Broader team reference only
  template-bases/                 Verified local copies created by INSTALL
  configuration/                 Local activation/audit created by INSTALL
  reports/                       Optional monthly input folders
  output/                        New monthly results only
```

Official production folders are never configured as an output destination. The program reads the verified template copies imported from the bundled company archive and generates new copies. There is no command that installs them over financial originals.

## Configuration already supplied

`company/company.json` binds the closed month, exact template ZIP hash, expected template counts and the legacy operational identity catalogue. `INSTALL.cmd` imports and verifies that archive at the new machine's actual path, then regenerates `automation/template-base.json` and its installation audit. It does not copy an old machine's absolute activation paths.

The operational account database is `engine/Automacao off-take/base-outlets/outlet-database.json`. Its 198 records span 126 literal outlet labels: 124 verified, 64 supplier-only and 10 requiring review. A verified record is historical evidence; current-report identity must still match. Unknown codes are never guessed. Source product mappings remain scoped to the evidenced outlet, SKU, product and bottle size.

The separate shared registry and broader Bangkok index are provided for reference and future controlled onboarding. They do not automatically replace the engine's operational catalogue and do not create missing prices, VAT evidence, source coverage or customer codes.

## Add other company outlets or update a closed base

Additional team scans alone are insufficient. Obtain the actual approved current Excel templates, verify the outlet identity in file name and C2, and match supplier + customer code with documentary evidence. Review SKU/size mappings, existing rebate cells, year/month headers and duplicate-row capacity. Preserve current prices from the actual monthly reports and preserve old months.

An administrator must create a new reviewed company configuration/template archive and regenerate the package integrity manifest through a controlled release. Do not hand-edit the sealed configuration and bypass hash errors. Register the actual latest accepted `closed_through`; never declare a month closed based on missing reports. The generic manifest checks derive counts from the reviewed inventory rather than hardcoding 89 outlets, but only the bundled 89-outlet base has been validated in this release.

## Command-line use

From the extracted package folder:

```bat
runtime\python.exe -B offtake.py doctor
runtime\python.exe -B offtake.py configure
runtime\python.exe -B offtake.py run --period 2026-10 --reports "C:\Monthly Reports\2026-10"
runtime\python.exe -B offtake.py run --period 2026-10 --reports "C:\Monthly Reports\2026-10" --validate-only
```

`configure` is safe to repeat with the same reviewed archive. If the package is moved to a different short folder, run `INSTALL.cmd` there again before monthly processing. No service, scheduled task or model/API call is created.

The templates already contain the rebate rules. Blank P values remain unknown; the program does not replace them with zero. Both VAT-included and ex-VAT calculations stay explicitly separated. Details and source evidence are retained in the private execution receipt.

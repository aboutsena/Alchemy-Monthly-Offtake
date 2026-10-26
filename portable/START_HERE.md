# Alchemy Monthly Off-Take — Windows package

This **private company package** contains the executable program, a portable Python interpreter, all required libraries, the reviewed company configuration and Excel template archive. No Codex, ChatGPT subscription, paid API, Excel automation, Node.js, administrator access or internet connection is needed to run it.

## Install once

1. Right-click the ZIP and choose **Extract All**. Use a short folder such as `C:\Users\YOUR_NAME\AlchemyOfftake` (at most 60 characters). Do not run the program from inside the ZIP or leave it in a long nested download folder.
2. Open the extracted folder and double-click **INSTALL.cmd**. The program verifies its files, checks the template archive and creates its own input copies and configuration. It never installs into the official spreadsheet folder.
3. The final message should say **Installation verified**. Then use **RUN_OFFTAKE.cmd**.

If Windows or company policy blocks an unsigned downloaded program, ask company IT to review it. Do not disable security settings.

## Run each month

1. Put only the actual wholesaler reports for that month in a separate folder. Keep historical scans, earlier generated files and test data out of it.
2. Double-click **RUN_OFFTAKE.cmd**.
3. Enter the month as `YYYY-MM` and paste the report folder path. For this template base the next month is **2026-10**; there are no real October sales bundled with the program.
4. Wait for the result page. Validated filled workbook **copies** are in a ZIP under `output`. Review `PENDENCIAS.csv` for unknown accounts, products, dates, VAT, units or unsupported layouts.
5. Have the responsible administrator review the output before replacing any official workbook. Automatic publication is disabled.

**PARTIAL_COPIES_GENERATED is not a completed monthly close.** Only eligible complete outlets are generated; missing information never means zero sales.

## What is included

- The actual report readers, monthly planner, formula model and native Excel merger, copied from the existing reviewed DEV engine.
- Portable Python 3.13.17 for **Windows x64** and 11 pinned library wheels, with license files and hashes. Libraries are already present in `runtime`; `wheelhouse` holds their offline installation archives.
- The approved Admin template archive: **89 outlet workbooks and 1 cover**, closed through September 2026. The program does not automatically fill the cover.
- The existing broader historical identity catalogue: **126 outlet labels / 198 supplier-account records**. Verified, supplier-only and review states remain distinct; it is not a complete current company master.
- The broader Bangkok team historical reference index. Its scans are not additional approved Excel templates or automatic routing authority. The raw historical PDFs are not bundled.
- English installation/configuration documentation and source code. Some inherited detailed diagnostics remain in Portuguese or the original report language.

## Current limits

This is a working initial distribution for the supported templates and report layouts. It is **not proof that every company outlet, every supplier format or every month is covered**.

Some specialist PDF readers are still restricted to the exact reviewed September sources; new months/layouts for those readers require review. Scanned PDFs without extractable text require manual review. Missing or conflicting customer codes and new products remain pending.

Formula caches use the reviewed Python formula model, independently checked against transaction-row Decimal arithmetic and expected totals. This distribution does not include a second independent Excel/Artifact calculation engine. Original formulas, styles, rebate parameters and other monthly sheets are preserved and audited. Unsupported formulas stop processing.

After a month is accepted, register a new approved template base that contains that close. The program does not promote results automatically. A new year also requires an approved template base for that year.

See [CONFIGURATION.md](CONFIGURATION.md), [LIBRARIES.json](LIBRARIES.json) and [VALIDATION.md](VALIDATION.md).

## Confidentiality

**Share this ZIP only with authorized company colleagues.** It contains real company identities and templates with historical commercial information. The public GitHub repository contains the technical handoff/portable interface, not these private templates or customer data.

Off-take is separate from the commercial dashboard. No dashboard, Power BI connection, scheduler, email sender, credentials or API key is included.

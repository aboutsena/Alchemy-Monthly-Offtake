# Executable Windows package — v0.1.0

The first functional **private company distribution** has been built. It includes the actual frozen report readers, monthly engine, portable Python, all libraries, reviewed company configuration and the Admin Excel template archive. Authorized colleagues receive `Alchemy_Offtake_Windows_x64_v0.1.0_PRIVATE.zip` directly from Lucas.

This public repository now also contains the [portable interface and calculation-stage source](portable/), [pinned dependencies](portable/requirements.txt), [library provenance/hashes](portable/LIBRARIES.json), [installation guide](portable/START_HERE.md), [configuration guide](portable/CONFIGURATION.md) and [validation report](portable/VALIDATION.md).

**The complete private ZIP is required to run the configured company workflow.** Cloning this public repository alone is still insufficient: the existing frozen readers contain literal customer mappings and are delivered privately with the company configuration/templates. The public directory does not contain those commercial records, raw reports or workbooks.

## For the colleague receiving the private ZIP

1. Extract the complete ZIP to a short folder such as `C:\Users\YOUR_NAME\AlchemyOfftake` (maximum 60 characters).
2. Double-click `INSTALL.cmd` and wait for **Installation verified**.
3. Double-click `RUN_OFFTAKE.cmd`, choose `YYYY-MM` and paste the actual monthly report folder.
4. Review the generated workbook copies and pending issues under `output`. Automatic replacement of production workbooks is disabled.

The package runs locally and offline on **Windows x64**, without Codex, Node.js, Microsoft Excel automation or a paid API. Its own Python and installed libraries are included, together with offline wheel archives and license files.

## Proven scope and limits

- 35 automated unit tests and 24 independent end-to-end acceptance checks passed; installation relocation was tested in separate Windows folders. See [validation](portable/VALIDATION.md).
- Actual reader/planner/writer execution generated a filled workbook copy from a physical synthetic report. The other 11 months, formulas, styles, 90 template inputs and report were preserved. This was not actual October sales.
- The private package includes 89 approved outlet templates and one cover, closed through September 2026. The broader historical catalogue/reference does not establish complete company-wide current coverage.
- The existing specialist PDF/month restrictions, uncertain codes/products and missing physical period/unit/VAT evidence remain visible blockers. No missing information becomes zero.
- The portable formula stage uses the existing reviewed Python evaluator plus independent Decimal row/totals checks. It does not claim a second independent Excel calculation engine.
- No financial production publication, watcher, scheduler, dashboard integration, credentials or API keys are enabled.

The private company ZIP must not be uploaded into this public repository. Its integrity hashes are unsigned checks, not a software-publisher signature; company IT may review the source and libraries before use.

# Monthly Off-Take

A repeatable monthly workflow for turning wholesaler reports into outlet off-take Excel workbooks, while preserving previous months, product mappings, formulas and current rebate settings.

**Off-take and the commercial dashboard are separate products.** Off-take uses wholesaler reports. The dashboard uses finance-approved Power BI for performance. They may share a private company/outlet identity registry; neither depends on running the other.

## Start here

1. [Monthly operating procedure](MONTHLY_WORKFLOW.md).
2. [Business rules](BUSINESS_RULES.md).
3. [Company-wide rollout checklist](COMPANY_ROLLOUT.md).
4. [Run request contract](contracts/run-request.schema.json).
5. [Sanitized September validation record](runs/2026-09/EXECUTION.md).

## What this public package contains

This is the shareable operating reference, input contract and validation record for an existing local implementation. It is **not a standalone installation of the financial engine**. Cloning this repository alone will not fill spreadsheets. The reviewed engine, spreadsheet runtime, approved templates and business configuration must be supplied and configured privately for the company environment.

The public package does not contain customer identities, account codes, company records, wholesaler reports, completed spreadsheets, contracts, actual sales figures or rebate parameters. The shared identity registry stays in the private Hub.

## Verified capabilities and current boundaries

| Capability | Evidence / current state |
| --- | --- |
| Read a monthly report folder and generate validated Excel copies | Existing local implementation, including preflight and explicit exceptions |
| Real September reprocessing | Completed in the specifically authorized original folder: 89 outlets checked, 68 filled, 21 confirmed without entries |
| History preservation | 979 worksheets for the other months checked byte for byte |
| Original-file delivery in that run | Separate explicitly authorized operation with backup, exclusive locks, stable file identity, journal and final verification |
| Generic monthly publication to originals | Still separate; the engine's `--publish` gate remains disabled |
| Real October processing | Not performed by this publication |
| Automatic result-to-template promotion | Not implemented |
| Automatic execution when reports arrive | Not enabled by this package |
| Company-wide compatibility | Requires the company's actual templates, accounts and report layouts to pass onboarding and tests |

September-specific prices, exclusions, zero confirmations, source hashes and reprocessing scripts are not a general recipe for future months.

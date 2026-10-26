# Using the process across the company

This repository is an operating/reference package. The company's reviewed engine installation and private configuration are required for live processing; they are not bundled here. Do not promise that a repository clone alone will process all company reports.

1. Appoint the monthly operator and the owner of each approved workbook base/year.
2. Provision the existing reviewed financial engine and compatible spreadsheet runtime privately. The current implementation depends on its existing local Python/Node environment and spreadsheet tooling; it is not an independently packaged public executable.
3. Create a private, versioned company/outlet registry: stable IDs, legal/trading names, aliases, wholesaler/customer codes, source evidence, status, effective-period information and shared-account restrictions.
4. Register each wholesaler's physical report format, period evidence, bottle/case semantics and VAT basis. Do not assume a department's existing layout covers every other team.
5. Verify SKU/variant/size mappings and current workbook parameters for each outlet/template. Do not carry another outlet's rebate or historical price into a new mapping.
6. Run preflight and a pilot on copies for each distinct layout/template before extending the batch. Include negative tests for wrong periods, unknown accounts/SKUs, duplicated occurrences, missing VAT/unit evidence and externally changed files.
7. Compare quantities and values against independent source evidence, preserve other months and verify the actual delivered files. Keep exception handling separate from the complete outlets.
8. Require an explicit reviewed delivery mechanism for original files. A successful preview is not an authorization to overwrite financial workbooks.
9. Keep templates, configuration, reports, completed files, financial results and identity records private. Use the public repository for procedures/contracts only.
10. After accepting a month, register the next approved base without losing the newly closed history. Do not treat base promotion as automatic.

## Ownership boundaries

| Component | Responsibility |
| --- | --- |
| Off-take module | Report intake, monthly workbook generation, financial validation, exceptions and authorized delivery |
| Shared private registry | Evidenced company/outlet/account identities, aliases, restrictions and version history |
| Dashboard module | Commercial analysis from approved BI facts; identity lookup does not replace its financial source |

The same process can be extended to more teams after their actual inputs pass onboarding. The recorded September test demonstrates its tested scope, not universal company-wide compatibility.

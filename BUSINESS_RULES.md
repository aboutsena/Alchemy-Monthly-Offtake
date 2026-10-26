# Off-take business rules

## Outlet and company identity

Use the workbook filename and C2 plus an evidenced wholesaler/customer-code relationship. Keep codes as text, preserving punctuation and leading zeros. Trading names, legal names, translations and aliases are separate observed fields. Similar spelling is not identity evidence.

A company may have multiple locations and accounts. A group label or BI display alias does not automatically merge off-take accounts or allocate transactions. The shared company registry provides identity only, retaining pending statuses and restrictions.

## Month selection

Sheets `01`–`12` represent January–December. Use the physically evidenced report period and check year, approved base and chronological sequence. The last chronologically populated month indicates the next expected month. Never choose the first historical zero. If all months are empty, use the report's evidenced month. Never create sheet `13`.

Preserve historical gaps. Normal processing does not overwrite a populated month. Reprocessing a closed month requires a specific request; September cleanup was an exception, not a recurring step.

## SKUs, variants, duplicates and wholesalers

- Reuse existing product/SKU/size lines and existing duplicates first.
- Within the current month, separate distinct product/SKU + wholesaler + effective unit price + VAT-basis combinations.
- A price or wholesaler change between different months does not automatically create a new mapping.
- Add only the extra lines actually needed, in verified space with known metadata, formulas and parameters. Otherwise report an exception.
- Do not identify products using another month's price or brand alone. Size and variant remain explicit.

## Quantities, prices, VAT and discounts

Use actual reports as the financial source. Bottle units need evidence; do not infer bottle count from a `Qty` heading alone or convert cases without verified packing.

For the existing template, `J` holds wholesaler, `K` price including VAT, `L` price excluding VAT, and `N` bottles. Fill only the proven price-basis column. Preserve original printed observations separately from their interpretation. Apply evidenced discounts once.

Reconcile quantity × effective price with the report amount. A reviewed monthly aggregate may only support a weighted average; disclose that basis rather than inventing invoice-level prices. Duplicate PDF/Excel representations need an evidenced selection rule; identical-looking physical lines are not automatically discarded.

## Formulas and rebates

Keep original financial formulas, shared formulas and arrays. Current destination-sheet parameters determine the native financial calculation. A missing rebate rate is not zero. Do not import old rates to make an old benchmark pass. Distinguish a sales discrepancy from a pre-existing parameter difference.

Update only current-month inputs and directly dependent calculated caches. Preserve the other months, formula structures, metadata, styles and workbook objects.

## Missing information and confirmed zero

`CONFIRMED_ZERO`, `MISSING_SOURCE`, `AMBIGUOUS`, `DIVERGENT` and `RECORDED_IN_EXCEL` are different states. Missing information is not zero. A zero, shared-account allocation or exclusion is scoped to its evidenced period/source/occurrence and does not silently carry into a future month.

One source occurrence cannot be allocated twice. Preserve traceability to report file/hash and page, row or cell.

## Separation from the dashboard

Monthly off-take uses wholesaler reports. Financial performance, growth, rankings and commercial opportunities in the dashboard use finance-approved Power BI only. A shared identity registry does not permit filling BI gaps with Excel/PDF sales or summing overlapping sources.

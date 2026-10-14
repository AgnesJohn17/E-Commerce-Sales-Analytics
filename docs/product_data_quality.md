# Product data quality: merchandise vs service codes

The original UCI Online Retail workbook contains entries that represent logistics or accounting charges alongside sellable merchandise. Ranking all StockCodes together **does not** give a pure ranking of products.

For example, top gross-sales entries include:
- `DOT` / DOTCOM POSTAGE: £206,248.77 (service/postage)
- `22423` / REGENCY CAKESTAND 3 TIER: £174,156.54 (merchandise)
- `23843` / PAPER CRAFT, LITTLE BIRDIE: £168,469.60 (merchandise)
- `85123A` / WHITE HANGING HEART T-LIGHT HOLDER: £104,284.24
- `47566` / PARTY BUNTING: £99,445.23

These values come from the independently processed original workbook using the same positive-sales inclusion rules documented in `verified_findings.md`.

**Recommended improvement:** Create a documented merchandise classification mapping and distinguish postage, manual adjustments and other non-product codes before reporting a 'best-selling product.' Avoid applying an unverified blanket exclusion based only on a StockCode prefix. Gross sales include postage as recorded in source, so removing service codes changes the reporting definition.

The public GitHub repository should contain only aggregate results, not customer-level transaction exports.

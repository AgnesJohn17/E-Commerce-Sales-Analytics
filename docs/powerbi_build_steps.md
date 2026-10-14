# Power BI Desktop — final implementation steps

**Status: not yet built.** No native `.pbix` file has been generated. The existing HTML dashboard is a working alternative, but it is not Power BI.

## Use the verified dataset

1. Clone the repository, install `requirements.txt`, and download the original UCI `Online Retail.xlsx` workbook.
2. Run:
   ```bash
   python src/analyze_workbook.py --input "Online Retail.xlsx" --output outputs
   python src/validate_results.py --input outputs
   ```
3. The benchmark to verify is **541,909 source rows and £10,642,110.80 gross positive sales**. If validation fails, resolve differences before using the results.

## Import into Power BI

Use **Home → Get data → Text/CSV** to import `outputs/monthly_sales.csv`, `outputs/country_sales.csv` and `outputs/top_products.csv`. These are already aggregated and have no customer-level identifiers. Do not join summary files together: they represent different aggregation grains.

For a truly interactive report where month/country/product slicers can cross-filter, use the original XLSX as the source in Power Query and implement the sales-cleaning rules in the README. Aggregate summary files cannot cross-filter each other.

## Suggested report pages

- Overview: Total gross positive sales KPI (using the complete monthly table), sales trend by month, total unique orders KPI if sourced from the verified global summary, and explanation of gross vs net.
- Geography: Country-level gross sales and share-of-total.
- Products: Product-revenue chart **explicitly labeled as including service/postage codes** until merchandise classification is implemented.

Set amounts to British pounds (£); make December 2011 visibly marked as a partial period.

## Before claiming Power BI proficiency on the resume

Actually build and save the report in Power BI Desktop, verify the visuals against `docs/verified_findings.md`, and capture screenshots. Save the `.pbix` locally or to GitHub Releases if its size and dataset licensing permit. Don't label an HTML dashboard as a Power BI deliverable.

# E-Commerce Sales Analytics

An end-to-end portfolio project exploring revenue, products, and customer purchasing patterns using **Python, SQL and a standalone interactive HTML dashboard**.

**Status: validated analytics dashboard delivered.** The complete 541,909-row original UCI workbook was exported and reanalyzed; all 10 reference KPIs matched the independently verified workbook benchmark, including £10,642,110.80 gross positive sales, and SQL KPI checks passed locally. The standalone browser dashboard is published in [`dashboard/index.html`](dashboard/index.html). A native Power BI report is not part of the completed scope.

## Project goals
- Validate and clean transaction-level retail data.
- Calculate revenue, orders, unique customers, and monthly sales performance.
- Investigate top products, repeat customers, and revenue concentration.
- Prepare reporting-ready CSV tables and SQL queries.
- Build and document an interactive HTML dashboard without requiring Microsoft Power BI.

## Dataset format
Use a retail transactions CSV with columns: `InvoiceNo`, `StockCode`, `Description`, `Quantity`, `InvoiceDate`, `UnitPrice`, `CustomerID`, `Country`. The UCI **Online Retail** dataset has this structure (originally distributed as XLSX). Convert the original XLSX to CSV using a spreadsheet application or Python before running the pipeline. See `data/README.md` for details. No raw dataset is redistributed in this repository.

## Quick start
```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
python src/analyze.py --input data/online_retail.csv --output outputs
python -m unittest discover -s tests -v
```

Outputs include `monthly_sales.csv`, `top_products.csv`, `country_sales.csv`, `customer_summary.csv`, and `summary.json`. Returns/cancellations are excluded from **gross merchandise sales** and reported separately in the summary. Revenue is before tax/shipping because these fields are unavailable. These choices are analytical assumptions, not accounting revenue recognition.

## SQL
The `sql/` folder contains a PostgreSQL table definition and KPI queries. Import cleaned sales lines from Python output or map your data to the documented schema.

## Roadmap
- [x] Define scope and reproducible project structure
- [x] Validate end-to-end execution with the complete original public workbook and converted CSV
- [x] Publish initial verified aggregate charts and business narrative
- [x] Reconcile full CSV pipeline KPIs against original-workbook benchmark; verify SQL KPI calculations
- [x] Create portable, interactive browser dashboard (HTML; not `.pbix`)
- [x] Publish benchmark KPIs and initial business findings
- [x] Publish working interactive dashboard and documented, resume-ready verified project metrics

## Limitations
The public Online Retail dataset is historical and not representative of modern e-commerce behavior. Customer IDs are missing on some rows. Reporting rules and all achieved project results will be documented only after actually running the pipeline.

## Verified historical findings

Direct analysis of the full UCI workbook (541,909 source rows) identified **£10,642,110.80 in gross positive sales**, **19,960 distinct sales orders**, and **4,338 identified customers**. November 2011 was the highest gross-sales month (£1,503,866.78). **The full CSV pipeline has now been reconciled to the original-workbook benchmark (2026-10-15).**

- [Detailed calculations and limitations](docs/verified_findings.md)
- [Business recommendations](docs/business_insights.md)
- [Monthly sales chart](reports/charts/monthly_sales.svg)
- [Country comparison](reports/charts/country_sales.svg)

## Interactive dashboard preview

Open [`dashboard/index.html`](dashboard/index.html) in a browser to interactively filter the independently verified monthly and country aggregates. This is HTML, **not** a Power BI `.pbix`. The original workbook benchmark reconciles to £10,642,110.80 across monthly and country aggregates. The complete 541,909-row standard CSV import was separately validated against this benchmark. A native Power BI report is intentionally not required.

## Validation update (2026-10-14)

The original Excel-workbook benchmark was reconciled across the complete 13-month and 38-country aggregate CSV files: **£10,642,110.80** in both. Run `python src/verify_published_aggregates.py` to check the committed reports. The standalone interactive HTML dashboard is available in `dashboard/index.html`. This is **not** a native Power BI `.pbix`; the Power BI Desktop report remains a separate deliverable. The full CSV conversion pipeline remains to be reconciled independently.

## Final delivery update (2026-10-15)

The complete original workbook was converted into a **541,909-row** CSV; the analysis pipeline output matched all published benchmark counts and £10,642,110.80 gross sales. Independent local SQL checks confirmed gross sales, 19,960 orders, 4,338 identified customers, 2,845 identified repeat customers, 13 months and 38 countries. The new [CommerceLens interactive dashboard](dashboard/index.html) includes month-filtered sales metrics and trend, country ranking, product-code performance, and transparent limitations. Year selection does not cross-filter country or product summary tables. No customer-level dataset is published. Open the HTML file in a browser or download it from the repository.

**Resume bullet:** Analyzed 541,909 historical e-commerce transaction lines with Python and SQL; validated 524,878 positive sales lines and £10.64M gross sales, and delivered an interactive browser dashboard of revenue trends, geographic markets and purchasing patterns.

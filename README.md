# E-Commerce Sales Analytics

An end-to-end, reproducible portfolio project exploring revenue, products, and customer purchasing patterns using **Python, SQL, and Power BI**.

**Status:** In development. Original Excel dataset analyzed; verified aggregate findings and SVG charts have been committed. The CSV-based pipeline still needs end-to-end reconciliation, and an interactive Power BI report is planned, not yet published.

## Project goals
- Validate and clean transaction-level retail data.
- Calculate revenue, orders, unique customers, and monthly sales performance.
- Investigate top products, repeat customers, and revenue concentration.
- Prepare reporting-ready CSV tables and SQL queries.
- Build and document an interactive Power BI dashboard after analysis is validated.

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
- [ ] Validate end-to-end execution with the public dataset
- [x] Publish initial verified aggregate charts and business narrative
- [ ] Validate charts and CSV pipeline end-to-end against original workbook
- [ ] Create interactive Power BI `.pbix` report
- [x] Publish benchmark KPIs and initial business findings
- [ ] Publish actual dashboard screenshots and resume-ready implementation outcomes

## Limitations
The public Online Retail dataset is historical and not representative of modern e-commerce behavior. Customer IDs are missing on some rows. Reporting rules and all achieved project results will be documented only after actually running the pipeline.

## Verified historical findings

Direct analysis of the full UCI workbook (541,909 source rows) identified **£10,642,110.80 in gross positive sales**, **19,960 distinct sales orders**, and **4,338 identified customers**. November 2011 was the highest gross-sales month (£1,503,866.78). **The standard CSV-import pipeline has not yet been reconciled against the direct-workbook benchmark.**

- [Detailed calculations and limitations](docs/verified_findings.md)
- [Business recommendations](docs/business_insights.md)
- [Monthly sales chart](reports/charts/monthly_sales.svg)
- [Country comparison](reports/charts/country_sales.svg)

## Interactive dashboard preview

Open [`dashboard/index.html`](dashboard/index.html) in a browser to interactively filter the independently verified monthly and country aggregates. This is HTML, **not** a Power BI `.pbix`. The original workbook benchmark reconciles to £10,642,110.80 when summing both monthly and country results. Full standard-import end-to-end pipeline validation and creation of the native Power BI report remain outstanding.

## Validation update (2026-10-14)

The original Excel-workbook benchmark was reconciled across the complete 13-month and 38-country aggregate CSV files: **£10,642,110.80** in both. Run `python src/verify_published_aggregates.py` to check the committed reports. The standalone interactive HTML dashboard is available in `dashboard/index.html`. This is **not** a native Power BI `.pbix`; the Power BI Desktop report remains a separate deliverable. The full CSV conversion pipeline remains to be reconciled independently.

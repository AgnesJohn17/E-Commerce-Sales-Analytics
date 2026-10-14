# E-Commerce Sales Analytics

An end-to-end, reproducible portfolio project exploring revenue, products, and customer purchasing patterns using **Python, SQL, and Power BI**.

**Status:** In development. Python analysis and SQL query templates are being implemented. A Power BI report is planned, not yet published.

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
- [ ] Complete exploratory visualizations and business narrative
- [ ] Create interactive Power BI `.pbix` report
- [ ] Publish screenshots, findings, and resume-ready quantitative results

## Limitations
The public Online Retail dataset is historical and not representative of modern e-commerce behavior. Customer IDs are missing on some rows. Reporting rules and all achieved project results will be documented only after actually running the pipeline.

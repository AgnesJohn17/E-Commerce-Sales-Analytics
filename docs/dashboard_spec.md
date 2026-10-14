# Power BI Dashboard Plan

**Status: planned** — no PBIX dashboard has been created yet.

## Source
Run the Python pipeline to produce cleaned sales data and KPI files. Use `outputs/cleaned_sales.csv` as the transaction-level fact table. Import the summaries separately for reporting; **do not directly join aggregate tables to transaction rows**, as this can multiply metrics.

## Measures (DAX)
```dax
Gross Sales = SUM(cleaned_sales[SalesAmount])
Orders = DISTINCTCOUNT(cleaned_sales[InvoiceNo])
Units Sold = SUM(cleaned_sales[Quantity])
Average Order Value = DIVIDE([Gross Sales], [Orders])
```

## Proposed pages
1. **Executive overview**: gross sales, orders, average order value, monthly trend and country slicers.
2. **Products and geography**: top products, units, revenue by country.
3. **Customers**: repeat-order proportion and highest-spending identified customers.

## Metric caveats
- Amounts represent positive-line gross merchandise sales, excluding cancellations and negative-quantity returns; they are not net realized revenue.
- UCI Online Retail prices are denominated in GBP.
- Missing customer IDs are included in revenue, but cannot be included in identifiable customer counts.
- Save dashboard screenshots and a real PBIX before claiming the dashboard is completed.

"""Reproducible online retail KPI pipeline.

Run: python src/analyze.py --input 'Online Retail.xlsx' --output outputs
Sales metrics exclude negative quantities, invalid prices and cancellation invoices.
"""
import argparse
import json
from pathlib import Path
import pandas as pd

REQUIRED = ["InvoiceNo", "StockCode", "Description", "Quantity", "InvoiceDate", "UnitPrice", "CustomerID", "Country"]

def analyze(df: pd.DataFrame):
    missing = set(REQUIRED) - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")
    frame = df.copy()
    original_rows = len(frame)
    frame = frame.drop_duplicates()
    duplicates = original_rows - len(frame)
    frame["InvoiceNo"] = frame["InvoiceNo"].astype("string").str.strip()
    frame["StockCode"] = frame["StockCode"].astype("string").str.strip()
    frame["Description"] = frame["Description"].astype("string").str.strip()
    frame["Country"] = frame["Country"].astype("string").str.strip()
    frame["CustomerID"] = frame["CustomerID"].astype("string").str.strip()
    frame["Quantity"] = pd.to_numeric(frame["Quantity"], errors="coerce")
    frame["UnitPrice"] = pd.to_numeric(frame["UnitPrice"], errors="coerce")
    frame["InvoiceDate"] = pd.to_datetime(frame["InvoiceDate"], errors="coerce")
    invalid = (frame["InvoiceNo"].isna() | frame["StockCode"].isna() |
               frame["InvoiceDate"].isna() | frame["Quantity"].isna() |
               frame["UnitPrice"].isna() | (frame["UnitPrice"] <= 0))
    cancelled = frame["InvoiceNo"].str.upper().str.startswith("C").fillna(False)
    returns = cancelled | (frame["Quantity"] < 0)
    return_lines = int((returns & ~invalid).sum())
    sales = frame.loc[~invalid & ~returns & (frame["Quantity"] > 0)].copy()
    sales["SalesAmount"] = (sales["Quantity"] * sales["UnitPrice"]).round(2)
    sales["Month"] = sales["InvoiceDate"].dt.to_period("M").astype(str)
    monthly = sales.groupby("Month", as_index=False).agg(
        Revenue=("SalesAmount", "sum"), Orders=("InvoiceNo", "nunique"),
        Units=("Quantity", "sum"))
    top_products = (sales.groupby(["StockCode", "Description"], dropna=False, as_index=False)
                    .agg(Revenue=("SalesAmount", "sum"), Units=("Quantity", "sum"))
                    .sort_values("Revenue", ascending=False).head(20))
    countries = (sales.groupby("Country", dropna=False, as_index=False)
                 .agg(Revenue=("SalesAmount", "sum"), Orders=("InvoiceNo", "nunique"))
                 .sort_values("Revenue", ascending=False))
    identified = sales.dropna(subset=["CustomerID"]).copy()
    customers = identified.groupby("CustomerID", as_index=False).agg(
        Revenue=("SalesAmount", "sum"), Orders=("InvoiceNo", "nunique"))
    customers["RepeatCustomer"] = customers["Orders"] > 1
    summary = {
        "source_rows": int(original_rows), "duplicate_rows_removed": int(duplicates),
        "invalid_rows_excluded": int(invalid.sum()), "return_or_cancellation_rows_excluded": return_lines,
        "sales_rows": int(len(sales)), "gross_sales": round(float(sales["SalesAmount"].sum()), 2),
        "orders": int(sales["InvoiceNo"].nunique()), "identified_customers": int(len(customers)),
        "repeat_customers": int(customers["RepeatCustomer"].sum()),
        "unidentified_sales_rows": int(sales["CustomerID"].isna().sum()),
        "method": "Positive-quantity, positive-price non-cancellation lines; gross sales before shipping/tax.",
    }
    return sales, monthly, top_products, countries, customers, summary

def main():
    parser = argparse.ArgumentParser(description="Clean retail transactions and export KPIs")
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output", default=Path("outputs"), type=Path)
    args = parser.parse_args()
    if args.input.suffix.lower() == ".xlsx":
        # Load original workbook directly: avoid partially converted intermediate CSV files.
        from openpyxl import load_workbook
        book = load_workbook(args.input, read_only=True, data_only=True)
        try:
            rows = book.active.values
            columns = next(rows)
            data = pd.DataFrame(rows, columns=columns)
        finally:
            book.close()
    else:
        data = pd.read_csv(args.input, dtype={"InvoiceNo": "string", "StockCode": "string", "CustomerID": "string"})
    sales, monthly, products, countries, customers, summary = analyze(data)
    args.output.mkdir(parents=True, exist_ok=True)
    for name, df in [("cleaned_sales", sales), ("monthly_sales", monthly), ("top_products", products),
                     ("country_sales", countries), ("customer_summary", customers)]:
        df.to_csv(args.output / f"{name}.csv", index=False)
    (args.output / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))

if __name__ == "__main__":
    main()

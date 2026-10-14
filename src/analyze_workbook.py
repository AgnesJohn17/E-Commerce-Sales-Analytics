"""Reproduce historical UCI Online Retail aggregates directly from the XLSX.

Usage:
    python src/analyze_workbook.py --input "Online Retail.xlsx" --output outputs

No intermediate CSV or raw customer records are published.
"""
import argparse
import json
from pathlib import Path
import pandas as pd
from openpyxl import load_workbook

def run(input_path: Path, output_path: Path):
    book = load_workbook(input_path, read_only=True, data_only=True)
    try:
        iterator = iter(book.active.values)
        columns = next(iterator)
        rows = list(iterator)
    finally:
        book.close()
    data = pd.DataFrame(rows, columns=columns)
    original = len(data)
    data = data.drop_duplicates()
    duplicates = original - len(data)
    for key in ("InvoiceNo", "StockCode", "CustomerID", "Country"):
        data[key] = data[key].astype("string").str.strip()
    data["Quantity"] = pd.to_numeric(data["Quantity"], errors="coerce")
    data["UnitPrice"] = pd.to_numeric(data["UnitPrice"], errors="coerce")
    data["InvoiceDate"] = pd.to_datetime(data["InvoiceDate"], errors="coerce")
    invalid = (data["InvoiceNo"].isna() | data["StockCode"].isna() |
               data["InvoiceDate"].isna() | data["Quantity"].isna() |
               data["UnitPrice"].isna() | (data["UnitPrice"] <= 0))
    cancelled = data["InvoiceNo"].str.upper().str.startswith("C").fillna(False)
    returns = cancelled | (data["Quantity"] < 0)
    sales = data.loc[~invalid & ~returns & (data["Quantity"] > 0)].copy()
    sales["SalesAmount"] = (sales["Quantity"] * sales["UnitPrice"]).round(2)
    sales["Month"] = sales["InvoiceDate"].dt.to_period("M").astype(str)
    monthly = sales.groupby("Month", as_index=False).agg(
        Revenue=("SalesAmount", "sum"), Orders=("InvoiceNo", "nunique"),
        Units=("Quantity", "sum"))
    products = (sales.groupby(["StockCode", "Description"], dropna=False, as_index=False)
                .agg(Revenue=("SalesAmount", "sum"), Units=("Quantity", "sum"))
                .sort_values("Revenue", ascending=False).head(20))
    countries = (sales.groupby("Country", dropna=False, as_index=False)
                 .agg(Revenue=("SalesAmount", "sum"), Orders=("InvoiceNo", "nunique"))
                 .sort_values("Revenue", ascending=False))
    identified = sales.dropna(subset=["CustomerID"])
    customers = identified.groupby("CustomerID", as_index=False).agg(
        Revenue=("SalesAmount", "sum"), Orders=("InvoiceNo", "nunique"))
    customers["RepeatCustomer"] = customers["Orders"] > 1
    summary = {
        "source_rows": original, "duplicate_rows_removed": duplicates,
        "invalid_rows_excluded": int(invalid.sum()),
        "return_or_cancellation_rows_excluded": int((returns & ~invalid).sum()),
        "sales_rows": len(sales), "gross_sales": round(float(sales["SalesAmount"].sum()), 2),
        "orders": int(sales["InvoiceNo"].nunique()),
        "identified_customers": len(customers),
        "repeat_customers": int(customers["RepeatCustomer"].sum()),
        "unidentified_sales_rows": int(sales["CustomerID"].isna().sum())
    }
    output_path.mkdir(parents=True, exist_ok=True)
    for name, frame in [
        ("monthly_sales", monthly), ("top_products", products),
        ("country_sales", countries), ("customer_summary", customers)
    ]:
        frame.to_csv(output_path / (name + ".csv"), index=False)
    (output_path / "summary.json").write_text(json.dumps(summary, indent=2))
    assert abs(float(monthly["Revenue"].sum()) - summary["gross_sales"]) < 0.01
    assert abs(float(countries["Revenue"].sum()) - summary["gross_sales"]) < 0.01
    print(json.dumps(summary, indent=2))
    return summary

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, default=Path("outputs"))
    args = parser.parse_args()
    run(args.input, args.output)

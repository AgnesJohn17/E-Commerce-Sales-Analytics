"""Verify published aggregate files against the independent original-XLSX benchmark.

Run: python src/verify_published_aggregates.py --data reports
No customer-level data required.
"""
import argparse
import csv
import json
from decimal import Decimal
from pathlib import Path

EXPECTED = Decimal("10642110.80")
EXPECTED_MONTHS = 13

def revenue_sum(path):
    with path.open(newline="", encoding="utf-8") as stream:
        rows = list(csv.DictReader(stream))
    if not rows or "Revenue" not in rows[0]:
        raise ValueError(f"Missing Revenue values in {path}")
    return sum((Decimal(row["Revenue"]) for row in rows), Decimal("0")), rows

def verify(monthly_file, countries_file):
    months_total, months = revenue_sum(monthly_file)
    countries_total, countries = revenue_sum(countries_file)
    errors = []
    if len(months) != EXPECTED_MONTHS:
        errors.append(f"Expected 13 month entries, found {len(months)}")
    if len(countries) != 38:
        errors.append(f"Expected 38 countries, found {len(countries)}")
    if abs(months_total - EXPECTED) >= Decimal("0.01"):
        errors.append(f"Monthly totals mismatch: {months_total} != {EXPECTED}")
    if abs(countries_total - EXPECTED) >= Decimal("0.01"):
        errors.append(f"Country totals mismatch: {countries_total} != {EXPECTED}")
    best = max(months, key=lambda x: Decimal(x["Revenue"]))
    if best["Month"] != "2011-11":
        errors.append(f"Wrong peak month: {best['Month']}")
    if errors:
        raise AssertionError("; ".join(errors))
    return {"monthly_total": str(months_total), "country_total": str(countries_total),
            "month_count": len(months), "country_count": len(countries), "peak_month": best["Month"]}

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--monthly", type=Path, default=Path("reports/monthly_sales.csv"))
    parser.add_argument("--countries", type=Path, default=Path("reports/country_sales_all.csv"))
    args = parser.parse_args()
    print(json.dumps(verify(args.monthly, args.countries), indent=2))

"""Validate pipeline outputs against the independently computed Excel benchmark."""
import argparse
import json
from pathlib import Path
import pandas as pd

BENCHMARK = {
    "source_rows": 541909,
    "duplicate_rows_removed": 5268,
    "invalid_rows_excluded": 2512,
    "return_or_cancellation_rows_excluded": 9251,
    "sales_rows": 524878,
    "gross_sales": 10642110.80,
    "orders": 19960,
    "identified_customers": 4338,
    "repeat_customers": 2845,
    "unidentified_sales_rows": 132186,
}
PEAK_MONTH = "2011-11"
PEAK_REVENUE = 1503866.78

def validate(directory: Path):
    summary = json.loads((directory / "summary.json").read_text())
    failures = []
    for key, expected in BENCHMARK.items():
        actual = summary.get(key)
        if isinstance(expected, float):
            ok = actual is not None and abs(float(actual) - expected) < 0.01
        else:
            ok = actual == expected
        if not ok:
            failures.append(f"{key}: expected {expected}, got {actual!r}")
    monthly = pd.read_csv(directory / "monthly_sales.csv")
    total = monthly["Revenue"].sum()
    if abs(float(total) - BENCHMARK["gross_sales"]) >= .01:
        failures.append(f"monthly sum: expected {BENCHMARK['gross_sales']}, got {total}")
    highest = monthly.loc[monthly["Revenue"].idxmax()]
    if str(highest["Month"]) != PEAK_MONTH or abs(float(highest["Revenue"]) - PEAK_REVENUE) >= .01:
        failures.append(f"peak month mismatch: got {highest['Month']} {highest['Revenue']}")
    return failures

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Compare generated outputs to the independently computed workbook benchmark")
    parser.add_argument("--input", type=Path, default=Path("outputs"))
    args = parser.parse_args()
    errors = validate(args.input)
    if errors:
        print("VALIDATION FAILED")
        for error in errors:
            print(" -", error)
        raise SystemExit(1)
    print("PASS: all benchmark checks match")

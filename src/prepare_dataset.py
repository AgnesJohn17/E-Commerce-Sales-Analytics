"""Download and convert the UCI Online Retail dataset to CSV.

Run: python src/prepare_dataset.py
Requires internet access, pandas and openpyxl.
"""
import argparse
from pathlib import Path
from urllib.request import Request, urlopen
from zipfile import ZipFile
from io import BytesIO
import pandas as pd

URL = "https://archive.ics.uci.edu/static/public/352/online%2Bretail.zip"
COLUMNS = ["InvoiceNo", "StockCode", "Description", "Quantity", "InvoiceDate", "UnitPrice", "CustomerID", "Country"]

def prepare(source: Path | None, destination: Path) -> int:
    if source:
        workbook = source
    else:
        print("Downloading the UCI Online Retail archive...")
        req = Request(URL, headers={"User-Agent": "Mozilla/5.0"})
        with urlopen(req, timeout=90) as response:
            archive = response.read()
        with ZipFile(BytesIO(archive)) as zipped:
            names = [name for name in zipped.namelist() if name.lower().endswith(".xlsx")]
            if not names:
                raise ValueError("No XLSX file in the downloaded archive")
            workbook = BytesIO(zipped.read(names[0]))
    frame = pd.read_excel(workbook, dtype={"InvoiceNo": "string", "StockCode": "string", "CustomerID": "string"}, engine="openpyxl")
    missing = set(COLUMNS) - set(frame.columns)
    if missing:
        raise ValueError(f"Dataset is missing columns: {sorted(missing)}")
    destination.parent.mkdir(parents=True, exist_ok=True)
    frame.to_csv(destination, index=False)
    print(f"Prepared {len(frame):,} rows at {destination}")
    return len(frame)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, help="Optional local XLSX file to avoid downloading")
    parser.add_argument("--output", type=Path, default=Path("data/online_retail.csv"))
    args = parser.parse_args()
    prepare(args.source, args.output)

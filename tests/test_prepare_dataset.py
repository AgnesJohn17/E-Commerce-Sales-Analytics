import sys
from pathlib import Path
import tempfile
import unittest
import pandas as pd
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from prepare_dataset import prepare

class TestPrepareDataset(unittest.TestCase):
    def test_local_excel_conversion(self):
        with tempfile.TemporaryDirectory() as folder:
            source = Path(folder) / "source.xlsx"
            target = Path(folder) / "clean.csv"
            pd.DataFrame({
                "InvoiceNo": ["000001"],
                "StockCode": ["A1"],
                "Description": ["Item"],
                "Quantity": [2],
                "InvoiceDate": ["2011-01-01"],
                "UnitPrice": [5.0],
                "CustomerID": ["00027"],
                "Country": ["United Kingdom"],
            }).to_excel(source, index=False)
            count = prepare(source, target)
            self.assertEqual(count, 1)
            result = pd.read_csv(target, dtype={"InvoiceNo":"string","CustomerID":"string"})
            self.assertEqual(result.loc[0, "InvoiceNo"], "000001")
            self.assertEqual(result.loc[0, "CustomerID"], "00027")

if __name__ == "__main__":
    unittest.main()

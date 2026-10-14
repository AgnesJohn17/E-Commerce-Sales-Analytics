import sys
from pathlib import Path
import unittest
import pandas as pd
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from analyze import analyze

class TestAnalyze(unittest.TestCase):
    def test_revenue_and_cancellations(self):
        rows = [
            ["100","SKU1","Item",2,"2011-01-01",10,"7","UK"],
            ["101","SKU2","Other",1,"2011-01-03",5,"7","UK"],
            ["C102","SKU1","Item",-1,"2011-01-04",10,"7","UK"],
            ["103","SKU1","Item",1,"2011-01-05",0,None,"UK"],
        ]
        df = pd.DataFrame(rows,columns=["InvoiceNo","StockCode","Description","Quantity","InvoiceDate","UnitPrice","CustomerID","Country"])
        sales, monthly, products, countries, customers, summary = analyze(df)
        self.assertEqual(summary["gross_sales"],25.0)
        self.assertEqual(summary["orders"],2)
        self.assertEqual(summary["return_or_cancellation_rows_excluded"],1)
        self.assertEqual(summary["invalid_rows_excluded"],1)
        self.assertEqual(summary["repeat_customers"],1)
        self.assertEqual(len(monthly),1)
    def test_missing_columns(self):
        with self.assertRaises(ValueError):
            analyze(pd.DataFrame({"InvoiceNo":["1"]}))

if __name__ == "__main__":
    unittest.main()

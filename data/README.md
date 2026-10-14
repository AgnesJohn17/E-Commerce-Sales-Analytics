# Data source

Download **Online Retail** from the [UCI Machine Learning Repository](https://archive.ics.uci.edu/dataset/352/online+retail). Convert `Online Retail.xlsx` to `data/online_retail.csv`, retaining original column headings. Raw customer transaction data is not committed. Required columns: InvoiceNo, StockCode, Description, Quantity, InvoiceDate, UnitPrice, CustomerID, Country.

Example conversion after `pip install openpyxl`:

```python
import pandas as pd
pd.read_excel('Online Retail.xlsx', dtype={'InvoiceNo':'string','StockCode':'string','CustomerID':'string'}).to_csv('data/online_retail.csv', index=False)
```

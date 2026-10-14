# Validation checklist

- [x] Unit tests for basic sales calculations and missing required columns passed locally (2026-10-14).
- [ ] Download the original UCI Online Retail dataset and convert XLSX to CSV.
- [ ] Run the pipeline against the full original dataset and reconcile KPI figures.
- [ ] Produce and inspect figures from `src/visualize.py`.
- [ ] Reconcile SQL queries against the Python output.
- [ ] Build an actual Power BI PBIX dashboard.
- [ ] Add results, findings, screenshots, and precise resume bullets.

Commands:

```bash
pip install -r requirements.txt
python -m unittest discover -s tests -v
python src/analyze.py --input data/online_retail.csv --output outputs
python src/visualize.py --input outputs --output outputs/charts
```

**Do not commit private customer records or generated files containing customer identifiers.**

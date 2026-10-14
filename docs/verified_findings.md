# Verified analysis — UCI Online Retail dataset

**Source:** UCI Online Retail workbook supplied for analysis (541,909 original rows, 2010-12-01 through 2011-12-09). Analyzed directly from Excel on 2026-10-14 to avoid an intermediate CSV conversion integrity issue.

## Sales KPI results
| Metric | Result |
|---|---:|
| Original transaction lines | 541,909 |
| Exact duplicate rows excluded | 5,268 |
| Invalid lines excluded (missing required fields, nonpositive price, or invalid date) | 2,512 |
| Cancellation/return lines excluded after other invalid exclusions | 9,251 |
| Positive sales lines retained | 524,878 |
| Gross positive sales | **£10,642,110.80** |
| Distinct sales orders | **19,960** |
| Identified customers | **4,338** |
| Identified repeat customers (>1 invoice) | **2,845** |
| Sales lines missing CustomerID | **132,186** |
| Highest revenue month | **November 2011 (£1,503,866.78)** |
| UK share of gross positive sales | **84.586%** |

**Important:** Gross positive sales excludes credit notes and negative quantities; it is **not net revenue**, and no tax/shipping adjustments are made. Customer analyses exclude unidentified customers; their sales remain in revenue. December 2011 includes only nine days, so it should **not** be compared as a full month.

## Analytical observations
- November 2011 has the highest observed monthly gross positive sales.
- UK transactions dominate observed sales (~84.6%).
- Among 4,338 customers identifiable by ID, 2,845 made purchases across more than one invoice (65.58%). This proportion describes *identified customers*, not all customers.

## Data reproducibility
Download the original dataset from https://archive.ics.uci.edu/dataset/352/online+retail and run:
```bash
python src/prepare_dataset.py
python src/analyze.py --input data/online_retail.csv --output outputs
python src/visualize.py --input outputs --output outputs/charts
```
Outputs should be validated against the KPI table above. The numbers above were computed directly from the XLSX (including de-duplication, date conversion, and consistent positive-sales exclusions). Generated files are excluded from source control, and customer-level exports are **not** published.

## Remaining work
- Validate standard importer/analysis pipeline against this Excel-based benchmark.
- Run and review visualization images and SQL totals.
- Create an actual interactive Power BI report and screenshots.

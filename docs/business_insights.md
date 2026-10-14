# Business insights from historical Online Retail transactions

**Source period:** December 2010 to December 2011 (December 2011 ends December 9).

### Findings
1. **Seasonal peak:** November 2011 achieved the highest observed monthly gross positive sales, **£1,503,866.78**. It is 30.6% above October 2011 (£1,151,263.73), suggesting a strong holiday-season ramp. The historical dataset does not establish causality.
2. **Geographic concentration:** The United Kingdom accounted for **£9,001,744.09**, **84.586%** of gross positive sales. The next largest countries were the Netherlands (£285,446.34), EIRE (£283,140.52), and Germany (£228,678.40).
3. **Repeat purchasing:** Of 4,338 identifiable customers, 2,845 (**65.58%**) made purchases in more than one distinct invoice. Customers without IDs cannot be classified.
4. **Product categories need cleaning:** Some top StockCodes represent postage or manual accounting entries (such as DOT, POST and M), not merchandise. Filter or classify them before making product-merchandising recommendations.

### Business recommendations to investigate
- Plan stock and fulfillment capacity ahead of the observed autumn/November sales peak; confirm with more years before forecasting.
- Investigate demand from non-UK markets, but evaluate shipping costs and margins before prioritizing geographic expansion.
- Explore retention strategies and cohort behavior; the repeat-customer statistic is descriptive and **not** a measured retention lift.

### Charts
- [Monthly gross sales](../reports/charts/monthly_sales.svg)
- [Top countries](../reports/charts/country_sales.svg)

**Limitations:** Gross positive sales exclude returns and cancellations but do not subtract returns from original sales. They are not net recognized revenue. Shipping, discounts and tax are not separately modeled. Partial December 2011 is not a full-month comparison. No causal effect or business outcome is claimed.

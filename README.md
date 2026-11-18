# FY27 FP&A Variance Analysis – Renewable Energy

An Excel FP&A model for **ABC Renewables Ltd**, a *fictional* solar module manufacturer and EPC company. It works through the monthly MIS cycle a business-finance team runs: budget vs actual vs forecast, variance drivers, project and cost-centre control, working capital and a capex business case.

> All data are synthetic, built for practice. Amounts are in ₹ crore.

## Business questions it answers

1. **How did H1 (Apr–Sep 2026) perform against budget, and why?** P&L by business line, plus an EBITDA bridge split into volume, price, variable-cost and fixed-cost effects.
2. **Where will the full year land?** A Latest Estimate built from H1 actuals plus an H2 forecast.
3. **Which EPC projects are losing margin?** Budget vs estimate-at-completion (EAC) gross margin, with automatic review flags.
4. **Which cost centres are overspending?** Budget vs actual by owner function (Manufacturing, Projects, Supply Chain, Sales, Finance).
5. **How much cash is stuck in working capital?** DSO, DIO, DPO, net working capital and the cash conversion cycle.
6. **Should we invest in a new 500 MW module line?** 10-year free cash flow, NPV, IRR and payback.

## Key findings (base case)

| Metric | H1 Budget | H1 Actual | Variance |
|---|---|---|---|
| Revenue (₹ Cr) | 1,614.5 | 1,540.7 | (73.8) |
| Contribution margin | 15.8% | 14.2% | (1.6 pp) |
| EBITDA (₹ Cr) | 90.7 | 50.3 | (40.4) |
| EBITDA margin | 5.6% | 3.3% | (2.4 pp) |
| Cash conversion cycle (days) | 60 | 82 | 22 days worse |

- **Module price erosion was the main driver:** it cost ₹58.5 Cr of EBITDA. Lower cell and wafer input costs recovered ₹21.4 Cr of that.
- **Volume netted to about zero:** module volume was 36 MW above budget, but EPC was 19 MW behind because of execution delays.
- **2 of 8 EPC projects are flagged** for gross-margin erosion above 2 pp, with ₹17.5 Cr of cost overrun between them.
- **3 of 5 cost centres overspent** by more than 5%.
- **Working capital ties up an extra ₹147 Cr** versus budget. DSO is up 13 days, and each 1-day cut in DSO would release about ₹8.4 Cr.
- **FY27 Latest Estimate:** EBITDA of ₹159.5 Cr against a ₹270 Cr budget.
- **Capex case:** NPV ₹50.3 Cr at 11% WACC, IRR 14.4%, payback 5.2 years, so the recommendation is to accept.

## Workbook structure

| Sheet | Contents |
|---|---|
| Dashboard | KPI summary with charts |
| Assumptions | All inputs (blue): prices, unit costs, volumes, seasonality, fixed costs, working-capital days, capex case |
| Volumes | Monthly volume and revenue: Budget, Actual, Latest Estimate |
| PnL | Revenue → contribution → gross profit → EBITDA; H1 BvA and FY Budget vs LE |
| Variance_Bridge | H1 EBITDA bridge (volume / price / variable cost / fixed cost), reconciled to the P&L |
| Projects | EPC project profitability, EAC and margin-erosion flags |
| Cost_Centres | Cost-centre budget vs actual and overspend flags |
| Working_Capital | DSO, DIO, DPO, NWC and cash conversion cycle |
| Capex_Case | NPV, IRR and payback for a new production line |

## How to use it

- Change any **blue** input on the `Assumptions` sheet (prices, volumes, cost per MW, DSO, WACC). Every downstream number recalculates, because there are no hardcoded results.
- Two built-in **checks** (`Variance_Bridge` K8 and B17) must equal 0. They confirm that the bridge ties back to the P&L.
- Colour code: blue = input, black = formula, green = link to another sheet, yellow fill = key assumption.

## Concepts covered

Budgeting and forecasting · variance analysis (price/volume/cost) · contribution and gross margin · EBITDA · cost-centre control · project profitability (EAC) · working capital (DSO/DIO/DPO, CCC) · capex appraisal (NPV, IRR, payback) · MIS dashboards in Excel

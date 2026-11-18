"""Regenerate the README charts from the Excel model.

Reads the values Excel last calculated (open the workbook in Excel and save it
after changing any input), then writes PNG charts to ../images/.

Usage:
    pip install -r requirements.txt
    python make_charts.py
"""
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
from openpyxl import load_workbook

ROOT = Path(__file__).resolve().parent.parent
MODEL = ROOT / "FY27_FPA_Variance_Model.xlsx"
OUT = ROOT / "images"
OUT.mkdir(exist_ok=True)

# Palette: categorical slots 1-2 (validated for colour-vision deficiency),
# diverging blue/red for favourable/unfavourable, neutral ink for totals.
BLUE, ORANGE, RED = "#2a78d6", "#eb6834", "#e34948"
INK, INK2, MUTED = "#0b0b0b", "#52514e", "#898781"
GRID, AXIS, SURFACE, NEUTRAL = "#e1e0d9", "#c3c2b7", "#fcfcfb", "#52514e"

plt.rcParams.update({
    "figure.facecolor": SURFACE, "axes.facecolor": SURFACE, "savefig.facecolor": SURFACE,
    "font.size": 10, "axes.titlesize": 13, "axes.titleweight": "bold", "axes.titlelocation": "left",
    "axes.edgecolor": AXIS, "axes.labelcolor": INK2, "xtick.color": INK2, "ytick.color": INK2,
    "text.color": INK, "axes.spines.top": False, "axes.spines.right": False,
    "axes.grid": True, "grid.color": GRID, "grid.linewidth": 0.8, "axes.axisbelow": True,
    "legend.frameon": False,
})

wb = load_workbook(MODEL, data_only=True)


def val(sheet, ref):
    v = wb[sheet][ref].value
    if v is None:
        raise SystemExit(f"{sheet}!{ref} has no cached value - open the model in Excel, save it, then re-run.")
    return v


def row(sheet, row_no, first_col, last_col):
    ws = wb[sheet]
    return [ws.cell(row=row_no, column=c).value for c in range(first_col, last_col + 1)]


cr = FuncFormatter(lambda x, _: f"{x:,.0f}")


def subtitle(ax, text):
    ax.text(0, 1.02, text, transform=ax.transAxes, color=INK2, fontsize=9.5, va="bottom")


def save(fig, name):
    fig.savefig(OUT / name, dpi=200, bbox_inches="tight")
    plt.close(fig)
    print("wrote", OUT / name)


# 1. Monthly revenue: budget vs latest estimate -------------------------------
months = row("Volumes", 3, 3, 14)
budget = row("Volumes", 19, 3, 14)
le = row("Volumes", 24, 3, 14)
fig, ax = plt.subplots(figsize=(9, 4.2))
ax.axvspan(-0.5, 5.5, color="#f0efec", zorder=0)
ax.text(2.5, max(budget) * 1.06, "Actual (Apr–Sep)", ha="center", color=INK2, fontsize=9)
ax.text(8.5, max(budget) * 1.06, "Forecast (Oct–Mar)", ha="center", color=INK2, fontsize=9)
ax.plot(months, budget, color=BLUE, lw=2, marker="o", ms=5, label="Budget")
ax.plot(months, le, color=ORANGE, lw=2, marker="o", ms=5, label="Latest estimate")
ax.annotate(f"Budget {budget[-1]:,.0f}", (11, budget[-1]), xytext=(6, 0), textcoords="offset points", va="center", color=INK2, fontsize=9)
ax.annotate(f"LE {le[-1]:,.0f}", (11, le[-1]), xytext=(6, -2), textcoords="offset points", va="center", color=INK2, fontsize=9)
ax.set_ylim(0, max(budget) * 1.15)
ax.yaxis.set_major_formatter(cr)
ax.set_ylabel("Revenue (INR Cr)")
ax.set_title("Monthly revenue: budget vs latest estimate", pad=22)
fy_b, fy_le = val("PnL", "G9"), val("PnL", "H9")
subtitle(ax, f"FY27 revenue: INR {fy_le:,.0f} Cr latest estimate vs INR {fy_b:,.0f} Cr budget ({(fy_le - fy_b) / fy_b:+.1%})")
ax.legend(loc="lower right", ncol=2)
save(fig, "01_revenue_budget_vs_le.png")

# 2. H1 EBITDA bridge (waterfall) ----------------------------------------------
labels = [wb["Variance_Bridge"][f"A{r}"].value for r in range(11, 17)]
vals = [val("Variance_Bridge", f"B{r}") for r in range(11, 17)]
fig, ax = plt.subplots(figsize=(9, 4.4))
running = vals[0]
for i, (lab, v) in enumerate(zip(labels, vals)):
    if i == 0 or i == len(vals) - 1:
        ax.bar(i, v, color=NEUTRAL, width=0.6)
        ax.text(i, v + 2, f"{v:,.1f}", ha="center", va="bottom", fontsize=10, fontweight="bold")
        continue
    bottom = running if v >= 0 else running + v
    ax.bar(i, abs(v), bottom=bottom, color=BLUE if v >= 0 else RED, width=0.6)
    y_text = running + v + 2 if v >= 0 else running + 2
    ax.text(i, y_text, f"{v:+,.1f}", ha="center", va="bottom", fontsize=10)
    ax.plot([i - 0.3, i + 0.7], [running + v] * 2, color=AXIS, lw=1, zorder=0)
    running += v
ax.plot([-0.3, 0.7], [vals[0]] * 2, color=AXIS, lw=1, zorder=0)
ax.set_xticks(range(len(labels)), [l.replace(" H1", "\nH1") for l in labels])
ax.set_ylim(0, max(vals[0], running) * 1.25)
ax.set_ylabel("INR Cr")
ax.grid(axis="x", visible=False)
ax.set_title("H1 EBITDA bridge: budget to actual", pad=22)
subtitle(ax, "Blue = favourable, red = unfavourable. Price erosion drove the gap; lower input costs recovered part of it.")
save(fig, "02_ebitda_bridge.png")

# 3. Cost-centre variance --------------------------------------------------------
names = [wb["Cost_Centres"][f"A{r}"].value for r in range(4, 9)]
var = [val("Cost_Centres", f"E{r}") for r in range(4, 9)]
pct = [val("Cost_Centres", f"F{r}") for r in range(4, 9)]
order = sorted(range(5), key=lambda i: var[i])
fig, ax = plt.subplots(figsize=(9, 3.8))
for y, i in enumerate(order):
    ax.barh(y, var[i], color=BLUE if var[i] >= 0 else RED, height=0.55)
    ax.text(var[i] + (0.1 if var[i] >= 0 else -0.1), y, f"{var[i]:+,.1f} ({pct[i]:+.1%})",
            va="center", ha="left" if var[i] >= 0 else "right", fontsize=9)
ax.set_yticks(range(5), [names[i] for i in order])
ax.axvline(0, color=AXIS, lw=1)
lim = max(abs(x) for x in var) * 1.8
ax.set_xlim(-lim, lim)
ax.set_xlabel("H1 variance vs budget (INR Cr, + = underspend)")
ax.grid(axis="y", visible=False)
ax.set_title("Cost-centre control: H1 budget vs actual", pad=22)
subtitle(ax, f"{val('Cost_Centres', 'B11')} of 5 cost centres overspent by more than {val('Assumptions', 'B43'):.0%}")
save(fig, "03_cost_centre_variance.png")

# 4. EPC project margin erosion (dumbbell) -----------------------------------------
proj = [wb["Projects"][f"A{r}"].value for r in range(4, 12)]
state = [wb["Projects"][f"B{r}"].value for r in range(4, 12)]
bgm = [val("Projects", f"I{r}") for r in range(4, 12)]
fgm = [val("Projects", f"J{r}") for r in range(4, 12)]
status = [wb["Projects"][f"M{r}"].value for r in range(4, 12)]
fig, ax = plt.subplots(figsize=(9, 4.6))
for y in range(8):
    ax.plot([bgm[y], fgm[y]], [y, y], color=AXIS, lw=2, zorder=1)
ax.scatter(bgm, range(8), color=BLUE, s=60, zorder=2, label="Budget gross margin", edgecolor=SURFACE, linewidth=1.5)
ax.scatter(fgm, range(8), color=ORANGE, s=60, zorder=3, label="Forecast gross margin (EAC)", edgecolor=SURFACE, linewidth=1.5)
for y in range(8):
    if status[y] == "Review":
        ax.text(max(bgm[y], fgm[y]) + 0.002, y, f"Review: −{(bgm[y] - fgm[y]) * 100:.1f} pts", va="center", fontsize=9, color=RED, fontweight="bold")
ax.set_yticks(range(8), [f"{p.split()[0]} {s}" for p, s in zip(proj, state)])
ax.invert_yaxis()
ax.xaxis.set_major_formatter(FuncFormatter(lambda x, _: f"{x:.0%}"))
ax.set_xlim(min(fgm) - 0.01, max(bgm + fgm) + 0.025)
ax.set_xlabel("Gross margin %")
ax.grid(axis="y", visible=False)
ax.legend(loc="lower center", bbox_to_anchor=(0.5, -0.32), ncol=2)
ax.set_title("EPC project profitability: budget vs estimate at completion", pad=22)
subtitle(ax, f"{val('Projects', 'B14')} of 8 projects lose more than {val('Assumptions', 'B42') * 100:.0f} pts of margin; "
             f"INR {val('Projects', 'B15'):,.1f} Cr cost overrun on them")
save(fig, "04_project_margins.png")

# 5. Working-capital days --------------------------------------------------------
metrics = ["DSO", "DIO", "DPO", "Cash conversion\ncycle"]
bud = [val("Working_Capital", r) for r in ("B7", "B8", "B9", "B15")]
act = [val("Working_Capital", r) for r in ("C7", "C8", "C9", "C15")]
x = range(4)
fig, ax = plt.subplots(figsize=(9, 4))
w = 0.36
ax.bar([i - w / 2 - 0.01 for i in x], bud, width=w, color=BLUE, label="Budget")
ax.bar([i + w / 2 + 0.01 for i in x], act, width=w, color=ORANGE, label="Actual H1")
for i in x:
    ax.text(i - w / 2 - 0.01, bud[i] + 1, f"{bud[i]:.0f}", ha="center", va="bottom", fontsize=9)
    ax.text(i + w / 2 + 0.01, act[i] + 1, f"{act[i]:.0f}", ha="center", va="bottom", fontsize=9)
ax.set_xticks(list(x), metrics)
ax.set_ylabel("Days")
ax.set_ylim(0, max(bud + act) * 1.3)
ax.grid(axis="x", visible=False)
ax.legend(loc="upper center", ncol=2)
ax.set_title("Working capital: budget vs actual (days)", pad=22)
subtitle(ax, f"Cash conversion cycle {act[3] - bud[3]:+.0f} days vs budget: INR {val('Working_Capital', 'B17'):,.0f} Cr extra cash tied up")
save(fig, "05_working_capital_days.png")

# 6. Capex case: cumulative free cash flow -----------------------------------------
years = row("Capex_Case", 4, 2, 12)
cum = row("Capex_Case", 13, 2, 12)
fcf = row("Capex_Case", 12, 2, 12)
payback = val("Capex_Case", "B20")
fig, ax = plt.subplots(figsize=(9, 4))
ax.bar(years, fcf, color=[RED if f < 0 else BLUE for f in fcf], width=0.55, alpha=0.35, label="Annual free cash flow")
ax.plot(years, cum, color=BLUE, lw=2, marker="o", ms=5, label="Cumulative free cash flow")
ax.axhline(0, color=AXIS, lw=1)
if isinstance(payback, (int, float)):
    ax.axvline(payback, color=INK2, lw=1, ls="--")
    ax.text(payback + 0.1, min(cum) * 0.85, f"Payback {payback:.1f} yrs", color=INK2, fontsize=9)
ax.set_xticks(years)
ax.set_xlabel("Year")
ax.set_ylabel("INR Cr")
ax.yaxis.set_major_formatter(cr)
ax.legend(loc="upper left")
ax.set_title("Capex case: new 500 MW module line", pad=22)
subtitle(ax, f"Capex INR {val('Assumptions', 'B31'):,.0f} Cr · NPV INR {val('Capex_Case', 'B18'):,.1f} Cr at "
             f"{val('Assumptions', 'B37'):.0%} WACC · IRR {val('Capex_Case', 'B19'):.1%}")
save(fig, "06_capex_cumulative_fcf.png")

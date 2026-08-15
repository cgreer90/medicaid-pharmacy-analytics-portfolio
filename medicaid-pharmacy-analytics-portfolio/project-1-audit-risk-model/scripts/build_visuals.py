import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "axes.edgecolor": "#444444",
    "axes.labelcolor": "#222222",
    "text.color": "#222222",
    "xtick.color": "#444444",
    "ytick.color": "#444444",
    "axes.titleweight": "bold",
})

DARK_BLUE = "#1F3864"
RED = "#C0392B"
GRAY = "#9AA5B1"

df = pd.read_csv("/home/claude/mi_audit/risk_scoring_export.csv")
top30 = df.sort_values("RiskRank").head(30).copy()
top15 = top30.head(15).copy()

# ---------- Chart 1: Top 15 risk scores (bar) ----------
fig, ax = plt.subplots(figsize=(10, 6))
order = top15.sort_values("RiskScore")
bars = ax.barh(order["Product"], order["RiskScore"], color=DARK_BLUE)
ax.set_title("Top 15 Highest-Risk Products — Michigan Medicaid, FY2024")
ax.set_xlabel("Composite Risk Score (Cost Z-Score + Utilization Volatility Z-Score)")
ax.spines[["top", "right"]].set_visible(False)
for b in bars:
    ax.text(b.get_width() + 0.05, b.get_y() + b.get_height() / 2, f"{b.get_width():.2f}",
            va="center", fontsize=9, color="#222222")
fig.tight_layout()
fig.savefig("/home/claude/mi_audit/visuals/01_top15_risk_scores.png", dpi=150)
plt.close(fig)

# ---------- Chart 2: Risk quadrant scatter ----------
fig, ax = plt.subplots(figsize=(10, 7))
flagged = df["RiskRank"] <= 30
sizes = (df["TotalAmt"] / df["TotalAmt"].max()) * 1200 + 20
ax.scatter(df.loc[~flagged, "TotalRx"], df.loc[~flagged, "AvgCostRx"],
           s=sizes[~flagged], color=GRAY, alpha=0.5, edgecolor="white", linewidth=0.5, label="Not flagged")
ax.scatter(df.loc[flagged, "TotalRx"], df.loc[flagged, "AvgCostRx"],
           s=sizes[flagged], color=RED, alpha=0.75, edgecolor="white", linewidth=0.6, label="Flagged (Top 30 risk)")
ax.set_yscale("log")
ax.set_xlabel("Total Prescriptions (FY2024)")
ax.set_ylabel("Avg Cost per Prescription ($, log scale)")
ax.set_title("Cost vs. Volume — Bubble Size = Total $ Reimbursed")
ax.spines[["top", "right"]].set_visible(False)
ax.legend(loc="upper right", frameon=False)
# annotate a few notable points
for _, row in top15.head(6).iterrows():
    ax.annotate(row["Product"], (row["TotalRx"], row["AvgCostRx"]),
                textcoords="offset points", xytext=(6, 6), fontsize=8, color="#222222")
fig.tight_layout()
fig.savefig("/home/claude/mi_audit/visuals/02_risk_quadrant_scatter.png", dpi=150)
plt.close(fig)

# ---------- Chart 3: Quarterly utilization trend for top volatility drugs ----------
vol_drivers = df.sort_values("VolZ", ascending=False).head(5)
fig, ax = plt.subplots(figsize=(10, 6))
colors = [DARK_BLUE, RED, "#2E86AB", "#E67E22", "#6C757D"]
for i, (_, row) in enumerate(vol_drivers.iterrows()):
    quarters = [row["Q1"], row["Q2"], row["Q3"], row["Q4"]]
    ax.plot(["Q1", "Q2", "Q3", "Q4"], quarters, marker="o", linewidth=2.2, color=colors[i], label=row["Product"])
ax.set_title("Quarterly Prescription Volume — Top 5 Utilization-Volatility Drivers")
ax.set_ylabel("Prescriptions per Quarter")
ax.spines[["top", "right"]].set_visible(False)
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x:,.0f}"))
ax.legend(loc="best", frameon=False, fontsize=9)
fig.tight_layout()
fig.savefig("/home/claude/mi_audit/visuals/03_quarterly_volatility_trend.png", dpi=150)
plt.close(fig)

# ---------- Chart 4: Distribution of cost-per-Rx with outlier threshold ----------
fig, ax = plt.subplots(figsize=(10, 6))
ax.hist(df["AvgCostRx"], bins=40, color=DARK_BLUE, alpha=0.85, edgecolor="white")
q1, q3 = df["AvgCostRx"].quantile([0.25, 0.75])
iqr = q3 - q1
threshold = q3 + 1.5 * iqr
ax.axvline(threshold, color=RED, linestyle="--", linewidth=2, label=f"Outlier threshold (Q3 + 1.5×IQR = ${threshold:,.0f})")
ax.set_title("Distribution of Avg Cost per Prescription — 200-Product Audit Universe")
ax.set_xlabel("Avg Cost per Prescription ($)")
ax.set_ylabel("Number of Products")
ax.spines[["top", "right"]].set_visible(False)
ax.legend(loc="upper right", frameon=False)
fig.tight_layout()
fig.savefig("/home/claude/mi_audit/visuals/04_cost_distribution.png", dpi=150)
plt.close(fig)

print("All 4 charts saved.")

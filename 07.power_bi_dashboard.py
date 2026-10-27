"""
NAAN MUDHALVAN - NM1130 AI AND DIGITAL SKILLS
EX.NO: 7  |  Power BI
------------------------------------------------------------------
Department  : CSE (AI & ML)
College     : University College of Engineering (BIT Campus), Anna University, Tiruchirappalli

Aim
---
To follow the same working mechanism as Power BI, but using Python:

    1. Collect data from a source        (Power BI: Get Data)
    2. Clean and transform the data      (Power BI: Power Query)
    3. Calculate measures / KPIs         (Power BI: DAX)
    4. Visualise as an interactive-style dashboard  (Power BI: Report view)
    5. Export the cleaned data so that it can be loaded into Power BI Desktop

Output files (created next to this script)
-------------------------------------------
    sales_raw.csv          - messy source data
    sales_clean.csv        - cleaned data (import this into Power BI Desktop)
    sales_dashboard.png    - the dashboard image

Libraries : pandas, numpy, matplotlib
Run       : python power_bi_dashboard.py
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")  # draw to a file, so it works without a display
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

HERE = Path(__file__).parent
RNG = np.random.default_rng(2026)


def heading(title: str) -> None:
    print("\n" + "=" * 64)
    print(title)
    print("=" * 64)


# ---------------------------------------------------------------------------
# STEP 1 - COLLECT DATA  (we create a realistic, slightly messy sales file)
# ---------------------------------------------------------------------------
def create_raw_data(rows: int = 400) -> pd.DataFrame:
    dates = pd.to_datetime("2025-01-01") + pd.to_timedelta(RNG.integers(0, 365, rows), unit="D")
    category = RNG.choice(["Electronics", "Clothing", "Groceries", "Furniture"], rows, p=[0.3, 0.3, 0.25, 0.15])
    region = RNG.choice(["North", "South", "East", "West"], rows)
    units = RNG.integers(1, 20, rows)
    price = pd.Series(category).map({"Electronics": 9000, "Clothing": 1500, "Groceries": 400, "Furniture": 12000})
    unit_price = (price * RNG.uniform(0.9, 1.1, rows)).round(2)
    cost_ratio = pd.Series(category).map({"Electronics": 0.78, "Clothing": 0.55, "Groceries": 0.85, "Furniture": 0.65})

    df = pd.DataFrame({
        "OrderDate": dates.strftime("%Y-%m-%d"),
        "Region": region,
        "Category": category,
        "Units": units,
        "UnitPrice": unit_price,
        "UnitCost": (unit_price * cost_ratio).round(2),
    })

    # Add typical data-quality problems
    df.loc[RNG.choice(rows, 12, replace=False), "Units"] = np.nan            # missing values
    df.loc[RNG.choice(rows, 8, replace=False), "Region"] = " north "         # spelling / spacing issues
    df = pd.concat([df, df.sample(10, random_state=1)], ignore_index=True)   # duplicate rows
    return df


# ---------------------------------------------------------------------------
# STEP 2 - CLEAN AND TRANSFORM  (what Power Query does)
# ---------------------------------------------------------------------------
def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    before = len(df)
    df = df.drop_duplicates()                                       # remove duplicate rows
    df = df.dropna(subset=["Units"]).copy()                         # remove rows with missing units
    df["Region"] = df["Region"].str.strip().str.title()             # fix spacing and capitalisation
    df["OrderDate"] = pd.to_datetime(df["OrderDate"])               # text -> date type
    df["Units"] = df["Units"].astype(int)

    # Calculated columns
    df["Month"] = df["OrderDate"].dt.to_period("M").dt.to_timestamp()
    df["Sales"] = df["Units"] * df["UnitPrice"]
    df["Profit"] = df["Units"] * (df["UnitPrice"] - df["UnitCost"])
    print(f"  Rows before cleaning: {before} | after cleaning: {len(df)} | removed: {before - len(df)}")
    return df.reset_index(drop=True)


# ---------------------------------------------------------------------------
# STEP 3 - MEASURES / KPIs  (what DAX does)
# ---------------------------------------------------------------------------
def calculate_kpis(df: pd.DataFrame) -> dict:
    return {
        "Total Sales": df["Sales"].sum(),                                  # DAX: SUM(Sales[Sales])
        "Total Profit": df["Profit"].sum(),                                # DAX: SUM(Sales[Profit])
        "Profit Margin %": df["Profit"].sum() / df["Sales"].sum() * 100,   # DAX: DIVIDE([Profit],[Sales])
        "Orders": len(df),                                                 # DAX: COUNTROWS(Sales)
        "Average Order Value": df["Sales"].mean(),                         # DAX: AVERAGE(Sales[Sales])
        "Top Region": df.groupby("Region")["Sales"].sum().idxmax(),
        "Top Category": df.groupby("Category")["Sales"].sum().idxmax(),
    }


# ---------------------------------------------------------------------------
# STEP 4 - VISUALISE  (the dashboard)
# ---------------------------------------------------------------------------
def build_dashboard(df: pd.DataFrame, kpis: dict) -> Path:
    colors = ["#118DFF", "#12239E", "#E66C37", "#6B007B"]
    fig = plt.figure(figsize=(14, 9), facecolor="#F3F2F1")
    fig.suptitle("Sales Performance Dashboard - 2025", fontsize=20, fontweight="bold", y=0.98)

    # KPI cards across the top
    cards = [
        ("Total Sales", f"Rs.{kpis['Total Sales'] / 1e6:.2f} M"),
        ("Total Profit", f"Rs.{kpis['Total Profit'] / 1e6:.2f} M"),
        ("Profit Margin", f"{kpis['Profit Margin %']:.1f}%"),
        ("Orders", f"{kpis['Orders']:,}"),
    ]
    for i, (label, value) in enumerate(cards):
        ax = fig.add_axes([0.05 + i * 0.235, 0.82, 0.21, 0.09], facecolor="white")
        ax.set_xticks([]); ax.set_yticks([])
        ax.text(0.5, 0.62, value, ha="center", va="center", fontsize=20, fontweight="bold", color="#12239E")
        ax.text(0.5, 0.18, label, ha="center", va="center", fontsize=11, color="#605E5C")

    grid = fig.add_gridspec(2, 2, left=0.06, right=0.97, top=0.76, bottom=0.07, hspace=0.38, wspace=0.22)

    # 1. Line chart - monthly trend
    ax1 = fig.add_subplot(grid[0, 0])
    monthly = df.groupby("Month")["Sales"].sum() / 1e3
    ax1.plot(monthly.index, monthly.values, marker="o", color=colors[0], linewidth=2)
    ax1.set_title("Monthly Sales Trend (Rs. thousands)", fontweight="bold")
    ax1.tick_params(axis="x", rotation=45)

    # 2. Bar chart - sales by region
    ax2 = fig.add_subplot(grid[0, 1])
    by_region = (df.groupby("Region")["Sales"].sum() / 1e3).sort_values(ascending=False)
    ax2.bar(by_region.index, by_region.values, color=colors[1])
    ax2.set_title("Sales by Region (Rs. thousands)", fontweight="bold")

    # 3. Donut chart - category share
    ax3 = fig.add_subplot(grid[1, 0])
    by_cat = df.groupby("Category")["Sales"].sum()
    ax3.pie(by_cat.values, labels=by_cat.index, autopct=lambda pct: f"{pct:.0f}%" if pct >= 5 else "", pctdistance=0.78, colors=colors,
            startangle=90, wedgeprops={"width": 0.45, "edgecolor": "white"})
    ax3.set_title("Sales Share by Category", fontweight="bold")

    # 4. Grouped bar - profit by category and region
    ax4 = fig.add_subplot(grid[1, 1])
    pivot = df.pivot_table(index="Category", columns="Region", values="Profit", aggfunc="sum") / 1e3
    pivot.plot(kind="bar", ax=ax4, color=colors, width=0.8)
    ax4.set_title("Profit by Category and Region (Rs. thousands)", fontweight="bold")
    ax4.set_xlabel("")
    ax4.tick_params(axis="x", rotation=0)
    ax4.legend(title="Region", fontsize=8)

    for ax in (ax1, ax2, ax4):
        ax.spines[["top", "right"]].set_visible(False)

    out = HERE / "sales_dashboard.png"
    fig.savefig(out, dpi=150)
    plt.close(fig)
    return out


def main() -> None:
    print("NM1130 - EX.NO: 7 - POWER BI STYLE DASHBOARD (Python)")

    heading("STEP 1: COLLECT DATA  (Get Data)")
    raw = create_raw_data()
    raw.to_csv(HERE / "sales_raw.csv", index=False)
    print(f"  Loaded {len(raw)} rows. Missing values: {int(raw['Units'].isna().sum())}, "
          f"duplicates: {int(raw.duplicated().sum())}")

    heading("STEP 2: CLEAN AND TRANSFORM  (Power Query)")
    df = clean_data(raw)
    df.to_csv(HERE / "sales_clean.csv", index=False)
    print("  Saved sales_clean.csv  <- import this file in Power BI Desktop")

    heading("STEP 3: CALCULATE KPIs  (DAX measures)")
    kpis = calculate_kpis(df)
    for name, value in kpis.items():
        shown = f"{value:,.2f}" if isinstance(value, float) else value
        print(f"  {name:<22}: {shown}")

    heading("STEP 4: BUILD THE DASHBOARD  (Report view)")
    out = build_dashboard(df, kpis)
    print(f"  Dashboard saved as {out.name}")

    print("\nResult: Raw data converted into insights using the Power BI workflow.")


if __name__ == "__main__":
    main()

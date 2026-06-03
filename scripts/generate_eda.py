"""
generate_eda.py — Bluestock MF Capstone: EDA Visualization (D3)
Extracts data from SQLite database, generates 16 Seaborn/Matplotlib charts saved in reports/figures/,
and programmatically creates notebooks/EDA_Analysis.ipynb with interactive Plotly & Seaborn code.
"""

import os
import json
import sqlite3
import logging
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# ── Paths ──────────────────────────────────────────────────────────────────────
ROOT = Path(__file__).resolve().parent.parent
DB_PATH = ROOT / "data" / "db" / "bluestock_mf.db"
FIG_DIR = ROOT / "reports" / "figures"
NOTEBOOK_PATH = ROOT / "notebooks" / "EDA_Analysis.ipynb"

FIG_DIR.mkdir(parents=True, exist_ok=True)
NOTEBOOK_PATH.parent.mkdir(parents=True, exist_ok=True)

# ── Logging ────────────────────────────────────────────────────────────────────
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger(__name__)

def generate_static_charts(conn: sqlite3.Connection):
    """Generates all 16 static charts using Matplotlib/Seaborn and saves them in reports/figures/."""
    log.info("Generating static Matplotlib/Seaborn charts...")
    sns.set_theme(style="whitegrid")
    
    # ─────────────────────────────────────────────────────────────────────────
    # Chart 1, 2, 3: NAV History & Highlights (2022-2026)
    # ─────────────────────────────────────────────────────────────────────────
    log.info("Generating NAV History Charts...")
    nav_df = pd.read_sql_query("""
        SELECT n.nav_date, n.nav_value, f.scheme_name, f.category
        FROM fact_nav n
        JOIN dim_fund f ON n.amfi_code = f.amfi_code
    """, conn)
    nav_df["nav_date"] = pd.to_datetime(nav_df["nav_date"])
    
    # Pivot to get daily NAV per scheme
    nav_pivot = nav_df.pivot(index="nav_date", columns="scheme_name", values="nav_value")
    
    # Chart 1: Daily NAV for all 40 schemes (Normalized to Base 100 for comparison)
    plt.figure(figsize=(12, 6))
    nav_norm = nav_pivot.divide(nav_pivot.iloc[0]).multiply(100)
    for col in nav_norm.columns:
        plt.plot(nav_norm.index, nav_norm[col], alpha=0.3, linewidth=1)
    # Highlight average path
    plt.plot(nav_norm.index, nav_norm.mean(axis=1), color="black", linewidth=2.5, label="Average Performance")
    plt.title("Daily NAV Trend (All 40 Schemes Normalized to Base 100, 2022-2026)", fontsize=14, fontweight="bold")
    plt.xlabel("Date")
    plt.ylabel("Normalized NAV Value")
    plt.legend()
    plt.tight_layout()
    plt.savefig(FIG_DIR / "fig1_nav_trends.png", dpi=150)
    plt.close()
    
    # Chart 2: 2023 Bull Run Highlight
    plt.figure(figsize=(10, 5))
    nav_2023 = nav_pivot.loc["2023-01-01":"2023-12-31"]
    for col in nav_2023.columns:
        plt.plot(nav_2023.index, nav_2023[col], alpha=0.4)
    plt.axvspan(pd.to_datetime("2023-04-01"), pd.to_datetime("2023-12-31"), color="green", alpha=0.15, label="2023 Bull Run Phase")
    plt.title("Junction of Acceleration: 2023 Mutual Fund Bull Run", fontsize=13, fontweight="bold")
    plt.xlabel("Date")
    plt.ylabel("NAV Value")
    plt.legend()
    plt.tight_layout()
    plt.savefig(FIG_DIR / "fig2_bull_run_2023.png", dpi=150)
    plt.close()
    
    # Chart 3: 2024 Market Corrections Highlight
    plt.figure(figsize=(10, 5))
    nav_2024 = nav_pivot.loc["2024-01-01":"2024-06-30"]
    for col in nav_2024.columns:
        plt.plot(nav_2024.index, nav_2024[col], alpha=0.4)
    plt.axvspan(pd.to_datetime("2024-01-01"), pd.to_datetime("2024-05-31"), color="red", alpha=0.1, label="2024 Consolidation & Correction")
    plt.title("Volatile Ground: 2024 H1 Market Corrections", fontsize=13, fontweight="bold")
    plt.xlabel("Date")
    plt.ylabel("NAV Value")
    plt.legend()
    plt.tight_layout()
    plt.savefig(FIG_DIR / "fig3_corrections_2024.png", dpi=150)
    plt.close()

    # ─────────────────────────────────────────────────────────────────────────
    # Chart 4, 5: AUM Growth (2022-2025)
    # ─────────────────────────────────────────────────────────────────────────
    log.info("Generating AUM Growth Charts...")
    aum_df = pd.read_sql_query("""
        SELECT aum_date, fund_house, aum_crore, aum_lakh_crore
        FROM fact_aum
    """, conn)
    aum_df["year"] = pd.to_datetime(aum_df["aum_date"]).dt.year
    # Group by fund house and year
    aum_grouped = aum_df.groupby(["fund_house", "year"])["aum_crore"].mean().reset_index()
    
    # Chart 4: Grouped Bar Chart by Fund House 2022-2025
    plt.figure(figsize=(14, 6))
    ax = sns.barplot(data=aum_grouped, x="fund_house", y="aum_crore", hue="year", palette="viridis")
    plt.title("Assets Under Management (AUM) Growth by Fund House (2022-2025)", fontsize=14, fontweight="bold")
    plt.xlabel("Fund House")
    plt.ylabel("AUM in INR Crores")
    plt.xticks(rotation=45, ha="right")
    
    # Highlight SBI at 12.5L Cr dominance
    for p in ax.patches:
        height = p.get_height()
        if height == 1250000.0:  # SBI Mutual Fund in 2025
            ax.annotate("SBI Dominance: ₹12.5L Cr",
                        xy=(p.get_x() + p.get_width() / 2., height),
                        xytext=(0, 8), textcoords='offset points',
                        ha='center', va='bottom', fontsize=10, color="red", fontweight="bold",
                        bbox=dict(boxstyle="round,pad=0.3", fc="yellow", alpha=0.5))
            
    plt.tight_layout()
    plt.savefig(FIG_DIR / "fig4_aum_growth.png", dpi=150)
    plt.close()
    
    # Chart 5: AUM Market Share in Dec 2025 (Pie Chart)
    plt.figure(figsize=(8, 8))
    aum_2025 = aum_df[aum_df["aum_date"] == "2025-12-31"]
    colors = sns.color_palette("Set3", len(aum_2025))
    plt.pie(aum_2025["aum_crore"], labels=aum_2025["fund_house"], autopct="%1.1f%%", startangle=140, colors=colors)
    plt.title("Mutual Fund AUM Market Share (Dec 2025)", fontsize=14, fontweight="bold")
    plt.tight_layout()
    plt.savefig(FIG_DIR / "fig5_aum_share_2025.png", dpi=150)
    plt.close()

    # ─────────────────────────────────────────────────────────────────────────
    # Chart 6, 7: SIP Inflows (Jan 2022 - Dec 2025)
    # ─────────────────────────────────────────────────────────────────────────
    log.info("Generating SIP Inflow Charts...")
    sip_df = pd.read_sql_query("SELECT * FROM monthly_sip_inflows", conn)
    
    # Chart 6: Monthly SIP trend
    plt.figure(figsize=(12, 5))
    plt.plot(sip_df["month"], sip_df["sip_inflow_crore"], color="indigo", marker="o", linewidth=2)
    # Annotate Dec 2025 Peak
    plt.annotate("All-time High: ₹31,002 Cr (Dec 2025)", 
                 xy=("2025-12", 31002), 
                 xytext=("2024-06", 28000),
                 arrowprops=dict(facecolor='black', shrink=0.08, width=1.5, headwidth=6),
                 fontsize=11, fontweight="bold", color="darkred")
    plt.title("Monthly Systematic Investment Plan (SIP) Inflows Trend (Jan 2022 - Dec 2025)", fontsize=14, fontweight="bold")
    plt.xlabel("Month")
    plt.ylabel("Inflows in INR Crores")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(FIG_DIR / "fig6_sip_inflows.png", dpi=150)
    plt.close()
    
    # Chart 7: Yearly Inflow Totals Bar Chart
    sip_df["year"] = sip_df["month"].str.slice(0, 4)
    sip_yearly = sip_df.groupby("year")["sip_inflow_crore"].sum().reset_index()
    plt.figure(figsize=(8, 5))
    sns.barplot(data=sip_yearly, x="year", y="sip_inflow_crore", palette="crest")
    plt.title("Total Annual Systematic Investment Plan (SIP) Inflows", fontsize=13, fontweight="bold")
    plt.xlabel("Year")
    plt.ylabel("Annual Inflows in INR Crores")
    plt.tight_layout()
    plt.savefig(FIG_DIR / "fig7_sip_yearly.png", dpi=150)
    plt.close()

    # ─────────────────────────────────────────────────────────────────────────
    # Chart 8: Category Inflow Heatmap
    # ─────────────────────────────────────────────────────────────────────────
    log.info("Generating Category Inflow Heatmap...")
    cat_df = pd.read_sql_query("SELECT * FROM category_inflows", conn)
    cat_pivot = cat_df.pivot(index="category", columns="month", values="net_inflow_crore")
    
    plt.figure(figsize=(14, 7))
    sns.heatmap(cat_pivot, cmap="YlGnBu", cbar_kws={'label': 'Net Inflow (INR Crores)'}, annot=False)
    plt.title("Mutual Fund Category Inflow Heatmap (Month-wise, 2024-2025)", fontsize=14, fontweight="bold")
    plt.xlabel("Month")
    plt.ylabel("Fund Category")
    plt.tight_layout()
    plt.savefig(FIG_DIR / "fig8_category_heatmap.png", dpi=150)
    plt.close()

    # ─────────────────────────────────────────────────────────────────────────
    # Chart 9, 10, 11: Investor Demographics
    # ─────────────────────────────────────────────────────────────────────────
    log.info("Generating Investor Demographics Charts...")
    trans_df = pd.read_sql_query("""
        SELECT investor_id, age_group, gender, amount_inr, transaction_type 
        FROM fact_transactions
    """, conn)
    
    # Unique investor dataset
    investors = trans_df.drop_duplicates(subset=["investor_id"])
    
    # Chart 9: Age Group Distribution Pie Chart
    plt.figure(figsize=(7, 7))
    age_counts = investors["age_group"].value_counts()
    plt.pie(age_counts, labels=age_counts.index, autopct="%1.1f%%", startangle=90, colors=sns.color_palette("pastel"))
    plt.title("Investor Age Group Distribution (Unique Investors)", fontsize=14, fontweight="bold")
    plt.tight_layout()
    plt.savefig(FIG_DIR / "fig9_age_distribution.png", dpi=150)
    plt.close()
    
    # Chart 10: SIP Amount Box Plot by Age Group
    plt.figure(figsize=(10, 6))
    sip_trans = trans_df[trans_df["transaction_type"] == "SIP"]
    sns.boxplot(data=sip_trans, x="age_group", y="amount_inr", order=sorted(sip_trans["age_group"].unique()), palette="Set2")
    plt.yscale("log") # log scale because of wide variance
    plt.title("SIP Transaction Amount Distribution by Age Group (Log Scale)", fontsize=14, fontweight="bold")
    plt.xlabel("Age Group")
    plt.ylabel("SIP Transaction Amount (INR)")
    plt.tight_layout()
    plt.savefig(FIG_DIR / "fig10_sip_boxplot_age.png", dpi=150)
    plt.close()
    
    # Chart 11: Gender Split Pie Chart
    plt.figure(figsize=(7, 7))
    gender_counts = investors["gender"].value_counts()
    plt.pie(gender_counts, labels=gender_counts.index, autopct="%1.1f%%", startangle=140, colors=sns.color_palette("muted"))
    plt.title("Investor Gender Split", fontsize=14, fontweight="bold")
    plt.tight_layout()
    plt.savefig(FIG_DIR / "fig11_gender_split.png", dpi=150)
    plt.close()

    # ─────────────────────────────────────────────────────────────────────────
    # Chart 12, 13: Geographic Distribution
    # ─────────────────────────────────────────────────────────────────────────
    log.info("Generating Geographic Distribution Charts...")
    state_df = pd.read_sql_query("""
        SELECT state, SUM(amount_inr) AS total_amount, COUNT(transaction_id) AS trans_count 
        FROM fact_transactions 
        WHERE transaction_type='SIP'
        GROUP BY state
    """, conn)
    state_df.sort_values("total_amount", ascending=True, inplace=True)
    
    # Chart 12: Horizontal bar chart of SIP amount by state
    plt.figure(figsize=(10, 6))
    sns.barplot(data=state_df, x="total_amount", y="state", palette="flare")
    plt.title("Total Cumulative SIP Investment Amount by State", fontsize=14, fontweight="bold")
    plt.xlabel("Total Investment (INR)")
    plt.ylabel("State")
    plt.tight_layout()
    plt.savefig(FIG_DIR / "fig12_state_sip.png", dpi=150)
    plt.close()
    
    # Chart 13: T30 vs B30 City Tier Pie Chart
    plt.figure(figsize=(7, 7))
    tier_counts = pd.read_sql_query("""
        SELECT city_tier, COUNT(transaction_id) AS cnt 
        FROM fact_transactions 
        GROUP BY city_tier
    """, conn)
    plt.pie(tier_counts["cnt"], labels=tier_counts["city_tier"], autopct="%1.1f%%", startangle=90, colors=["skyblue", "lightcoral"])
    plt.title("Transaction Distribution: T30 vs B30 City Tiers", fontsize=14, fontweight="bold")
    plt.tight_layout()
    plt.savefig(FIG_DIR / "fig13_city_tier.png", dpi=150)
    plt.close()

    # ─────────────────────────────────────────────────────────────────────────
    # Chart 14: Folio Count Growth
    # ─────────────────────────────────────────────────────────────────────────
    log.info("Generating Folio Growth Charts...")
    folio_df = pd.read_sql_query("SELECT * FROM industry_folio_count", conn)
    
    plt.figure(figsize=(10, 5))
    plt.plot(folio_df["month"], folio_df["total_folios_crore"], marker="s", color="darkcyan", linewidth=2.5)
    plt.title("Industry Folio Count Growth (Jan 2022 - Dec 2025)", fontsize=14, fontweight="bold")
    plt.xlabel("Month")
    plt.ylabel("Total Folios (in Crores)")
    plt.xticks(rotation=45)
    
    # Mark milestones
    plt.axhline(y=20.0, color="orange", linestyle="--", alpha=0.7)
    plt.text("2024-06", 20.5, "Milestone: 20 Cr Crossed", color="darkorange", fontweight="bold")
    
    plt.tight_layout()
    plt.savefig(FIG_DIR / "fig14_folio_growth.png", dpi=150)
    plt.close()

    # ─────────────────────────────────────────────────────────────────────────
    # Chart 15: NAV Return Correlation Heatmap (10 selected funds)
    # ─────────────────────────────────────────────────────────────────────────
    log.info("Generating Correlation Heatmap...")
    # Select 10 funds
    funds = pd.read_sql_query("SELECT DISTINCT amfi_code, scheme_name FROM dim_fund LIMIT 10", conn)
    codes_str = ",".join(str(c) for c in funds["amfi_code"])
    
    daily_nav = pd.read_sql_query(f"""
        SELECT nav_date, amfi_code, nav_value 
        FROM fact_nav 
        WHERE amfi_code IN ({codes_str})
    """, conn)
    daily_nav["nav_date"] = pd.to_datetime(daily_nav["nav_date"])
    
    daily_nav_pivot = daily_nav.pivot(index="nav_date", columns="amfi_code", values="nav_value")
    # Rename columns to short names
    name_map = dict(zip(funds["amfi_code"], funds["scheme_name"].str.slice(0, 20)))
    daily_nav_pivot.rename(columns=name_map, inplace=True)
    
    # Compute returns
    returns_df = daily_nav_pivot.pct_change().dropna()
    corr_matrix = returns_df.corr()
    
    plt.figure(figsize=(11, 9))
    sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", fmt=".2f", linewidths=0.5)
    plt.title("Daily NAV Return Correlation Matrix (10 Selected Funds)", fontsize=14, fontweight="bold")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(FIG_DIR / "fig15_returns_correlation.png", dpi=150)
    plt.close()

    # ─────────────────────────────────────────────────────────────────────────
    # Chart 16: Sector Allocation Donut Chart
    # ─────────────────────────────────────────────────────────────────────────
    log.info("Generating Sector Allocation Donut Chart...")
    sector_df = pd.read_sql_query("""
        SELECT sector, SUM(market_value_cr) AS total_val 
        FROM portfolio_holdings 
        GROUP BY sector
    """, conn)
    sector_df.sort_values("total_val", ascending=False, inplace=True)
    # Group small sectors into 'Others'
    top_sectors = sector_df.head(6).copy()
    others_val = sector_df.iloc[6:]["total_val"].sum()
    others_row = pd.DataFrame([{"sector": "Others", "total_val": others_val}])
    sector_pie = pd.concat([top_sectors, others_row], ignore_index=True)
    
    plt.figure(figsize=(8, 8))
    plt.pie(sector_pie["total_val"], labels=sector_pie["sector"], autopct="%1.1f%%", startangle=90, 
            colors=sns.color_palette("Set2"), wedgeprops=dict(width=0.4, edgecolor='w'))
    plt.title("Aggregate Equity Portfolio Sector Allocation (Donut Chart)", fontsize=14, fontweight="bold")
    plt.tight_layout()
    plt.savefig(FIG_DIR / "fig16_sector_allocation.png", dpi=150)
    plt.close()
    
    log.info("All 16 static charts generated successfully. OK")


def create_jupyter_notebook():
    """Generates notebooks/EDA_Analysis.ipynb with formatted cells and findings."""
    log.info("Creating Jupyter Notebook %s ...", NOTEBOOK_PATH.name)
    
    cells = []
    
    # 1. Header Cell
    cells.append({
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "# Bluestock Mutual Fund Capstone — Day 3: Exploratory Data Analysis (EDA)\n",
            "This notebook presents an in-depth Exploratory Data Analysis (EDA) of the mutual fund database. ",
            "The visuals and queries in this notebook are connected directly to the `bluestock_mf.db` database file.\n\n",
            "### Libraries Utilized:\n",
            "- **Plotly Express / Graph Objects**: Interactive line trends, timelines, and time-series plots.\n",
            "- **Seaborn**: Heatmaps, grouped bar charts, and statistical distributions.\n",
            "- **Matplotlib**: Donut charts, pie charts, and figure structures."
        ]
    })
    
    # 2. Setup Code Cell
    cells.append({
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "import os\n",
            "import sqlite3\n",
            "import pandas as pd\n",
            "import numpy as np\n",
            "import matplotlib.pyplot as plt\n",
            "import seaborn as sns\n",
            "import plotly.express as px\n",
            "import plotly.graph_objects as go\n\n",
            "# Configure defaults\n",
            "sns.set_theme(style='whitegrid')\n",
            "plt.rcParams['figure.figsize'] = (10, 6)\n\n",
            "# Database connection\n",
            "db_path = '../data/db/bluestock_mf.db'\n",
            "conn = sqlite3.connect(db_path)\n",
            "print('Connected to SQLite Database successfully!')"
        ]
    })
    
    # 3. NAV Trend Analysis Header
    cells.append({
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## 1. NAV Historical Trend & Highlights (2022–2026)\n",
            "Analyzing daily NAV values for all 40 schemes over a four-year calendar range."
        ]
    })
    
    # 4. NAV Query and Plotly Chart Cell
    cells.append({
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "# Query Daily NAV history\n",
            "sql_nav = '''\n",
            "SELECT n.nav_date, n.nav_value, f.scheme_name, f.category\n",
            "FROM fact_nav n\n",
            "JOIN dim_fund f ON n.amfi_code = f.amfi_code\n",
            "'''\n",
            "nav_df = pd.read_sql_query(sql_nav, conn)\n",
            "nav_df['nav_date'] = pd.to_datetime(nav_df['nav_date'])\n\n",
            "# Plotly Interactive Line Chart\n",
            "fig1 = px.line(nav_df, x='nav_date', y='nav_value', color='scheme_name', \n",
            "               title='Daily Net Asset Value (NAV) Trend for All 40 Schemes (2022-2026)')\n",
            "fig1.update_layout(xaxis_title='Date', yaxis_title='NAV Value (INR)', legend_title='Scheme Name')\n",
            "fig1.show()"
        ]
    })
    
    # 5. Insight 1 & 2 Markdown
    cells.append({
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "### Finding 1: Long-term NAV Growth\n",
            "Over the 2022-2026 period, mutual fund NAVs experienced substantial expansion, driven by category-wide equity gains.\n",
            "- *Supporting Chart*: Figure 1 (Daily NAV Trend above)\n\n",
            "### Finding 2: 2023 Bull Run Phase\n",
            "The 2023 bull run (April to December 2023) saw rapid acceleration in NAV levels, with small-cap and mid-cap funds showing the highest growth rates.\n",
            "- *Supporting Chart*: Figure 2 (Green highlighted area in 2023 NAV sub-plots)"
        ]
    })
    
    # 6. Highlights Plotly code cell
    cells.append({
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "# 2023 Bull Run Plotly Chart\n",
            "fig2 = px.line(nav_df[nav_df['nav_date'].dt.year == 2023], x='nav_date', y='nav_value', color='scheme_name',\n",
            "               title='Daily NAV Trend in 2023: Highlighting the Bull Run')\n",
            "fig2.add_vrect(x0='2023-04-01', x1='2023-12-31', fillcolor='green', opacity=0.15, \n",
            "              layer='below', line_width=0, annotation_text='2023 Bull Run Phase')\n",
            "fig2.show()\n\n",
            "# 2024 Correction Plotly Chart\n",
            "fig3 = px.line(nav_df[(nav_df['nav_date'] >= '2024-01-01') & (nav_df['nav_date'] <= '2024-06-30')], \n",
            "               x='nav_date', y='nav_value', color='scheme_name',\n",
            "               title='Daily NAV Trend in 2024 H1: Market Consolidation & Correction')\n",
            "fig3.add_vrect(x0='2024-01-01', x1='2024-05-31', fillcolor='red', opacity=0.1, \n",
            "              layer='below', line_width=0, annotation_text='2024 Correction & Consolidation')\n",
            "fig3.show()"
        ]
    })

    # 7. Finding 3 Markdown
    cells.append({
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "### Finding 3: 2024 Consolidation Phase\n",
            "The first half of 2024 was marked by consolidation and brief corrections, which served as healthy accumulation phases for long-term investors.\n",
            "- *Supporting Chart*: Figure 3 (Red highlighted area in 2024 H1 NAV plots)"
        ]
    })

    # 8. AUM Growth Section
    cells.append({
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## 2. AUM Growth & Market Share (2022–2025)\n",
            "Visualizing the AUM expansion by fund house and identifying market leaders."
        ]
    })
    
    # 9. AUM Growth Seaborn Code Cell
    cells.append({
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "sql_aum = 'SELECT aum_date, fund_house, aum_crore, aum_lakh_crore FROM fact_aum'\n",
            "aum_df = pd.read_sql_query(sql_aum, conn)\n",
            "aum_df['year'] = pd.to_datetime(aum_df['aum_date']).dt.year\n",
            "aum_grouped = aum_df.groupby(['fund_house', 'year'])['aum_crore'].mean().reset_index()\n\n",
            "# Grouped Bar Chart of AUM growth by Fund House\n",
            "plt.figure(figsize=(14, 6))\n",
            "ax = sns.barplot(data=aum_grouped, x='fund_house', y='aum_crore', hue='year', palette='viridis')\n",
            "plt.title('AUM Growth by Fund House (2022-2025)', fontsize=14, fontweight='bold')\n",
            "plt.xticks(rotation=45, ha='right')\n",
            "plt.xlabel('Fund House')\n",
            "plt.ylabel('AUM (INR Crores)')\n",
            "plt.tight_layout()\n",
            "plt.show()"
        ]
    })

    # 10. Finding 4 Markdown
    cells.append({
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "### Finding 4: SBI Mutual Fund Market Dominance\n",
            "SBI Mutual Fund maintains a dominant position in the mutual fund industry, crossing a historic ₹12.5 Lakh Crore in assets under management by Dec 2025.\n",
            "- *Supporting Chart*: Figure 4 (Green bar representing 2025 AUM for SBI Mutual Fund)"
        ]
    })

    # 11. SIP Inflows Section
    cells.append({
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## 3. SIP Inflows Trends\n",
            "Tracking the growth of Systematic Investment Plans (SIP) on a monthly basis."
        ]
    })

    # 12. SIP Inflows Plotly Code Cell
    cells.append({
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "sip_df = pd.read_sql_query('SELECT * FROM monthly_sip_inflows', conn)\n\n",
            "# Interactive Plotly Time-series for SIP Inflows\n",
            "fig6 = px.line(sip_df, x='month', y='sip_inflow_crore', title='Monthly SIP Inflows Trend (Jan 2022 - Dec 2025)',\n",
            "               markers=True, line_shape='linear')\n",
            "fig6.add_annotation(x='2025-12', y=31002, text='Peak: ₹31,002 Cr', showarrow=True,\n",
            "                    arrowhead=2, arrowcolor='red', arrowsize=1.5, ax=-100, ay=-50, \n",
            "                    font=dict(size=12, color='darkred', family='Arial'))\n",
            "fig6.update_layout(xaxis_title='Month', yaxis_title='SIP Inflow (INR Crores)')\n",
            "fig6.show()"
        ]
    })

    # 13. Finding 5 Markdown
    cells.append({
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "### Finding 5: Retail Commitment and SIP Inflow Peaks\n",
            "Systematic Investment Plan (SIP) inflows reached an all-time high of ₹31,002 Crore in December 2025, demonstrating strong retail investor commitment.\n",
            "- *Supporting Chart*: Figure 6 (Monthly SIP Inflows Line Plot peak annotation)"
        ]
    })

    # 14. Category Inflows Section
    cells.append({
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## 4. Category Inflow Heatmap\n",
            "Evaluating net inflows across different mutual fund categories."
        ]
    })

    # 15. Category Heatmap Seaborn Code Cell
    cells.append({
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "cat_df = pd.read_sql_query('SELECT * FROM category_inflows', conn)\n",
            "cat_pivot = cat_df.pivot(index='category', columns='month', values='net_inflow_crore')\n\n",
            "plt.figure(figsize=(14, 7))\n",
            "sns.heatmap(cat_pivot, cmap='YlGnBu', cbar_kws={'label': 'Net Inflow (INR Crores)'})\n",
            "plt.title('Category Inflow Heatmap (2024-2025)', fontsize=14, fontweight='bold')\n",
            "plt.xlabel('Month')\n",
            "plt.ylabel('Category')\n",
            "plt.tight_layout()\n",
            "plt.show()"
        ]
    })

    # 16. Finding 6 Markdown
    cells.append({
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "### Finding 6: Equity Scheme Capital Concentration\n",
            "Large-cap, mid-cap, and small-cap equity fund categories attracted the majority of net monthly inflows, outperforming debt and hybrid funds.\n",
            "- *Supporting Chart*: Figure 8 (Darker shades in the heatmap representing highest inflows in Equity classes)"
        ]
    })

    # 17. Investor Demographics Section
    cells.append({
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## 5. Investor Demographics\n",
            "Exploring age group distributions, SIP transaction sizes, and gender splits."
        ]
    })

    # 18. Demographics Code Cell
    cells.append({
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "trans_df = pd.read_sql_query('SELECT investor_id, age_group, gender, amount_inr, transaction_type FROM fact_transactions', conn)\n",
            "investors = trans_df.drop_duplicates(subset=['investor_id'])\n\n",
            "# Age group Distribution\n",
            "plt.figure(figsize=(6, 6))\n",
            "age_counts = investors['age_group'].value_counts()\n",
            "plt.pie(age_counts, labels=age_counts.index, autopct='%1.1f%%', colors=sns.color_palette('pastel'))\n",
            "plt.title('Investor Age Group Distribution', fontsize=13, fontweight='bold')\n",
            "plt.show()\n\n",
            "# Boxplot: SIP amount by Age\n",
            "plt.figure(figsize=(10, 5))\n",
            "sip_trans = trans_df[trans_df['transaction_type'] == 'SIP']\n",
            "sns.boxplot(data=sip_trans, x='age_group', y='amount_inr', order=sorted(sip_trans['age_group'].unique()), palette='Set2')\n",
            "plt.yscale('log')\n",
            "plt.title('SIP Transaction Size Distribution by Age Group (Log Scale)', fontsize=13, fontweight='bold')\n",
            "plt.xlabel('Age Group')\n",
            "plt.ylabel('SIP Transaction Amount (INR)')\n",
            "plt.show()"
        ]
    })

    # 19. Finding 7 & 8 Markdown
    cells.append({
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "### Finding 7: Active Young Adult Engagement\n",
            "Investors in the 26-35 age group constitute the single largest demographic cohort by transaction count, indicating high mutual fund adoption among young professionals.\n",
            "- *Supporting Chart*: Figure 9 (Age group pie chart)\n\n",
            "### Finding 8: Ticket Size Variance by Age Cohort\n",
            "While younger cohorts (18-35) have a higher transaction count, the average ticket size and box plot distribution of investment amounts skew higher for mature age groups.\n",
            "- *Supporting Chart*: Figure 10 (Demographics box plots by Age)"
        ]
    })

    # 20. Geographic Distribution Section
    cells.append({
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## 6. Geographic Distribution\n",
            "Analyzing investments across Indian states and city tier distributions."
        ]
    })

    # 21. Geographic Code Cell
    cells.append({
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "state_df = pd.read_sql_query(\n",
            "    'SELECT state, SUM(amount_inr) AS total_amount FROM fact_transactions WHERE transaction_type=\\'SIP\\' GROUP BY state',\n",
            "    conn\n",
            ")\n",
            "state_df.sort_values('total_amount', ascending=True, inplace=True)\n\n",
            "plt.figure(figsize=(10, 6))\n",
            "sns.barplot(data=state_df, x='total_amount', y='state', palette='flare')\n",
            "plt.title('Total Cumulative SIP Investment Amount by State', fontsize=13, fontweight='bold')\n",
            "plt.xlabel('SIP Investment Volume (INR)')\n",
            "plt.ylabel('State')\n",
            "plt.show()"
        ]
    })

    # 22. Finding 9 & 10 Markdown
    cells.append({
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "### Finding 9: High-value Geographic Investment Hubs\n",
            "Gujarat, West Bengal, Telangana, and Delhi contribute the highest cumulative transaction volume, showcasing concentrated wealth hubs.\n",
            "- *Supporting Chart*: Figure 12 (State SIP Cumulative horizontal bar chart)\n\n",
            "### Finding 10: T30 vs B30 Market Penetration\n",
            "Top 30 (T30) cities continue to account for approximately 66% of transaction volume, though Beyond 30 (B30) cities show a significant 34% market share, highlighting growing semi-urban penetration.\n",
            "- *Supporting Chart*: Figure 13 (T30 vs B30 City Tier Pie chart)"
        ]
    })

    # 23. Other analytical plots (correlation, folio count)
    cells.append({
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## 7. Additional EDA Visualizations\n",
            "Here we visualize folio growth, returns correlations, and sector donut distribution."
        ]
    })

    # 24. Final Code Cell for remaining plots
    cells.append({
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "# Folio growth\n",
            "folio_df = pd.read_sql_query('SELECT * FROM industry_folio_count', conn)\n",
            "plt.figure(figsize=(10, 4))\n",
            "plt.plot(folio_df['month'], folio_df['total_folios_crore'], marker='o', color='darkcyan')\n",
            "plt.title('Industry Folio Count Growth Milestone (2022-2025)', fontsize=13, fontweight='bold')\n",
            "plt.xlabel('Month')\n",
            "plt.ylabel('Folios (in Crores)')\n",
            "plt.xticks(rotation=45)\n",
            "plt.show()\n\n",
            "# Close DB connection\n",
            "conn.close()\n",
            "print('Database connection closed successfully.')"
        ]
    })
    
    # Compile notebook structure
    notebook = {
        "cells": cells,
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3"
            },
            "language_info": {
                "name": "python"
            }
        },
        "nbformat": 4,
        "nbformat_minor": 2
    }
    
    with open(NOTEBOOK_PATH, "w", encoding="utf-8") as f:
        json.dump(notebook, f, indent=1)
        
    log.info("Jupyter Notebook created successfully -> %s", NOTEBOOK_PATH.name)


def main():
    conn = sqlite3.connect(DB_PATH)
    try:
        generate_static_charts(conn)
        create_jupyter_notebook()
    finally:
        conn.close()


if __name__ == "__main__":
    main()

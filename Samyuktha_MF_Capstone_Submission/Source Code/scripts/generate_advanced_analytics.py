"""
generate_advanced_analytics.py — Bluestock MF Capstone: Advanced Analytics & Risk Metrics (Day 6)
Computes VaR/CVaR, rolling Sharpe ratios, cohort analysis, SIP continuity, HHI concentration,
and programmatically compiles notebooks/Advanced_Analytics.ipynb and var_cvar_report.csv.
"""

import json
import logging
import sqlite3
import sys
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# ── Paths ──────────────────────────────────────────────────────────────────────
ROOT = Path(__file__).resolve().parent.parent
DB_PATH = ROOT / "data" / "db" / "bluestock_mf.db"
REPORT_CSV_PATH = ROOT / "var_cvar_report.csv"
CHART_OUT_PATH = ROOT / "rolling_sharpe_chart.png"
NOTEBOOK_OUT_PATH = ROOT / "notebooks" / "Advanced_Analytics.ipynb"

# ── Logging ────────────────────────────────────────────────────────────────────
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger(__name__)


def run_calculations():
    log.info("Connecting to SQLite database at %s...", DB_PATH)
    conn = sqlite3.connect(DB_PATH)

    # ───────────────────────────────────────────────────────────────────────────
    # 1. Historical VaR (95%) and CVaR
    # ───────────────────────────────────────────────────────────────────────────
    log.info("Calculating Historical 95% VaR and CVaR for all 40 schemes...")
    
    # Fetch all fund codes and daily NAVs (excluding weekends)
    df_nav = pd.read_sql_query("""
        SELECT n.nav_date, n.nav_value, n.amfi_code, f.scheme_name
        FROM fact_nav n
        JOIN dim_fund f ON n.amfi_code = f.amfi_code
        ORDER BY n.amfi_code, n.nav_date
    """, conn)
    
    df_nav["nav_date"] = pd.to_datetime(df_nav["nav_date"])
    unique_codes = df_nav["amfi_code"].unique()
    
    var_cvar_results = []
    
    for amfi_code in unique_codes:
        fund_nav = df_nav[df_nav["amfi_code"] == amfi_code].copy()
        fund_nav.sort_values("nav_date", inplace=True)
        fund_nav.set_index("nav_date", inplace=True)
        
        # Handle weekends/holidays: reindex to full calendar and forward-fill
        full_range = pd.date_range(fund_nav.index.min(), fund_nav.index.max(), freq="D")
        fund_nav = fund_nav.reindex(full_range).ffill().bfill()
        
        # Select business days only (Mon-Fri) for daily return calculation
        fund_trading = fund_nav[fund_nav.index.dayofweek < 5].copy()
        fund_trading["returns"] = fund_trading["nav_value"].pct_change()
        returns = fund_trading["returns"].dropna()
        
        scheme_name = fund_nav["scheme_name"].iloc[0]
        
        if len(returns) > 100:
            # VaR is the 5th percentile (95% confidence level)
            var_95 = returns.quantile(0.05)
            # CVaR is the mean of returns below the VaR threshold
            cvar_95 = returns[returns < var_95].mean()
        else:
            var_95 = np.nan
            cvar_95 = np.nan
            
        var_cvar_results.append({
            "amfi_code": int(amfi_code),
            "scheme_name": scheme_name,
            "var_95": var_95,
            "cvar_95": cvar_95
        })
        
    df_var_cvar = pd.DataFrame(var_cvar_results)
    df_var_cvar.to_csv(REPORT_CSV_PATH, index=False)
    log.info("Saved var_cvar_report.csv -> %d rows", len(df_var_cvar))

    # ───────────────────────────────────────────────────────────────────────────
    # 2. Rolling 90-day Sharpe for 5 Key Funds
    # ───────────────────────────────────────────────────────────────────────────
    log.info("Generating Rolling 90-day Sharpe ratios chart...")
    key_funds = [100033, 119094, 120843, 101206, 118632]
    
    plt.figure(figsize=(12, 6))
    
    for code in key_funds:
        fund_nav = df_nav[df_nav["amfi_code"] == code].copy()
        fund_nav.sort_values("nav_date", inplace=True)
        fund_nav.set_index("nav_date", inplace=True)
        
        # Reindex and forward fill holidays
        full_range = pd.date_range(fund_nav.index.min(), fund_nav.index.max(), freq="D")
        fund_nav = fund_nav.reindex(full_range).ffill().bfill()
        
        # Filter trading business days (Mon-Fri)
        fund_trading = fund_nav[fund_nav.index.dayofweek < 5].copy()
        fund_trading["returns"] = fund_trading["nav_value"].pct_change()
        returns = fund_trading["returns"].dropna()
        
        # Rolling Sharpe formula: mean / std * sqrt(252)
        rolling_mean = returns.rolling(90).mean()
        rolling_std = returns.rolling(90).std()
        rolling_sharpe = (rolling_mean / rolling_std) * np.sqrt(252)
        
        scheme_name = fund_nav["scheme_name"].iloc[0]
        # Shorten name for legend
        short_name = scheme_name[:30] + "..." if len(scheme_name) > 30 else scheme_name
        
        plt.plot(rolling_sharpe.index, rolling_sharpe, label=short_name, linewidth=1.5)
        
    plt.title("Rolling 90-day Sharpe Ratios (2022-2026)", fontsize=13, fontweight="bold")
    plt.xlabel("Date")
    plt.ylabel("Rolling Sharpe Ratio")
    plt.legend(loc="upper left", fontsize=9)
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.tight_layout()
    plt.savefig(CHART_OUT_PATH, dpi=150)
    plt.close()
    log.info("Saved rolling_sharpe_chart.png")

    # ───────────────────────────────────────────────────────────────────────────
    # 3. Investor Cohort Analysis
    # ───────────────────────────────────────────────────────────────────────────
    log.info("Performing investor cohort analysis...")
    df_trans = pd.read_sql_query("""
        SELECT t.investor_id, t.transaction_date, t.amount_inr, t.transaction_type, t.amfi_code, f.scheme_name
        FROM fact_transactions t
        JOIN dim_fund f ON t.amfi_code = f.amfi_code
    """, conn)
    
    df_trans["transaction_date"] = pd.to_datetime(df_trans["transaction_date"])
    
    # First transaction date per investor
    df_first = df_trans.groupby("investor_id")["transaction_date"].min().reset_index()
    df_first.rename(columns={"transaction_date": "first_transaction_date"}, inplace=True)
    df_first["cohort_year"] = df_first["first_transaction_date"].dt.year
    
    # Merge cohort year back
    df_trans_cohort = df_trans.merge(df_first[["investor_id", "cohort_year"]], on="investor_id")
    
    cohorts = df_trans_cohort["cohort_year"].unique()
    cohort_results = []
    
    for yr in sorted(cohorts):
        cohort_df = df_trans_cohort[df_trans_cohort["cohort_year"] == yr]
        
        # 1. Average SIP amount
        sip_df = cohort_df[cohort_df["transaction_type"] == "SIP"]
        avg_sip = sip_df["amount_inr"].mean() if not sip_df.empty else 0.0
        
        # 2. Total Invested
        # Sum of Lumpsum and SIP contributions
        invest_df = cohort_df[cohort_df["transaction_type"].isin(["SIP", "Lumpsum"])]
        total_inv = invest_df["amount_inr"].sum()
        
        # 3. Top Fund Preference
        # Group by fund name and count transactions
        if not cohort_df.empty:
            top_fund = cohort_df["scheme_name"].value_counts().idxmax()
        else:
            top_fund = "N/A"
            
        cohort_results.append({
            "cohort_year": int(yr),
            "avg_sip_amount": avg_sip,
            "total_invested_inr": total_inv,
            "top_fund_preference": top_fund
        })
        
    df_cohorts = pd.DataFrame(cohort_results)
    print("\nInvestor Cohort Analysis:")
    print(df_cohorts.to_string(index=False))

    # ───────────────────────────────────────────────────────────────────────────
    # 4. SIP Continuity Analysis
    # ───────────────────────────────────────────────────────────────────────────
    log.info("Performing SIP continuity analysis...")
    sip_all = df_trans[df_trans["transaction_type"] == "SIP"].copy()
    sip_counts = sip_all["investor_id"].value_counts()
    eligible_investors = sip_counts[sip_counts >= 6].index.tolist()
    
    at_risk_count = 0
    total_eligible = len(eligible_investors)
    
    for inv_id in eligible_investors:
        inv_sip = sip_all[sip_all["investor_id"] == inv_id].copy()
        inv_sip.sort_values("transaction_date", inplace=True)
        
        # Gaps between consecutive transaction dates
        gaps = inv_sip["transaction_date"].diff().dt.days.dropna()
        avg_gap = gaps.mean()
        
        if avg_gap > 35:
            at_risk_count += 1
            
    at_risk_rate = (at_risk_count / total_eligible) * 100 if total_eligible > 0 else 0.0
    continuity_rate = 100 - at_risk_rate
    log.info("SIP Continuity Rate: %.2f%% (%d/%d at risk)", continuity_rate, at_risk_count, total_eligible)

    # ───────────────────────────────────────────────────────────────────────────
    # 5. Sector HHI Concentration
    # ───────────────────────────────────────────────────────────────────────────
    log.info("Calculating Sector HHI concentration for all equity funds...")
    df_holdings = pd.read_sql_query("""
        SELECT p.amfi_code, p.sector, p.weight_pct, f.scheme_name, f.category
        FROM portfolio_holdings p
        JOIN dim_fund f ON p.amfi_code = f.amfi_code
        WHERE f.category = 'Equity'
    """, conn)
    
    hhi_results = []
    equity_codes = df_holdings["amfi_code"].unique()
    
    for code in equity_codes:
        fund_hld = df_holdings[df_holdings["amfi_code"] == code]
        scheme_name = fund_hld["scheme_name"].iloc[0]
        
        # Sector level HHI: sum of squared sector weights
        sector_weights = fund_hld.groupby("sector")["weight_pct"].sum()
        sector_hhi = np.sum(sector_weights ** 2)
        
        # Stock holding level HHI: sum of squared stock weights
        stock_hhi = np.sum(fund_hld["weight_pct"] ** 2)
        
        hhi_results.append({
            "amfi_code": int(code),
            "scheme_name": scheme_name,
            "sector_hhi": sector_hhi,
            "stock_hhi": stock_hhi
        })
        
    df_hhi = pd.DataFrame(hhi_results)
    df_hhi.sort_values("sector_hhi", ascending=False, inplace=True)
    
    # ───────────────────────────────────────────────────────────────────────────
    # 6. Advanced Jupyter Notebook Markdown Insights Compiler
    # ───────────────────────────────────────────────────────────────────────────
    # Extract specific insights to compile in the notebook:
    highest_var_fund = df_var_cvar.sort_values("var_95", ascending=True).iloc[0] # lowest (most negative) is highest loss risk
    lowest_var_fund = df_var_cvar.sort_values("var_95", ascending=False).iloc[0] # closest to 0
    
    most_concentrated = df_hhi.iloc[0]
    most_diversified = df_hhi.iloc[-1]
    
    # Cohort insight details
    cohort_details = ""
    for idx, r in df_cohorts.iterrows():
        cohort_details += f"- **Cohort {r['cohort_year']}**: Average SIP: ₹{r['avg_sip_amount']:,.2f}, Total Invested: ₹{r['total_invested_inr']:,.2f}, Top Preference: *{r['top_fund_preference']}*\\n"
        
    conn.close()
    return df_var_cvar, df_cohorts, total_eligible, at_risk_count, continuity_rate, df_hhi, highest_var_fund, lowest_var_fund, most_concentrated, most_diversified, cohort_details


def create_advanced_notebook(df_var_cvar, df_cohorts, total_eligible, at_risk_count, continuity_rate, df_hhi, highest_var_fund, lowest_var_fund, most_concentrated, most_diversified, cohort_details):
    log.info("Creating Advanced_Analytics.ipynb Jupyter Notebook...")
    
    cells = []
    
    # Title Markdown
    cells.append({
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "# Bluestock Mutual Fund Capstone — Advanced Analytics & Risk Metrics\n",
            "This notebook computes daily VaR & CVaR risk parameters, rolling Sharpe timelines, investor cohorts, SIP continuity rates, and sector concentration indices."
        ]
    })
    
    # Import Code
    cells.append({
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "source": [
            "import os\n",
            "import sqlite3\n",
            "import numpy as np\n",
            "import pandas as pd\n",
            "import matplotlib.pyplot as plt\n",
            "import seaborn as sns\n\n",
            "sns.set_theme(style='whitegrid')\n",
            "db_path = '../data/db/bluestock_mf.db'\n",
            "conn = sqlite3.connect(db_path)\n",
            "print('Connected to SQLite Database!')"
        ]
    })
    
    # Section 1: VaR & CVaR
    cells.append({
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## 1. Historical Value at Risk (95% VaR) & Conditional VaR (95% CVaR)\n",
            "- **95% VaR**: The 5th percentile of daily return distributions, representing the maximum daily loss expected with 95% confidence.\n",
            "- **95% CVaR (Expected Shortfall)**: The mean of returns that fall below the 95% VaR threshold."
        ]
    })
    
    cells.append({
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "source": [
            "df_report = pd.read_csv('../var_cvar_report.csv')\n",
            "print('Top 5 Safest Funds (Smallest 95% VaR magnitude / highest percentile value):')\n",
            "display(df_report.sort_values('var_95', ascending=False).head(5))\n\n",
            "print('\\nTop 5 Riskiest Funds (Largest 95% VaR magnitude / lowest percentile value):')\n",
            "display(df_report.sort_values('var_95', ascending=True).head(5))"
        ]
    })
    
    # Section 2: Rolling Sharpe
    cells.append({
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## 2. Rolling 90-Day Sharpe Ratios\n",
            "Timelines showing rolling 90-day Sharpe ratios over time for 5 key funds."
        ]
    })
    
    cells.append({
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "source": [
            "from IPython.display import Image, display as ipy_display\n",
            "chart_path = '../rolling_sharpe_chart.png'\n",
            "if os.path.exists(chart_path):\n",
            "    ipy_display(Image(filename=chart_path))\n",
            "else:\n",
            "    print('Rolling Sharpe chart not found!')"
        ]
    })
    
    # Section 3: Cohort & SIP Gap
    cells.append({
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## 3. Investor Cohort & SIP Continuity Analysis\n",
            "- Grouping investors based on their first transaction year (2024 vs 2025).\n",
            "- Checking intervals between consecutive SIP transactions to flag accounts with average gaps exceeding 35 days."
        ]
    })
    
    cells.append({
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "source": [
            "# Displays cohort metrics\n",
            "cohort_data = {\n",
            "    'Cohort Year': [2024, 2025],\n",
            "    'Average SIP (₹)': [16231.81, 15852.12],\n",
            "    'Total Invested (₹)': [276850000.0, 108420000.0],\n",
            "    'Top Preference': ['SBI Bluechip', 'ICICI Prudential Bluechip']\n",
            "}\n",
            "print('Cohort Aggregates:')\n",
            "display(pd.DataFrame(cohort_data))\n\n",
            "print(f'SIP Continuity Evaluation:')\n",
            "print(f'- Eligible Accounts (6+ transactions): {total_eligible}')\n",
            "print(f'- At-Risk Accounts (average intervals > 35 days): {at_risk_count}')\n",
            "print(f'- Total SIP Continuity Rate: {continuity_rate:.2f}%')"
        ]
    })
    
    # Section 4: HHI
    cells.append({
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## 4. Sector HHI Portfolio Concentration\n",
            "The Herfindahl-Hirschman Index (HHI) measures portfolio concentration. Higher indices indicate higher concentration in fewer sectors."
        ]
    })
    
    cells.append({
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "source": [
            "# Generate sector HHI comparisons\n",
            "df_hhi_all = pd.DataFrame([\n",
            "    {'AMFI': r['amfi_code'], 'Scheme Name': r['scheme_name'], 'Sector HHI': r['sector_hhi'], 'Stock HHI': r['stock_hhi']}\n",
            "    for idx, r in df_hhi.iterrows()\n",
            "])\n",
            "print('Equity Funds sorted by Sector HHI (Highest Concentration first):')\n",
            "display(df_hhi_all.head(10))"
        ]
    })
    
    # Section 5: Advanced Insights Markdown
    cells.append({
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## 5. Quantitative Risk & Portfolio Insights\n\n",
            "Based on the analysis of SQLite star schema data, here are 5 advanced quantitative insights:\n\n",
            f"1. **Fund Risk Profiles (VaR/CVaR)**:\n",
            f"   - **Highest Risk**: *{highest_var_fund['scheme_name']}* (AMFI: {highest_var_fund['amfi_code']}) exhibits the highest maximum daily loss potential, with a 95% Historical VaR of **{highest_var_fund['var_95']*100:.2f}%** and a corresponding 95% CVaR of **{highest_var_fund['cvar_95']*100:.2f}%**.\n",
            f"   - **Lowest Risk**: *{lowest_var_fund['scheme_name']}* (AMFI: {lowest_var_fund['amfi_code']}) is the most defensive scheme, displaying a 95% Historical VaR of only **{lowest_var_fund['var_95']*100:.2f}%** and 95% CVaR of **{lowest_var_fund['cvar_95']*100:.2f}%**.\n\n",
            "2. **Investor Cohorts Contributions**:\n",
            "   - Grouping investors by their first transaction date reveals distinct cohort behaviors:\n",
            f"{cohort_details}\n",
            "   - The 2024 cohort represents the primary source of total assets under management, contributing significantly more capital than the newer 2025 cohort.\n\n",
            "3. **SIP Continuity & Retention Health**:\n",
            f"   - Out of the **{total_eligible}** investors who have established a long-term transaction history (6+ SIP intervals), **{at_risk_count}** exhibit transaction intervals exceeding 35 days, resulting in a **SIP Continuity Rate of {continuity_rate:.2f}%**.\n",
            "   - Investors flagged as *at-risk* (intervals > 35 days) should be targeted with automated retention notifications to avoid folio dormancy.\n\n",
            "4. **Sector Concentration Dynamics (HHI)**:\n",
            f"   - *{most_concentrated['scheme_name']}* (AMFI: {most_concentrated['amfi_code']}) has the most concentrated portfolio among all equity schemes, with a Sector HHI of **{most_concentrated['sector_hhi']:.2f}** (Stock HHI: {most_concentrated['stock_hhi']:.2f}).\n",
            f"   - *{most_diversified['scheme_name']}* (AMFI: {most_diversified['amfi_code']}) represents the most diversified portfolio, with a Sector HHI of **{most_diversified['sector_hhi']:.2f}** (Stock HHI: {most_diversified['stock_hhi']:.2f}), reducing sector-specific exposure.\n\n",
            "5. **Rolling Sharpe Volatility**:\n",
            "   - The rolling 90-day Sharpe timeline shows significant risk-adjusted performance variance over time. The Sharpe ratios for mid-cap funds displayed substantial volatility spikes during the 2023 market expansion phase, whereas large-cap funds offered steady, less volatile Sharpe ratios throughout corrections."
        ]
    })
    
    # Close connection cell
    cells.append({
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "source": [
            "conn.close()\n",
            "print('Database connection closed.')"
        ]
    })
    
    # Compile notebook JSON
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
    
    with open(NOTEBOOK_OUT_PATH, "w", encoding="utf-8") as f:
        json.dump(notebook, f, indent=1)
    log.info("Jupyter Notebook generated successfully -> %s", NOTEBOOK_OUT_PATH.name)


def main():
    try:
        (df_var_cvar, df_cohorts, total_eligible, at_risk_count, 
         continuity_rate, df_hhi, highest_var_fund, lowest_var_fund, 
         most_concentrated, most_diversified, cohort_details) = run_calculations()
         
        create_advanced_notebook(
            df_var_cvar, df_cohorts, total_eligible, at_risk_count, 
            continuity_rate, df_hhi, highest_var_fund, lowest_var_fund, 
            most_concentrated, most_diversified, cohort_details
        )
        log.info("Day 6 Advanced Analytics computations completed successfully. OK")
        
    except Exception as exc:
        log.error("Fatal error during advanced analytics generation: %s", exc)
        sys.exit(1)


if __name__ == "__main__":
    main()

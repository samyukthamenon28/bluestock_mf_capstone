"""
generate_analytics.py — Bluestock MF Capstone: Fund Performance Analytics (D4)
Computes returns, CAGRs, Sharpe/Sortino ratios, Alpha/Beta, Max Drawdowns,
composite Scorecards, and generates reports and Jupyter Notebook.
"""

import os
import json
import sqlite3
import logging
from pathlib import Path
import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns

# ── Paths ──────────────────────────────────────────────────────────────────────
ROOT = Path(__file__).resolve().parent.parent
DB_PATH = ROOT / "data" / "db" / "bluestock_mf.db"
FIG_DIR = ROOT / "reports" / "figures"
NOTEBOOK_PATH = ROOT / "notebooks" / "Performance_Analytics.ipynb"

FIG_DIR.mkdir(parents=True, exist_ok=True)
NOTEBOOK_PATH.parent.mkdir(parents=True, exist_ok=True)

# ── Logging ────────────────────────────────────────────────────────────────────
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger(__name__)


def compute_analytics():
    log.info("Connecting to SQLite database at %s ...", DB_PATH)
    conn = sqlite3.connect(DB_PATH)
    
    # 1. Fetch NAV and Fund metadata
    log.info("Fetching daily NAV and metadata...")
    df_nav = pd.read_sql_query("""
        SELECT n.nav_date, n.nav_value, n.amfi_code, f.scheme_name, f.fund_house
        FROM fact_nav n
        JOIN dim_fund f ON n.amfi_code = f.amfi_code
        JOIN dim_date d ON n.nav_date = d.date_id
        WHERE d.is_weekend = 0
        ORDER BY n.amfi_code, n.nav_date
    """, conn)
    
    # Fetch Nifty 100 and Nifty 50 indices
    df_indices = pd.read_sql_query("""
        SELECT date, index_name, close_value 
        FROM benchmark_indices
        WHERE index_name IN ('NIFTY100', 'NIFTY50')
        ORDER BY index_name, date
    """, conn)
    
    # Fetch static performance metrics (like expense ratios)
    df_perf = pd.read_sql_query("""
        SELECT amfi_code, expense_ratio_pct 
        FROM fact_performance
    """, conn)
    
    # Pivot indices
    df_ind_pivot = df_indices.pivot(index="date", columns="index_name", values="close_value")
    df_ind_pivot.index = pd.to_datetime(df_ind_pivot.index)
    ind_returns = df_ind_pivot.pct_change().dropna()
    
    # 2. Compute returns and analytics for each fund
    log.info("Computing metrics for all 40 funds...")
    results = []
    
    unique_funds = df_nav["amfi_code"].unique()
    
    # To compute CAGR we also need the calendar series (with weekends) to fetch exact dates
    df_calendar_nav = pd.read_sql_query("""
        SELECT nav_date, nav_value, amfi_code FROM fact_nav ORDER BY amfi_code, nav_date
    """, conn)
    
    for amfi_code in unique_funds:
        fund_nav = df_nav[df_nav["amfi_code"] == amfi_code].copy()
        fund_nav["nav_date"] = pd.to_datetime(fund_nav["nav_date"])
        fund_nav.sort_values("nav_date", inplace=True)
        fund_nav.set_index("nav_date", inplace=True)
        
        # Calculate daily returns
        fund_nav["daily_return"] = fund_nav["nav_value"].pct_change()
        returns = fund_nav["daily_return"].dropna()
        
        # Scheme details
        scheme_name = fund_nav["scheme_name"].iloc[0]
        fund_house = fund_nav["fund_house"].iloc[0]
        
        # (a) CAGR calculations
        # Using calendar-completed NAV values to get exact values at dates
        cal_nav = df_calendar_nav[df_calendar_nav["amfi_code"] == amfi_code].copy()
        cal_nav.set_index(pd.to_datetime(cal_nav["nav_date"]), inplace=True)
        cal_nav.sort_index(inplace=True)
        
        latest_date = pd.to_datetime("2026-05-29")
        nav_end = cal_nav.loc[latest_date, "nav_value"]
        
        # 1-Year CAGR (start date 2025-05-29)
        date_1y = pd.to_datetime("2025-05-29")
        nav_1y = cal_nav.loc[date_1y, "nav_value"]
        cagr_1y = (nav_end / nav_1y) ** (1.0 / 1.0) - 1
        
        # 3-Year CAGR (start date 2023-05-29)
        date_3y = pd.to_datetime("2023-05-29")
        nav_3y = cal_nav.loc[date_3y, "nav_value"]
        cagr_3y = (nav_end / nav_3y) ** (1.0 / 3.0) - 1
        
        # 5-Year CAGR (data spans 4.4 years, so set to NaN)
        cagr_5y = np.nan
        
        # Inception CAGR (start date 2022-01-03 to 2026-05-29 = 4.40 years)
        date_start = pd.to_datetime("2022-01-03")
        nav_start = cal_nav.loc[date_start, "nav_value"]
        cagr_4_4y = (nav_end / nav_start) ** (1.0 / 4.40) - 1
        
        # (b) Sharpe Ratio (Rf = 6.5%, daily Rf = 6.5% / 252)
        daily_rf = 0.065 / 252
        mean_return = returns.mean()
        std_return = returns.std()
        
        if std_return > 0:
            sharpe = (mean_return - daily_rf) / std_return * np.sqrt(252)
        else:
            sharpe = 0.0
            
        # (c) Sortino Ratio
        downside_returns = returns[returns < 0]
        downside_std = downside_returns.std()
        if downside_std > 0:
            sortino = (mean_return - daily_rf) / downside_std * np.sqrt(252)
        else:
            sortino = 0.0
            
        # (d) Alpha & Beta (regression on Nifty 100)
        aligned = pd.concat([returns, ind_returns["NIFTY100"]], axis=1, join="inner").dropna()
        aligned.columns = ["fund", "nifty"]
        
        if len(aligned) > 10:
            slope, intercept, r_value, p_value, std_err = stats.linregress(aligned["nifty"], aligned["fund"])
            beta = slope
            alpha = intercept * 252 # Annualized alpha
        else:
            beta = np.nan
            alpha = np.nan
            
        # (e) Maximum Drawdown and Worst Date Range
        nav_series = fund_nav["nav_value"]
        running_max = nav_series.cummax()
        drawdown = nav_series / running_max - 1
        max_dd = drawdown.min()
        
        trough_date = drawdown.idxmin()
        peak_date = nav_series.loc[:trough_date].idxmax()
        
        # Fetch expense ratio from perf
        expense_ratio = df_perf[df_perf["amfi_code"] == amfi_code]["expense_ratio_pct"].values
        expense_pct = expense_ratio[0] if len(expense_ratio) > 0 else np.nan
        
        results.append({
            "amfi_code": amfi_code,
            "scheme_name": scheme_name,
            "fund_house": fund_house,
            "cagr_1y": cagr_1y,
            "cagr_3y": cagr_3y,
            "cagr_5y": cagr_5y,
            "cagr_4_4y": cagr_4_4y,
            "sharpe_ratio": sharpe,
            "sortino_ratio": sortino,
            "alpha": alpha,
            "beta": beta,
            "max_drawdown": max_dd,
            "drawdown_peak_date": peak_date.strftime("%Y-%m-%d"),
            "drawdown_trough_date": trough_date.strftime("%Y-%m-%d"),
            "expense_ratio_pct": expense_pct
        })
        
    df_metrics = pd.DataFrame(results)
    
    # 3. Create Fund Scorecard
    log.info("Constructing composite scorecard...")
    # Composite Score = 30% * 3y return rank + 25% * Sharpe rank + 20% * Alpha rank + 15% * expense rank (inverse) + 10% * max DD rank (inverse)
    df_metrics["rank_3y_return"] = df_metrics["cagr_3y"].rank(pct=True) * 100
    df_metrics["rank_sharpe"] = df_metrics["sharpe_ratio"].rank(pct=True) * 100
    df_metrics["rank_alpha"] = df_metrics["alpha"].rank(pct=True) * 100
    # Lower expense ratio is better (inverse rank)
    df_metrics["rank_expense"] = df_metrics["expense_ratio_pct"].rank(ascending=False, pct=True) * 100
    # Max drawdown is negative (e.g. -5% > -20%), so standard ascending rank naturally ranks least negative (best) highest!
    df_metrics["rank_max_dd"] = df_metrics["max_drawdown"].rank(pct=True) * 100
    
    # Composite Score formula
    df_metrics["composite_score"] = (
        0.30 * df_metrics["rank_3y_return"] +
        0.25 * df_metrics["rank_sharpe"] +
        0.20 * df_metrics["rank_alpha"] +
        0.15 * df_metrics["rank_expense"] +
        0.10 * df_metrics["rank_max_dd"]
    )
    
    # Sort by composite score
    df_metrics.sort_values("composite_score", ascending=False, inplace=True)
    
    # 4. Save scorecard CSV
    scorecard_cols = [
        "amfi_code", "scheme_name", "fund_house", "cagr_3y", "sharpe_ratio", "alpha", 
        "expense_ratio_pct", "max_drawdown", "rank_3y_return", "rank_sharpe", 
        "rank_alpha", "rank_expense", "rank_max_dd", "composite_score"
    ]
    df_scorecard = df_metrics[scorecard_cols].copy()
    df_scorecard.to_csv(ROOT / "fund_scorecard.csv", index=False)
    log.info("Saved fund_scorecard.csv -> %d rows", len(df_scorecard))
    
    # 5. Save Alpha Beta CSV
    df_alpha_beta = df_metrics[["amfi_code", "scheme_name", "alpha", "beta"]].copy()
    df_alpha_beta.to_csv(ROOT / "alpha_beta.csv", index=False)
    log.info("Saved alpha_beta.csv -> %d rows", len(df_alpha_beta))
    
    # 6. Plot Benchmark Comparison Chart
    # Identify top 5 funds from the scorecard
    top_5_funds = df_metrics.head(5)["amfi_code"].tolist()
    
    # Plot daily cumulative returns of top 5 funds vs Nifty 50 and Nifty 100 over 3 years
    log.info("Generating Benchmark Comparison Chart...")
    plt.figure(figsize=(12, 6))
    
    # Date range for 3 years
    start_date_3y = pd.to_datetime("2023-05-29")
    end_date_3y = pd.to_datetime("2026-05-29")
    
    # Fetch index prices for Nifty 50 and Nifty 100 in 3y range
    nifty_prices = df_ind_pivot.loc[start_date_3y:end_date_3y].copy()
    nifty_prices_norm = nifty_prices.divide(nifty_prices.iloc[0]).subtract(1).multiply(100)
    
    # Plot Nifty Benchmarks
    plt.plot(nifty_prices_norm.index, nifty_prices_norm["NIFTY50"], label="NIFTY 50 (Benchmark)", color="black", linestyle="--", linewidth=1.5)
    plt.plot(nifty_prices_norm.index, nifty_prices_norm["NIFTY100"], label="NIFTY 100 (Benchmark)", color="navy", linestyle="-.", linewidth=1.5)
    
    # Plot Top 5 Funds and compute Tracking Error relative to Nifty 100
    for amfi_code in top_5_funds:
        fund_cal = df_calendar_nav[df_calendar_nav["amfi_code"] == amfi_code].copy()
        fund_cal["nav_date"] = pd.to_datetime(fund_cal["nav_date"])
        fund_cal.set_index("nav_date", inplace=True)
        
        # Sub-select 3 years
        fund_3y = fund_cal.loc[start_date_3y:end_date_3y].copy()
        fund_3y_norm = fund_3y["nav_value"].divide(fund_3y["nav_value"].iloc[0]).subtract(1).multiply(100)
        
        # Align returns for Tracking Error calculation on trading days
        fund_returns_3y = fund_3y["nav_value"].pct_change().dropna()
        nifty_returns_3y = nifty_prices["NIFTY100"].pct_change().dropna()
        
        aligned_3y = pd.concat([fund_returns_3y, nifty_returns_3y], axis=1, join="inner").dropna()
        aligned_3y.columns = ["fund", "nifty"]
        
        # Tracking Error = std(fund_return - nifty_return) * sqrt(252)
        diff_returns = aligned_3y["fund"] - aligned_3y["nifty"]
        tracking_error = diff_returns.std() * np.sqrt(252) * 100 # In percentage
        
        fund_name = df_metrics[df_metrics["amfi_code"] == amfi_code]["scheme_name"].values[0]
        short_name = fund_name[:30] + "..." if len(fund_name) > 30 else fund_name
        
        plt.plot(fund_3y_norm.index, fund_3y_norm, label=f"{short_name} (TE: {tracking_error:.2f}%)")
        
    plt.title("Cumulative 3-Year Performance of Top 5 Funds vs Nifty Benchmarks (2023-2026)", fontsize=13, fontweight="bold")
    plt.xlabel("Date")
    plt.ylabel("Cumulative Returns (%)")
    plt.legend(loc="upper left", fontsize=9)
    plt.tight_layout()
    
    chart_path = FIG_DIR / "benchmark_comparison.png"
    plt.savefig(chart_path, dpi=150)
    plt.close()
    log.info("Saved benchmark_comparison.png -> %s", chart_path.name)
    
    conn.close()
    return df_metrics


def create_analytics_notebook():
    """Generates notebooks/Performance_Analytics.ipynb with formatted markdown and code cells."""
    log.info("Creating Performance_Analytics.ipynb Jupyter Notebook...")
    
    cells = []
    
    # 1. Title cell
    cells.append({
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "# Bluestock Mutual Fund Capstone — Day 4: Performance Analytics & Scoring\n",
            "This notebook calculates advanced risk-adjusted performance statistics for all 40 schemes, including:\n",
            "- **Daily Returns & Validation**: Computation and verification of returns.\n",
            "- **CAGR Comparisons**: Annualized returns over 1-Year, 3-Year, and 5-Year (4.4-Year data limit) horizons.\n",
            "- **Sharpe and Sortino Ratios**: Risk-adjusted returns (using daily RBI repo proxy of 6.5% risk-free rate).\n",
            "- **Alpha and Beta Regression**: OLS regression against Nifty 100.\n",
            "- **Maximum Drawdowns**: Minimum cumulative peak-to-trough returns and worst date ranges.\n",
            "- **Fund Scorecard**: A composite scoring ranking system (0-100)."
        ]
    })
    
    # 2. Setup cell
    cells.append({
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "source": [
            "import os\n",
            "import sqlite3\n",
            "import pandas as pd\n",
            "import numpy as np\n",
            "from scipy import stats\n",
            "import matplotlib.pyplot as plt\n",
            "import seaborn as sns\n\n",
            "sns.set_theme(style='whitegrid')\n",
            "db_path = '../data/db/bluestock_mf.db'\n",
            "conn = sqlite3.connect(db_path)\n",
            "print('Connected to SQLite Database successfully!')"
        ]
    })
    
    # 3. Daily returns section
    cells.append({
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## 1. Daily Returns Calculation & Distribution\n",
            "Calculating daily percentage changes of fund NAVs on trading business days and plotting returns distributions."
        ]
    })
    
    # 4. Daily returns code
    cells.append({
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "source": [
            "# Load daily NAVs excluding weekends\n",
            "sql_nav = '''\n",
            "SELECT n.nav_date, n.nav_value, n.amfi_code, f.scheme_name\n",
            "FROM fact_nav n\n",
            "JOIN dim_fund f ON n.amfi_code = f.amfi_code\n",
            "JOIN dim_date d ON n.nav_date = d.date_id\n",
            "WHERE d.is_weekend = 0\n",
            "ORDER BY n.amfi_code, n.nav_date\n",
            "'''\n",
            "df_nav = pd.read_sql_query(sql_nav, conn)\n",
            "df_nav['nav_date'] = pd.to_datetime(df_nav['nav_date'])\n\n",
            "# Calculate daily returns for a sample fund\n",
            "sample_code = 119551 # SBI Bluechip\n",
            "sample_nav = df_nav[df_nav['amfi_code'] == sample_code].copy()\n",
            "sample_nav['daily_return'] = sample_nav['nav_value'].pct_change()\n\n",
            "# Plotting distribution\n",
            "plt.figure(figsize=(10, 4))\n",
            "sns.histplot(sample_nav['daily_return'].dropna(), bins=60, kde=True, color='indigo')\n",
            "plt.title(f'Daily Returns Distribution — {sample_nav[\"scheme_name\"].iloc[0]}', fontsize=12, fontweight='bold')\n",
            "plt.xlabel('Daily Return')\n",
            "plt.ylabel('Frequency')\n",
            "plt.show()\n\n",
            "# Distribution statistics\n",
            "print(sample_nav['daily_return'].describe())"
        ]
    })
    
    # 5. CAGR Section
    cells.append({
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## 2. Compounding Annual Growth Rate (CAGR) Comparison\n",
            "CAGR is calculated as: $CAGR = (NAV_{end} / NAV_{start}) ^ {(1/n)} - 1$. ",
            "We compile 1-Year, 3-Year, and Inception (4.4-Year) comparison tables for all 40 funds. Note that the 5-Year CAGR is reported as `NaN` due to data limits."
        ]
    })
    
    # 6. CAGR code
    cells.append({
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "source": [
            "# Load scorecard and print top 10 funds based on 3-Year CAGR\n",
            "df_scorecard = pd.read_csv('../fund_scorecard.csv')\n",
            "print('Top 10 Funds by 3-Year CAGR:')\n",
            "display(df_scorecard[['amfi_code', 'scheme_name', 'cagr_3yr']].head(10))"
        ]
    })
    
    # 7. Risk Ratios
    cells.append({
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## 3. Sharpe & Sortino Ratios (Risk-Adjusted Performance)\n",
            "- **Sharpe Ratio**: $(R_p - R_f) / Std(R_p) \\times \\sqrt{252}$ using risk-free rate $R_f = 6.5\\%$.\n",
            "- **Sortino Ratio**: Denominator uses downside standard deviation (focusing on negative return days only)."
        ]
    })
    
    # 8. Risk Ratios code
    cells.append({
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "source": [
            "print('Top 10 Funds by Sharpe Ratio:')\n",
            "display(df_scorecard[['amfi_code', 'scheme_name', 'sharpe_ratio']].sort_values('sharpe_ratio', ascending=False).head(10))"
        ]
    })
    
    # 9. Alpha & Beta
    cells.append({
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## 4. Alpha & Beta Regression Analysis\n",
            "Computing linear regression parameters using Nifty 100 as the market index proxy. "
        ]
    })
    
    # 10. Alpha Beta code
    cells.append({
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "source": [
            "df_alpha_beta = pd.read_csv('../alpha_beta.csv')\n",
            "print('Sample Alpha/Beta coefficients:')\n",
            "display(df_alpha_beta.head(10))"
        ]
    })
    
    # 11. Max Drawdown
    cells.append({
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## 5. Maximum Drawdown & Worst Date Ranges\n",
            "Calculating the peak-to-trough drop: $Drawdown = NAV_t / Cummax(NAV) - 1$. "
        ]
    })
    
    # 12. Max DD code
    cells.append({
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "source": [
            "print('Top 5 funds with the smallest maximum drawdown (most defensive):')\n",
            "display(df_scorecard[['amfi_code', 'scheme_name', 'max_drawdown']].sort_values('max_drawdown', ascending=False).head(5))"
        ]
    })

    # 13. Scorecard
    cells.append({
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## 6. Composite Fund Scorecard & Rankings\n",
            "Composite scorecard rank from 0-100: `30% × 3yr return rank + 25% × Sharpe rank + 20% × Alpha rank + 15% × expense ratio rank (inverse) + 10% × max DD rank (inverse)`."
        ]
    })
    
    # 14. Scorecard code
    cells.append({
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "source": [
            "print('Overall Fund Leaderboard (Composite Score):')\n",
            "display(df_scorecard[['amfi_code', 'scheme_name', 'composite_score']].head(10))"
        ]
    })

    # 15. Benchmark chart
    cells.append({
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## 7. Benchmark Comparison Chart & Tracking Error\n",
            "Visualizing Top 5 funds relative to Nifty 50 and Nifty 100 with annualized Tracking Error: $TE = Std(R_p - R_m) \\times \\sqrt{252}$."
        ]
    })
    
    # 16. Benchmark chart code
    cells.append({
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "source": [
            "# Display the generated figure\n",
            "from IPython.display import Image, display as ipy_display\n",
            "fig_path = '../reports/figures/benchmark_comparison.png'\n",
            "if os.path.exists(fig_path):\n",
            "    ipy_display(Image(filename=fig_path))\n",
            "else:\n",
            "    print('Benchmark chart figure not found!')\n\n",
            "# Close connection\n",
            "conn.close()"
        ]
    })
    
    # Build notebook structure
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
    try:
        compute_analytics()
        create_analytics_notebook()
        log.info("Day 4 Fund Performance Analytics completed successfully! OK")
    except Exception as e:
        log.error("Fatal error during Day 4 execution: %s", e)
        raise e


if __name__ == "__main__":
    main()

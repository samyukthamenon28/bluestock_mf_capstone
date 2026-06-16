"""
app.py — Bluestock Mutual Fund Capstone: Premium Financial Terminal (B2, B3, B4)
An interactive financial terminal dashboard overriding default Streamlit styles.
Features a cyber-dark glassmorphism design, unified Plotly themes, and advanced risk simulations.
"""

import os
import sqlite3
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from pathlib import Path
from datetime import datetime

# ── Paths ──────────────────────────────────────────────────────────────────────
ROOT = Path(__file__).resolve().parent.parent
DB_PATH = ROOT / "data" / "db" / "bluestock_mf.db"
SCORECARD_PATH = ROOT / "fund_scorecard.csv"
ALPHA_BETA_PATH = ROOT / "alpha_beta.csv"

# ── Page Configuration ──────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Bluestock Terminal",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Custom CSS for Premium Financial Terminal Design ───────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Space+Grotesk:wght@300;400;600;700&display=swap');
    
    /* Global Styles */
    html, body, [class*="css"] {
        font-family: 'Space Grotesk', sans-serif;
    }
    
    /* App Background Gradient */
    [data-testid="stAppViewContainer"] {
        background: radial-gradient(circle at 80% 20%, rgba(124, 58, 237, 0.08) 0%, rgba(8, 9, 12, 1) 75%) !important;
        color: #e2e8f0 !important;
    }
    
    /* Hide Default Header/Footer */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #0b0c10 !important;
        border-right: 1px solid rgba(139, 92, 246, 0.15) !important;
    }
    
    /* Header Card */
    .terminal-header {
        background: linear-gradient(135deg, rgba(20, 21, 33, 0.95) 0%, rgba(10, 11, 22, 0.95) 100%);
        border: 1px solid rgba(139, 92, 246, 0.25);
        border-radius: 12px;
        padding: 2rem;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
    }
    
    .terminal-header h1 {
        margin: 0;
        font-size: 2.2rem;
        font-weight: 700;
        color: #ffffff;
        letter-spacing: -0.03em;
        text-shadow: 0 0 10px rgba(139, 92, 246, 0.3);
    }
    
    .terminal-header p {
        margin: 0.5rem 0 0 0;
        color: #94a3b8;
        font-size: 1.05rem;
    }
    
    /* Cyber KPI Card */
    .kpi-card-cyber {
        background: linear-gradient(135deg, rgba(22, 25, 41, 0.8) 0%, rgba(15, 17, 28, 0.8) 100%);
        border: 1px solid rgba(6, 182, 212, 0.2);
        border-radius: 10px;
        padding: 18px;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 20px rgba(6, 182, 212, 0.03);
        transition: all 0.3s ease;
    }
    
    .kpi-card-cyber:hover {
        border-color: rgba(6, 182, 212, 0.5);
        box-shadow: 0 4px 25px rgba(6, 182, 212, 0.15);
        transform: translateY(-2px);
    }
    
    .kpi-label {
        font-size: 11px;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: #94a3b8;
        font-weight: 600;
    }
    
    .kpi-val {
        font-size: 20px;
        font-weight: 700;
        color: #06b6d4;
        font-family: 'Share Tech Mono', monospace;
        margin-top: 6px;
        text-shadow: 0 0 8px rgba(6, 182, 212, 0.2);
    }
    
    /* Input Widget Custom Overrides */
    .stSelectbox div[data-baseweb="select"] {
        background-color: #12131a !important;
        border: 1px solid rgba(139, 92, 246, 0.2) !important;
        color: #ffffff !important;
    }
    
    .stMultiSelect div[role="combobox"] {
        background-color: #12131a !important;
        border: 1px solid rgba(139, 92, 246, 0.2) !important;
    }
    
    /* Custom tab headers */
    .stTabs [data-baseweb="tab-list"] {
        background-color: transparent !important;
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #12131a !important;
        border: 1px solid rgba(139, 92, 246, 0.1) !important;
        border-radius: 6px 6px 0 0 !important;
        color: #94a3b8 !important;
        padding: 10px 20px !important;
    }
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background-color: #1c1d29 !important;
        border-color: rgba(139, 92, 246, 0.4) !important;
        color: #06b6d4 !important;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)


# ── Plotly Unified Dark styling Helper ─────────────────────────────────────────

def style_plotly_figure(fig, title_text=None):
    """Applies a custom dark-glass themed layout to a Plotly figure."""
    fig.update_layout(
        paper_bgcolor='rgba(18, 19, 26, 0.5)',
        plot_bgcolor='rgba(0, 0, 0, 0)',
        font=dict(color='#cbd5e1', family='Space Grotesk, sans-serif'),
        title=dict(
            text=title_text, 
            font=dict(size=15, color='#ffffff', family='Space Grotesk, sans-serif')
        ) if title_text else None,
        xaxis=dict(
            gridcolor='rgba(255, 255, 255, 0.04)',
            zerolinecolor='rgba(255, 255, 255, 0.08)',
            tickfont=dict(color='#94a3b8')
        ),
        yaxis=dict(
            gridcolor='rgba(255, 255, 255, 0.04)',
            zerolinecolor='rgba(255, 255, 255, 0.08)',
            tickfont=dict(color='#94a3b8')
        ),
        legend=dict(
            bgcolor='rgba(11, 12, 16, 0.8)',
            bordercolor='rgba(255, 255, 255, 0.05)',
            borderwidth=1,
            font=dict(color='#cbd5e1')
        ),
        margin=dict(l=40, r=40, t=60, b=40)
    )
    return fig


# ── Database & CSV Loaders ──────────────────────────────────────────────────────

def get_connection():
    """Create SQLite database connection."""
    return sqlite3.connect(DB_PATH)


@st.cache_data
def load_scorecard():
    """Load calculated performance scorecard csv."""
    if SCORECARD_PATH.exists():
        return pd.read_csv(SCORECARD_PATH)
    else:
        st.error("fund_scorecard.csv not found. Please run scripts/generate_analytics.py first.")
        return pd.DataFrame()


@st.cache_data
def load_alpha_beta():
    """Load regression table results."""
    if ALPHA_BETA_PATH.exists():
        return pd.read_csv(ALPHA_BETA_PATH)
    return pd.DataFrame()


@st.cache_data
def load_nav_history(amfi_codes=None):
    """Load NAV history, reindexed to daily business calendars."""
    conn = get_connection()
    if amfi_codes:
        # Cast to standard python int because SQLite's python adapter doesn't always support numpy.int64 types on Windows.
        casted_codes = [int(c) for c in amfi_codes]
        placeholders = ",".join("?" for _ in casted_codes)
        query = f"""
            SELECT n.nav_date, n.nav_value, n.amfi_code, f.scheme_name, f.fund_house
            FROM fact_nav n
            JOIN dim_fund f ON n.amfi_code = f.amfi_code
            WHERE n.amfi_code IN ({placeholders})
            ORDER BY n.nav_date
        """
        df = pd.read_sql_query(query, conn, params=casted_codes)
    else:
        query = """
            SELECT n.nav_date, n.nav_value, n.amfi_code, f.scheme_name, f.fund_house
            FROM fact_nav n
            JOIN dim_fund f ON n.amfi_code = f.amfi_code
            ORDER BY n.nav_date
        """
        df = pd.read_sql_query(query, conn)
    conn.close()
    df["nav_date"] = pd.to_datetime(df["nav_date"])
    return df


@st.cache_data
def load_index_history():
    """Load benchmark index prices."""
    conn = get_connection()
    query = """
        SELECT date, index_name, close_value 
        FROM benchmark_indices
        WHERE index_name IN ('NIFTY50', 'NIFTY100')
        ORDER BY date
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    df["date"] = pd.to_datetime(df["date"])
    return df


@st.cache_data
def load_demographics_data():
    """Load transaction datasets."""
    conn = get_connection()
    query = """
        SELECT age_group, gender, state, city_tier, amount_inr, transaction_type
        FROM fact_transactions
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df


@st.cache_data
def load_industry_aum():
    """Load fund house total AUM growth."""
    conn = get_connection()
    df = pd.read_sql_query("SELECT aum_date, fund_house, aum_lakh_crore, aum_crore, num_schemes FROM fact_aum", conn)
    conn.close()
    df["aum_date"] = pd.to_datetime(df["aum_date"])
    return df


@st.cache_data
def load_sip_inflows():
    """Load SIP inflows."""
    conn = get_connection()
    df = pd.read_sql_query("SELECT month, sip_inflow_crore, active_sip_accounts_crore, new_sip_accounts_lakh FROM monthly_sip_inflows", conn)
    conn.close()
    return df


@st.cache_data
def load_category_inflows():
    """Load category inflows."""
    conn = get_connection()
    df = pd.read_sql_query("SELECT month, category, net_inflow_crore FROM category_inflows", conn)
    conn.close()
    return df


@st.cache_data
def load_folio_growth():
    """Load folio count."""
    conn = get_connection()
    df = pd.read_sql_query("SELECT month, total_folios_crore, equity_folios_crore, debt_folios_crore FROM industry_folio_count", conn)
    conn.close()
    return df


@st.cache_data
def load_portfolio_sectors(amfi_code):
    """Load sector details for donut charts."""
    conn = get_connection()
    query = """
        SELECT sector, SUM(weight_pct) as weight_pct
        FROM portfolio_holdings
        WHERE amfi_code = ?
        GROUP BY sector
        ORDER BY weight_pct DESC
    """
    df = pd.read_sql_query(query, conn, params=(int(amfi_code),))
    conn.close()
    return df


def compute_rolling_sharpe(df_nav_selected, window=90):
    """Compute rolling Sharpe ratios for dynamic comparison."""
    rolling_series = []
    for name, group in df_nav_selected.groupby("scheme_name"):
        group = group.sort_values("nav_date").set_index("nav_date")
        if group.empty or pd.isna(group.index.min()) or pd.isna(group.index.max()):
            continue
        full_range = pd.date_range(group.index.min(), group.index.max(), freq="D")
        group = group.reindex(full_range).ffill().bfill()
        
        trading = group[group.index.dayofweek < 5].copy()
        trading["returns"] = trading["nav_value"].pct_change()
        returns = trading["returns"].dropna()
        
        rolling_mean = returns.rolling(window).mean()
        rolling_std = returns.rolling(window).std()
        rolling_sharpe = (rolling_mean / rolling_std) * np.sqrt(252)
        
        df_rs = pd.DataFrame(rolling_sharpe).reset_index()
        df_rs.columns = ["Date", "Rolling Sharpe"]
        df_rs["Scheme Name"] = name
        rolling_series.append(df_rs)
        
    if rolling_series:
        return pd.concat(rolling_series).dropna()
    return pd.DataFrame()


@st.cache_data
def load_var_cvar_report():
    """Load precalculated 95% VaR & CVaR report."""
    report_path = ROOT / "var_cvar_report.csv"
    if report_path.exists():
        return pd.read_csv(report_path)
    return pd.DataFrame()


@st.cache_data
def load_cohort_analysis():
    """Calculate investor cohorts based on first transaction year."""
    conn = get_connection()
    df_trans = pd.read_sql_query("""
        SELECT t.investor_id, t.transaction_date, t.amount_inr, t.transaction_type, f.scheme_name
        FROM fact_transactions t
        JOIN dim_fund f ON t.amfi_code = f.amfi_code
    """, conn)
    conn.close()
    
    df_trans["transaction_date"] = pd.to_datetime(df_trans["transaction_date"])
    df_first = df_trans.groupby("investor_id")["transaction_date"].min().reset_index()
    df_first.rename(columns={"transaction_date": "first_transaction_date"}, inplace=True)
    df_first["cohort_year"] = df_first["first_transaction_date"].dt.year
    
    df_trans_cohort = df_trans.merge(df_first[["investor_id", "cohort_year"]], on="investor_id")
    cohorts = df_trans_cohort["cohort_year"].unique()
    cohort_results = []
    
    for yr in sorted(cohorts):
        cohort_df = df_trans_cohort[df_trans_cohort["cohort_year"] == yr]
        sip_df = cohort_df[cohort_df["transaction_type"] == "SIP"]
        avg_sip = sip_df["amount_inr"].mean() if not sip_df.empty else 0.0
        invest_df = cohort_df[cohort_df["transaction_type"].isin(["SIP", "Lumpsum"])]
        total_inv = invest_df["amount_inr"].sum()
        
        if not cohort_df.empty:
            top_fund = cohort_df["scheme_name"].value_counts().idxmax()
        else:
            top_fund = "N/A"
            
        cohort_results.append({
            "Cohort Year": int(yr),
            "Avg. SIP Amount (₹)": avg_sip,
            "Total Invested (₹ Cr)": total_inv / 1e7,
            "Top Fund Preference": top_fund
        })
    return pd.DataFrame(cohort_results)


@st.cache_data
def load_sip_continuity():
    """Calculate SIP gaps and flag at-risk investors."""
    conn = get_connection()
    df_trans = pd.read_sql_query("""
        SELECT investor_id, transaction_date, transaction_type
        FROM fact_transactions
        WHERE transaction_type = 'SIP'
    """, conn)
    conn.close()
    
    df_trans["transaction_date"] = pd.to_datetime(df_trans["transaction_date"])
    sip_counts = df_trans["investor_id"].value_counts()
    eligible_investors = sip_counts[sip_counts >= 6].index.tolist()
    
    at_risk_count = 0
    total_eligible = len(eligible_investors)
    
    for inv_id in eligible_investors:
        inv_sip = df_trans[df_trans["investor_id"] == inv_id].copy()
        inv_sip.sort_values("transaction_date", inplace=True)
        gaps = inv_sip["transaction_date"].diff().dt.days.dropna()
        if len(gaps) > 0:
            avg_gap = gaps.mean()
            if avg_gap > 35:
                at_risk_count += 1
                
    at_risk_rate = (at_risk_count / total_eligible) * 100 if total_eligible > 0 else 0.0
    continuity_rate = 100 - at_risk_rate
    return total_eligible, at_risk_count, continuity_rate


@st.cache_data
def load_hhi_concentration():
    """Calculate Sector and Stock HHI for all equity funds."""
    conn = get_connection()
    df_holdings = pd.read_sql_query("""
        SELECT p.amfi_code, p.sector, p.weight_pct, f.scheme_name
        FROM portfolio_holdings p
        JOIN dim_fund f ON p.amfi_code = f.amfi_code
        WHERE f.category = 'Equity'
    """, conn)
    conn.close()
    
    hhi_results = []
    equity_codes = df_holdings["amfi_code"].unique()
    
    for code in equity_codes:
        fund_hld = df_holdings[df_holdings["amfi_code"] == code]
        scheme_name = fund_hld["scheme_name"].iloc[0]
        
        sector_weights = fund_hld.groupby("sector")["weight_pct"].sum()
        sector_hhi = np.sum(sector_weights ** 2)
        stock_hhi = np.sum(fund_hld["weight_pct"] ** 2)
        
        hhi_results.append({
            "AMFI Code": int(code),
            "Scheme Name": scheme_name,
            "Sector HHI": sector_hhi,
            "Stock HHI": stock_hhi
        })
    return pd.DataFrame(hhi_results).sort_values("Sector HHI", ascending=False)


def get_recommendations_df(risk_appetite: str):
    """Retrieve top 3 funds sorted by Sharpe ratio matching the selected risk profile."""
    risk_appetite = risk_appetite.strip().lower()
    if risk_appetite == "low":
        grades = ["Low"]
    elif risk_appetite == "moderate":
        grades = ["Moderate", "Moderately High"]
    elif risk_appetite == "high":
        grades = ["High", "Very High"]
    else:
        return pd.DataFrame()
        
    conn = get_connection()
    placeholders = ",".join("?" for _ in grades)
    query = f"""
        SELECT f.amfi_code, f.scheme_name, f.fund_house, p.risk_grade, p.sharpe_ratio, p.return_3yr_pct
        FROM dim_fund f
        JOIN fact_performance p ON f.amfi_code = p.amfi_code
        WHERE p.risk_grade IN ({placeholders})
        ORDER BY p.sharpe_ratio DESC
        LIMIT 3
    """
    df = pd.read_sql_query(query, conn, params=grades)
    conn.close()
    return df


# ── Navigation Sidebar ─────────────────────────────────────────────────────────

st.sidebar.markdown(
    "<h2 style='text-align: center; color: #a78bfa; font-weight:700; font-family:\"Space Grotesk\";'>BLUESTOCK</h2>", 
    unsafe_allow_html=True
)
st.sidebar.markdown("<p style='text-align: center; color: #64748b; font-size: 0.85rem; margin-top:-10px;'>Quantitative Analytics Terminal</p>", unsafe_allow_html=True)
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Navigation Workspace",
    [
        "Fund Scorecard & Benchmark",
        "NAV Analysis & Correlation",
        "Industry & AUM Growth",
        "Investor Demographics",
        "Advanced Simulation & Optimization",
        "Advanced Risk & Cohort Analytics"
    ]
)

# ── Load Core Data ─────────────────────────────────────────────────────────────
df_scorecard = load_scorecard()
df_ab = load_alpha_beta()


# ── Page 1: Fund Scorecard & Benchmark ──────────────────────────────────────────

if page == "Fund Scorecard & Benchmark":
    st.markdown("""
        <div class="terminal-header">
            <h1>Mutual Fund Scorecard & Benchmark Analysis</h1>
            <p>Interactive leaderboard ranking funds based on annualized CAGRs, Sharpe/Sortino ratios, Alpha, Beta, and drawdowns.</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Page-Level Slicers (At least 2 required)
    st.markdown("### Filters")
    col_f1, col_f2, col_f3 = st.columns(3)
    with col_f1:
        f_fund_house = st.selectbox("Select Fund House", ["All"] + list(df_scorecard["fund_house"].unique()))
    with col_f2:
        f_min_score = st.slider("Minimum Composite Score (0-100)", 0.0, 100.0, 0.0, 1.0)
    with col_f3:
        conn = get_connection()
        cats = pd.read_sql_query("SELECT DISTINCT category FROM dim_fund", conn)["category"].tolist()
        conn.close()
        f_category = st.multiselect("Select Fund Category", cats, default=cats)
        
    # Apply Filters
    df_filtered = df_scorecard.copy()
    conn = get_connection()
    df_dim_fund = pd.read_sql_query("SELECT amfi_code, category FROM dim_fund", conn)
    conn.close()
    df_filtered = df_filtered.merge(df_dim_fund, on="amfi_code")
    
    if f_fund_house != "All":
        df_filtered = df_filtered[df_filtered["fund_house"] == f_fund_house]
    df_filtered = df_filtered[df_filtered["composite_score"] >= f_min_score]
    df_filtered = df_filtered[df_filtered["category"].isin(f_category)]
    
    # Render Cyber KPIs
    if not df_filtered.empty:
        col_m1, col_m2, col_m3, col_m4 = st.columns(4)
        with col_m1:
            st.markdown(f"""
                <div class="kpi-card-cyber">
                    <div class="kpi-label">Terminal Leader</div>
                    <div class="kpi-val" style="color: #a78bfa; font-size:15px;">{df_filtered.iloc[0]['scheme_name'][:25]}...</div>
                </div>
            """, unsafe_allow_html=True)
        with col_m2:
            st.markdown(f"""
                <div class="kpi-card-cyber">
                    <div class="kpi-label">Avg. 3-Year CAGR</div>
                    <div class="kpi-val">{(df_filtered['cagr_3y'].mean()*100):.2f}%</div>
                </div>
            """, unsafe_allow_html=True)
        with col_m3:
            st.markdown(f"""
                <div class="kpi-card-cyber">
                    <div class="kpi-label">Avg. Sharpe Ratio</div>
                    <div class="kpi-val">{df_filtered['sharpe_ratio'].mean():.2f}</div>
                </div>
            """, unsafe_allow_html=True)
        with col_m4:
            st.markdown(f"""
                <div class="kpi-card-cyber">
                    <div class="kpi-label">Listed Funds</div>
                    <div class="kpi-val">{len(df_filtered)} / 40</div>
                </div>
            """, unsafe_allow_html=True)
            
    # Leaderboard Table
    st.markdown("### Overall Scoreboard Ranking")
    df_display = df_filtered[[
        "amfi_code", "scheme_name", "fund_house", "category", "cagr_3y", "sharpe_ratio", "alpha", 
        "expense_ratio_pct", "max_drawdown", "composite_score"
    ]].copy()
    
    df_display.columns = [
        "AMFI Code", "Scheme Name", "Fund House", "Category", "3-Year CAGR", "Sharpe Ratio", "Alpha (Annual)", 
        "Expense Ratio (%)", "Max Drawdown", "Composite Score (0-100)"
    ]
    
    st.dataframe(
        df_display.style.format({
            "3-Year CAGR": "{:.2%}",
            "Sharpe Ratio": "{:.2f}",
            "Alpha (Annual)": "{:.4f}",
            "Expense Ratio (%)": "{:.2f}%",
            "Max Drawdown": "{:.2%}",
            "Composite Score (0-100)": "{:.2f}"
        }),
        use_container_width=True,
        hide_index=True
    )
    
    # Dynamic Benchmark Comparison & Tracking Error
    st.markdown("---")
    st.markdown("### Dynamic Benchmark Comparison & Tracking Error")
    
    col_b1, col_b2, col_b3 = st.columns(3)
    with col_b1:
        selected_funds = st.multiselect(
            "Select Funds (Up to 5)", 
            options=df_scorecard["scheme_name"].tolist(),
            default=df_scorecard["scheme_name"].head(3).tolist()
        )
    with col_b2:
        benchmark_name = st.selectbox("Select Index Benchmark", ["NIFTY100", "NIFTY50"])
    with col_b3:
        start_date_slider = st.date_input("Start Date", datetime(2023, 5, 29))
        end_date_slider = st.date_input("End Date", datetime(2026, 5, 29))
        
    if len(selected_funds) > 5:
        st.warning("Please select a maximum of 5 funds.")
    elif len(selected_funds) == 0:
        st.info("Select at least 1 fund to compare returns.")
    else:
        selected_codes = df_scorecard[df_scorecard["scheme_name"].isin(selected_funds)]["amfi_code"].tolist()
        df_navs = load_nav_history(selected_codes)
        df_indices = load_index_history()
        
        start_dt = pd.to_datetime(start_date_slider)
        end_dt = pd.to_datetime(end_date_slider)
        
        df_navs_f = df_navs[(df_navs["nav_date"] >= start_dt) & (df_navs["nav_date"] <= end_dt)]
        df_indices_f = df_indices[(df_indices["date"] >= start_dt) & (df_indices["date"] <= end_dt)]
        if df_navs_f.empty or df_indices_f.empty:
            st.error("No trading data found for the selected range.")
        else:
            df_ind_pivot = df_indices_f.pivot(index="date", columns="index_name", values="close_value")
            if df_ind_pivot.empty or pd.isna(df_ind_pivot.index.min()) or pd.isna(df_ind_pivot.index.max()):
                st.error("No trading data found for the selected benchmark in this range.")
                st.stop()
            df_ind_pivot = df_ind_pivot.reindex(pd.date_range(df_ind_pivot.index.min(), df_ind_pivot.index.max(), freq='D')).ffill().bfill()
            idx_norm = df_ind_pivot[benchmark_name].divide(df_ind_pivot[benchmark_name].iloc[0]).subtract(1).multiply(100)
            
            fig_compare = go.Figure()
            fig_compare.add_trace(go.Scatter(
                x=idx_norm.index,
                y=idx_norm,
                name=f"{benchmark_name} (Benchmark)",
                line=dict(color="#f43f5e", width=2, dash="dash")
            ))
            
            for code in selected_codes:
                fund_df = df_navs_f[df_navs_f["amfi_code"] == code].copy()
                fund_df.set_index("nav_date", inplace=True)
                fund_df.sort_index(inplace=True)
                
                if fund_df.empty or pd.isna(fund_df.index.min()) or pd.isna(fund_df.index.max()):
                    continue
                
                # Reindex & forward fill holidays
                full_range = pd.date_range(fund_df.index.min(), fund_df.index.max(), freq="D")
                fund_df = fund_df.reindex(full_range).ffill().bfill()
                
                fund_norm = fund_df["nav_value"].divide(fund_df["nav_value"].iloc[0]).subtract(1).multiply(100)
                
                # Exclude weekends for daily return analytics
                fund_days = fund_df[fund_df.index.dayofweek < 5].copy()
                fund_returns = fund_days["nav_value"].pct_change().dropna()
                
                idx_days = df_ind_pivot[df_ind_pivot.index.dayofweek < 5].copy()
                idx_returns = idx_days[benchmark_name].pct_change().dropna()
                
                aligned = pd.concat([fund_returns, idx_returns], axis=1, join="inner").dropna()
                aligned.columns = ["fund", "benchmark"]
                
                # Tracking Error
                diff = aligned["fund"] - aligned["benchmark"]
                tracking_error = diff.std() * np.sqrt(252) * 100
                
                f_name = df_scorecard[df_scorecard["amfi_code"] == code]["scheme_name"].values[0]
                short_name = f_name[:28] + "..." if len(f_name) > 30 else f_name
                
                fig_compare.add_trace(go.Scatter(
                    x=fund_norm.index,
                    y=fund_norm,
                    name=f"{short_name} (TE: {tracking_error:.2f}%)",
                    line=dict(width=2)
                ))
                
            fig_compare = style_plotly_figure(fig_compare, f"Cumulative Returns vs {benchmark_name}")
            fig_compare.update_layout(
                yaxis_title="Cumulative Return (%)",
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                hovermode="x unified"
            )
            st.plotly_chart(fig_compare, use_container_width=True)


# ── Page 2: NAV Analysis & Correlation ──────────────────────────────────────────

elif page == "NAV Analysis & Correlation":
    st.markdown("""
        <div class="terminal-header">
            <h1>NAV Historical Trends & Asset Correlations</h1>
            <p>View daily NAV timelines, overlay event horizons, query return correlations, and verify sector weights.</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### Filters")
    col_n1, col_n2, col_n3 = st.columns(3)
    with col_n1:
        f_primary_fund = st.selectbox("Select Primary Fund", df_scorecard["scheme_name"].tolist())
    with col_n2:
        start_date = st.date_input("Trend Start Date", datetime(2022, 1, 3))
        end_date = st.date_input("Trend End Date", datetime(2026, 5, 29))
    with col_n3:
        highlight_bull = st.checkbox("Highlight 2023 Bull Run", value=True)
        highlight_corr = st.checkbox("Highlight 2024 Market Corrections", value=True)
        
    primary_code = df_scorecard[df_scorecard["scheme_name"] == f_primary_fund]["amfi_code"].values[0]
    
    df_navs = load_nav_history([primary_code])
    start_dt = pd.to_datetime(start_date)
    end_dt = pd.to_datetime(end_date)
    
    df_navs_f = df_navs[(df_navs["nav_date"] >= start_dt) & (df_navs["nav_date"] <= end_dt)].copy()
    df_navs_f.set_index("nav_date", inplace=True)
    df_navs_f.sort_index(inplace=True)
    
    if df_navs_f.empty or pd.isna(df_navs_f.index.min()) or pd.isna(df_navs_f.index.max()):
        st.error("No trading data found for the selected fund and range.")
        st.stop()
        
    # Reindex & ffill
    full_range = pd.date_range(df_navs_f.index.min(), df_navs_f.index.max(), freq="D")
    df_navs_f = df_navs_f.reindex(full_range).ffill().bfill()
    
    fig_nav = go.Figure()
    fig_nav.add_trace(go.Scatter(
        x=df_navs_f.index,
        y=df_navs_f["nav_value"],
        name="NAV Value",
        line=dict(color="#06b6d4", width=2)
    ))
    
    if highlight_bull:
        fig_nav.add_vrect(
            x0="2023-01-01", x1="2023-12-31",
            fillcolor="#a855f7", opacity=0.08,
            layer="below", line_width=0,
            annotation_text="2023 Bull Run",
            annotation_position="top left",
            annotation_font=dict(color="#a78bfa")
        )
    if highlight_corr:
        fig_nav.add_vrect(
            x0="2024-03-01", x1="2024-06-30",
            fillcolor="#ef4444", opacity=0.08,
            layer="below", line_width=0,
            annotation_text="2024 Corrections",
            annotation_position="top left",
            annotation_font=dict(color="#f87171")
        )
        
    fig_nav = style_plotly_figure(fig_nav, f"NAV Value Timeline — {f_primary_fund}")
    fig_nav.update_layout(yaxis_title="NAV (₹)", hovermode="x unified")
    
    col_chart1, col_chart2 = st.columns([2, 1])
    with col_chart1:
        st.plotly_chart(fig_nav, use_container_width=True)
    with col_chart2:
        st.markdown("### Sector Allocation")
        df_sectors = load_portfolio_sectors(primary_code)
        if df_sectors.empty:
            st.info("No holdings data available.")
        else:
            fig_sectors = px.pie(
                df_sectors,
                names="sector",
                values="weight_pct",
                hole=0.5,
                color_discrete_sequence=px.colors.qualitative.Prism
            )
            fig_sectors = style_plotly_figure(fig_sectors)
            fig_sectors.update_layout(
                margin=dict(l=10, r=10, t=10, b=10),
                legend=dict(orientation="h", y=-0.1)
            )
            st.plotly_chart(fig_sectors, use_container_width=True)
            
    # Daily Returns Heatmap
    st.markdown("---")
    st.markdown("### Pairwise Return Correlation Heatmap")
    
    col_c1, col_c2 = st.columns(2)
    with col_c1:
        selected_corr_funds = st.multiselect(
            "Select 10 Funds for Heatmap Analysis",
            options=df_scorecard["scheme_name"].tolist(),
            default=df_scorecard["scheme_name"].head(10).tolist()
        )
    with col_c2:
        corr_date_range = st.date_input("Correlation Window", [datetime(2022, 1, 3), datetime(2026, 5, 29)])
        
    if len(selected_corr_funds) < 2:
        st.info("Please select at least 2 funds.")
    else:
        corr_codes = df_scorecard[df_scorecard["scheme_name"].isin(selected_corr_funds)]["amfi_code"].tolist()
        df_all_navs = load_nav_history(corr_codes)
        
        if len(corr_date_range) == 2:
            c_start, c_end = pd.to_datetime(corr_date_range[0]), pd.to_datetime(corr_date_range[1])
            df_all_navs = df_all_navs[(df_all_navs["nav_date"] >= c_start) & (df_all_navs["nav_date"] <= c_end)]
            
        df_pivot_navs = df_all_navs.pivot(index="nav_date", columns="scheme_name", values="nav_value")
        if df_pivot_navs.empty or pd.isna(df_pivot_navs.index.min()) or pd.isna(df_pivot_navs.index.max()):
            st.error("No NAV data found in the selected range to compute correlation matrix.")
            st.stop()
        df_pivot_navs = df_pivot_navs.reindex(pd.date_range(df_pivot_navs.index.min(), df_pivot_navs.index.max(), freq='D')).ffill().bfill()
        
        df_pivot_returns = df_pivot_navs[df_pivot_navs.index.dayofweek < 5].pct_change().dropna()
        corr_matrix = df_pivot_returns.corr()
        short_labels = [n[:18] + "..." if len(n) > 18 else n for n in corr_matrix.columns]
        
        fig_corr = go.Figure(data=go.Heatmap(
            z=corr_matrix.values,
            x=short_labels,
            y=short_labels,
            colorscale="Electric",
            zmin=-1, zmax=1,
            text=np.round(corr_matrix.values, 2),
            texttemplate="%{text}",
            hoverongaps=False
        ))
        
        fig_corr = style_plotly_figure(fig_corr, "Pairwise Correlation Matrix")
        fig_corr.update_layout(xaxis=dict(tickangle=-45), height=550)
        st.plotly_chart(fig_corr, use_container_width=True)


# ── Page 3: Industry & AUM Growth ──────────────────────────────────────────────

elif page == "Industry & AUM Growth":
    st.markdown("""
        <div class="terminal-header">
            <h1>Mutual Fund Industry Inflows & Total AUM</h1>
            <p>Industry-level statistics mapping asset growth, category trends, SIP collections, and total folio growth milestones.</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### Filters")
    col_a1, col_a2 = st.columns(2)
    with col_a1:
        df_aum = load_industry_aum()
        f_aum_houses = st.multiselect("Select Fund House Filter", options=list(df_aum["fund_house"].unique()), default=list(df_aum["fund_house"].unique()))
    with col_a2:
        f_years = st.slider("Select Year Horizon (2022-2025)", 2022, 2025, (2022, 2025))
        
    df_aum_f = df_aum[df_aum["fund_house"].isin(f_aum_houses)].copy()
    df_aum_f["year"] = df_aum_f["aum_date"].dt.year
    df_aum_f = df_aum_f[(df_aum_f["year"] >= f_years[0]) & (df_aum_f["year"] <= f_years[1])]
    
    st.markdown("### Total AUM Growth by Fund House (Highlighting SBI ₹12.5L Cr)")
    df_aum_grouped = df_aum_f.groupby(["year", "fund_house"])["aum_lakh_crore"].sum().reset_index()
    
    fig_aum = px.bar(
        df_aum_grouped,
        x="year",
        y="aum_lakh_crore",
        color="fund_house",
        barmode="group",
        labels={"aum_lakh_crore": "Total AUM (₹ Lakh Crore)", "year": "Year"},
        color_discrete_sequence=px.colors.qualitative.Vivid
    )
    
    fig_aum.add_annotation(
        x=2025,
        y=12.5,
        text="SBI Dominance: ₹12.5 Lakh Crore",
        showarrow=True,
        arrowhead=2,
        arrowcolor="#f43f5e",
        font=dict(size=12, color="#ffffff", weight="bold"),
        bgcolor="#f43f5e",
        opacity=0.9,
        ax=-70,
        ay=-35
    )
    
    fig_aum = style_plotly_figure(fig_aum)
    st.plotly_chart(fig_aum, use_container_width=True)
    
    st.markdown("---")
    col_sip, col_heat = st.columns(2)
    
    with col_sip:
        st.markdown("### Monthly SIP Inflow Time-Series")
        df_sip = load_sip_inflows()
        
        fig_sip = go.Figure()
        fig_sip.add_trace(go.Scatter(
            x=df_sip["month"],
            y=df_sip["sip_inflow_crore"],
            mode="lines+markers",
            line=dict(color="#10b981", width=2),
            marker=dict(size=6),
            name="SIP Inflow (₹ Crore)"
        ))
        
        fig_sip.add_annotation(
            x="2025-12",
            y=31002,
            text="Peak Inflow: ₹31,002 Cr (Dec 2025)",
            showarrow=True,
            arrowhead=2,
            arrowcolor="#10b981",
            font=dict(color="#ffffff", size=11, weight="bold"),
            bgcolor="#10b981",
            ax=-80,
            ay=-40
        )
        
        fig_sip = style_plotly_figure(fig_sip)
        fig_sip.update_layout(xaxis_title="Month", yaxis_title="SIP Inflow (₹ Crore)")
        st.plotly_chart(fig_sip, use_container_width=True)
        
    with col_heat:
        st.markdown("### Category Net Inflow Heatmap")
        df_cat = load_category_inflows()
        df_cat_pivot = df_cat.pivot(index="category", columns="month", values="net_inflow_crore")
        
        fig_cat = go.Figure(data=go.Heatmap(
            z=df_cat_pivot.values,
            x=df_cat_pivot.columns,
            y=df_cat_pivot.index,
            colorscale="Viridis",
            hoverongaps=False
        ))
        fig_cat = style_plotly_figure(fig_cat)
        fig_cat.update_layout(xaxis_title="Month", yaxis_title="Category")
        st.plotly_chart(fig_cat, use_container_width=True)
        
    st.markdown("---")
    st.markdown("### Folio Count Growth Milestones")
    df_folio = load_folio_growth()
    
    fig_folio = go.Figure()
    fig_folio.add_trace(go.Scatter(
        x=df_folio["month"],
        y=df_folio["total_folios_crore"],
        name="Total Folios (Cr)",
        line=dict(color="#8b5cf6", width=2.5)
    ))
    
    fig_folio.add_annotation(
        x="2022-01",
        y=13.26,
        text="Start: 13.26 Cr",
        showarrow=True,
        arrowhead=1,
        ax=45,
        ay=30
    )
    fig_folio.add_annotation(
        x="2025-12",
        y=26.12,
        text="Peak: 26.12 Cr",
        showarrow=True,
        arrowhead=1,
        ax=-45,
        ay=-30
    )
    
    fig_folio = style_plotly_figure(fig_folio)
    fig_folio.update_layout(xaxis_title="Month", yaxis_title="Folios Count (Crore)")
    st.plotly_chart(fig_folio, use_container_width=True)


# ── Page 4: Investor Demographics ──────────────────────────────────────────────

elif page == "Investor Demographics":
    st.markdown("""
        <div class="terminal-header">
            <h1>Investor Demographics & States</h1>
            <p>Visualizing transaction demography slices across Age, State distribution, City tiers, and Gender ratios.</p>
        </div>
    """, unsafe_allow_html=True)
    
    df_demo = load_demographics_data()
    
    st.markdown("### Filters")
    col_d1, col_d2, col_d3 = st.columns(3)
    with col_d1:
        f_state = st.multiselect("Select State Filter", options=["All"] + list(df_demo["state"].unique()), default="All")
    with col_d2:
        f_tier = st.selectbox("Select City Tier", ["All", "T30", "B30"])
    with col_d3:
        f_gender = st.selectbox("Select Gender", ["All", "Male", "Female"])
        
    df_demo_f = df_demo.copy()
    if "All" not in f_state and len(f_state) > 0:
        df_demo_f = df_demo_f[df_demo_f["state"].isin(f_state)]
    if f_tier != "All":
        df_demo_f = df_demo_f[df_demo_f["city_tier"] == f_tier]
    if f_gender != "All":
        df_demo_f = df_demo_f[df_demo_f["gender"] == f_gender]
        
    if df_demo_f.empty:
        st.warning("No rows match the filters.")
    else:
        col_c1, col_c2, col_c3 = st.columns(3)
        
        with col_c1:
            st.markdown("#### Age Group Distribution")
            df_age = df_demo_f["age_group"].value_counts().reset_index()
            fig_age = px.pie(df_age, names="age_group", values="count", color_discrete_sequence=px.colors.qualitative.Safe)
            fig_age = style_plotly_figure(fig_age)
            fig_age.update_layout(margin=dict(t=20, b=20, l=10, r=10))
            st.plotly_chart(fig_age, use_container_width=True)
            
        with col_c2:
            st.markdown("#### SIP Amount Boxplot by Age Group")
            df_sip_only = df_demo_f[df_demo_f["transaction_type"] == "SIP"]
            if df_sip_only.empty:
                st.info("No SIP transactions.")
            else:
                fig_box = px.box(df_sip_only, x="age_group", y="amount_inr", color="age_group", color_discrete_sequence=px.colors.qualitative.Dark24)
                fig_box = style_plotly_figure(fig_box)
                fig_box.update_layout(showlegend=False, xaxis_title="Age Group", yaxis_title="SIP Amount (₹)")
                st.plotly_chart(fig_box, use_container_width=True)
                
        with col_c3:
            st.markdown("#### Gender Split")
            df_gender_cnt = df_demo_f["gender"].value_counts().reset_index()
            fig_gender = px.pie(df_gender_cnt, names="gender", values="count", hole=0.4, color_discrete_sequence=px.colors.qualitative.Pastel)
            fig_gender = style_plotly_figure(fig_gender)
            fig_gender.update_layout(margin=dict(t=20, b=20, l=10, r=10))
            st.plotly_chart(fig_gender, use_container_width=True)
            
        st.markdown("---")
        col_g1, col_g2 = st.columns(2)
        
        with col_g1:
            st.markdown("#### SIP Amount Regional Distribution by State")
            df_state_sip = df_demo_f[df_demo_f["transaction_type"] == "SIP"].groupby("state")["amount_inr"].sum().reset_index()
            df_state_sip.sort_values("amount_inr", ascending=True, inplace=True)
            fig_state = px.bar(
                df_state_sip,
                y="state",
                x="amount_inr",
                orientation="h",
                labels={"amount_inr": "Total SIP Volume (₹)", "state": "State"},
                color="amount_inr",
                color_continuous_scale="Viridis"
            )
            fig_state = style_plotly_figure(fig_state)
            fig_state.update_layout(coloraxis_showscale=False)
            st.plotly_chart(fig_state, use_container_width=True)
            
        with col_g2:
            st.markdown("#### T30 vs B30 City Tier distribution")
            df_tier_cnt = df_demo_f["city_tier"].value_counts().reset_index()
            fig_tier = px.pie(df_tier_cnt, names="city_tier", values="count", hole=0.5, color_discrete_sequence=px.colors.qualitative.Prism)
            fig_tier = style_plotly_figure(fig_tier)
            st.plotly_chart(fig_tier, use_container_width=True)


# ── Page 5: Advanced Simulation & Optimization (B3 & B4) ──────────────────────

elif page == "Advanced Simulation & Optimization":
    st.markdown("""
        <div class="terminal-header">
            <h1>Quantitative Modelling & Analytics Terminal</h1>
            <p>Run Monte Carlo predictive simulations using GBM and optimize asset weights on the Markowitz Efficient Frontier.</p>
        </div>
    """, unsafe_allow_html=True)
    
    sim_mode = st.tabs(["B3: Monte Carlo Simulator", "B4: Markowitz Efficient Frontier"])
    
    # ── TAB 1: Monte Carlo Simulation (B3) ─────────────────────────────────────
    with sim_mode[0]:
        st.markdown("### Monte Carlo Projection (Geometric Brownian Motion)")
        
        # Slicers (At least 2 required)
        col_m1, col_m2, col_m3, col_m4 = st.columns(4)
        with col_m1:
            mc_fund = st.selectbox("Fund to Simulate", df_scorecard["scheme_name"].tolist(), key="mc_fund")
        with col_m2:
            mc_years = st.slider("Projection Horizon (Years)", 1, 5, 5)
        with col_m3:
            mc_paths = st.slider("Simulation Paths", 100, 1000, 500)
        with col_m4:
            mc_investment = st.number_input("Initial Investment (₹)", min_value=1000, max_value=10000000, value=10000, step=1000)
            
        mc_code = df_scorecard[df_scorecard["scheme_name"] == mc_fund]["amfi_code"].values[0]
        
        df_f_nav = load_nav_history([mc_code])
        df_f_nav.set_index("nav_date", inplace=True)
        df_f_nav.sort_index(inplace=True)
        
        if df_f_nav.empty or pd.isna(df_f_nav.index.min()) or pd.isna(df_f_nav.index.max()):
            st.error("No trading data found for this fund.")
            st.stop()
            
        df_f_nav = df_f_nav.reindex(pd.date_range(df_f_nav.index.min(), df_f_nav.index.max(), freq='D')).ffill().bfill()
        
        # Exclude weekends to avoid return damping
        df_trading = df_f_nav[df_f_nav.index.dayofweek < 5].copy()
        df_trading["log_return"] = np.log(df_trading["nav_value"] / df_trading["nav_value"].shift(1))
        log_returns = df_trading["log_return"].dropna()
        
        mu_d = log_returns.mean()
        sigma_d = log_returns.std()
        
        T_days = int(mc_years * 252)
        N_paths = mc_paths
        drift = mu_d - 0.5 * (sigma_d ** 2)
        
        np.random.seed(42)
        shocks = np.random.normal(0, 1, (T_days, N_paths))
        increments = drift + sigma_d * shocks
        
        cum_increments = np.vstack([np.zeros((1, N_paths)), np.cumsum(increments, axis=0)])
        paths = mc_investment * np.exp(cum_increments)
        
        p10 = np.percentile(paths, 10, axis=1)
        p50 = np.percentile(paths, 50, axis=1)
        p90 = np.percentile(paths, 90, axis=1)
        
        last_date = df_f_nav.index.max()
        future_dates = pd.date_range(last_date + pd.Timedelta(days=1), periods=T_days + 1, freq="B")
        
        fig_mc = go.Figure()
        
        fig_mc.add_trace(go.Scatter(
            x=future_dates, y=p90,
            line=dict(color="rgba(167, 139, 250, 0.05)"),
            showlegend=False,
            hoverinfo="skip"
        ))
        fig_mc.add_trace(go.Scatter(
            x=future_dates, y=p10,
            fill="tonexty",
            fillcolor="rgba(167, 139, 250, 0.12)",
            line=dict(color="rgba(167, 139, 250, 0.05)"),
            name="Uncertainty Band (10th - 90th percentile)"
        ))
        
        fig_mc.add_trace(go.Scatter(
            x=future_dates, y=p50,
            line=dict(color="#a855f7", width=2.5),
            name="Median Path (50th percentile)"
        ))
        
        for i in range(min(5, N_paths)):
            fig_mc.add_trace(go.Scatter(
                x=future_dates, y=paths[:, i],
                line=dict(width=0.8, dash="dot"),
                name=f"Sample Path {i+1}",
                opacity=0.4
            ))
            
        fig_mc = style_plotly_figure(fig_mc, f"5-Year Projection: {mc_fund}")
        fig_mc.update_layout(yaxis_title="Portfolio Value (₹)", hovermode="x unified")
        st.plotly_chart(fig_mc, use_container_width=True)
        
        st.markdown("#### Simulation Statistics")
        col_s1, col_s2, col_s3 = st.columns(3)
        with col_s1:
            st.metric("Median Projected Value", f"₹{p50[-1]:,.2f}", f"{((p50[-1]/mc_investment - 1)*100):.2f}% Growth")
        with col_s2:
            st.metric("Optimistic Projected Value (90th %)", f"₹{p90[-1]:,.2f}")
        with col_s3:
            st.metric("Conservative Projected Value (10th %)", f"₹{p10[-1]:,.2f}")

    # ── TAB 2: Markowitz Portfolio Optimization (B4) ───────────────────────────
    with sim_mode[1]:
        st.markdown("### Markowitz Efficient Frontier")
        
        col_o1, col_o2, col_o3 = st.columns(3)
        with col_o1:
            port_funds = st.multiselect(
                "Select exactly 5 funds to optimize",
                options=df_scorecard["scheme_name"].tolist(),
                default=df_scorecard["scheme_name"].head(5).tolist()
            )
        with col_o2:
            rf_rate = st.slider("Risk-Free Rate (Annualized %)", 4.0, 9.0, 6.5, 0.1)
        with col_o3:
            sim_portfolios = st.slider("Number of simulated portfolios", 1000, 10000, 5000, 500)
            
        if len(port_funds) != 5:
            st.warning("Please select exactly 5 funds.")
        else:
            port_codes = df_scorecard[df_scorecard["scheme_name"].isin(port_funds)]["amfi_code"].tolist()
            df_port_navs = load_nav_history(port_codes)
            
            df_port_pivot = df_port_navs.pivot(index="nav_date", columns="scheme_name", values="nav_value")
            if df_port_pivot.empty or pd.isna(df_port_pivot.index.min()) or pd.isna(df_port_pivot.index.max()):
                st.error("No trading data found for the selected funds.")
                st.stop()
            df_port_pivot = df_port_pivot.reindex(pd.date_range(df_port_pivot.index.min(), df_port_pivot.index.max(), freq='D')).ffill().bfill()
            
            df_port_returns = df_port_pivot[df_port_pivot.index.dayofweek < 5].pct_change().dropna()
            
            ann_returns = df_port_returns.mean() * 252
            ann_cov = df_port_returns.cov() * 252
            
            num_ports = sim_portfolios
            results = np.zeros((3 + len(port_codes), num_ports))
            
            rf_daily_proxy = rf_rate / 100.0
            
            np.random.seed(101)
            for i in range(num_ports):
                w = np.random.random(5)
                w /= np.sum(w)
                
                p_ret = np.sum(w * ann_returns)
                p_vol = np.sqrt(np.dot(w.T, np.dot(ann_cov, w)))
                p_sharpe = (p_ret - rf_daily_proxy) / p_vol
                
                results[0, i] = p_ret
                results[1, i] = p_vol
                results[2, i] = p_sharpe
                for j in range(len(w)):
                    results[3 + j, i] = w[j]
                    
            columns_w = [f"w_{name[:15]}" for name in port_funds]
            df_sim_ports = pd.DataFrame(results.T, columns=["Return", "Volatility", "Sharpe"] + columns_w)
            
            max_sharpe_idx = df_sim_ports["Sharpe"].idxmax()
            max_sharpe_port = df_sim_ports.iloc[max_sharpe_idx]
            
            min_vol_idx = df_sim_ports["Volatility"].idxmin()
            min_vol_port = df_sim_ports.iloc[min_vol_idx]
            
            fig_ef = go.Figure()
            fig_ef.add_trace(go.Scatter(
                x=df_sim_ports["Volatility"] * 100,
                y=df_sim_ports["Return"] * 100,
                mode="markers",
                marker=dict(
                    color=df_sim_ports["Sharpe"],
                    colorscale="Jet",
                    showscale=True,
                    colorbar=dict(title="Sharpe Ratio"),
                    size=5
                ),
                text=[f"Sharpe: {s:.2f}" for s in df_sim_ports["Sharpe"]],
                showlegend=False
            ))
            
            fig_ef.add_trace(go.Scatter(
                x=[max_sharpe_port["Volatility"] * 100],
                y=[max_sharpe_port["Return"] * 100],
                mode="markers",
                marker=dict(color="#a855f7", size=14, symbol="star"),
                name=f"Max Sharpe Ratio ({max_sharpe_port['Sharpe']:.2f})"
            ))
            
            fig_ef.add_trace(go.Scatter(
                x=[min_vol_port["Volatility"] * 100],
                y=[min_vol_port["Return"] * 100],
                mode="markers",
                marker=dict(color="#06b6d4", size=14, symbol="star"),
                name=f"Min Volatility ({min_vol_port['Volatility']*100:.2f}%)"
            ))
            
            fig_ef = style_plotly_figure(fig_ef, "Efficient Frontier Portfolio Allocations")
            fig_ef.update_layout(
                xaxis_title="Annualized Volatility (Standard Deviation %)",
                yaxis_title="Expected Annualized Return (%)",
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
            )
            st.plotly_chart(fig_ef, use_container_width=True)
            
            st.markdown("#### Optimal Weights Comparison")
            col_w1, col_w2 = st.columns(2)
            
            with col_w1:
                st.markdown("**Maximum Sharpe Ratio Portfolio Weights**")
                w_max = max_sharpe_port[[f"w_{n[:15]}" for n in port_funds]].values
                df_w_max = pd.DataFrame({"Fund": port_funds, "Weight (%)": w_max * 100})
                
                fig_w_max = px.bar(df_w_max, x="Fund", y="Weight (%)", color="Fund", text_auto=".1f%", color_discrete_sequence=px.colors.qualitative.G10)
                fig_w_max = style_plotly_figure(fig_w_max)
                fig_w_max.update_layout(showlegend=False, height=300)
                st.plotly_chart(fig_w_max, use_container_width=True)
                
                st.dataframe(df_w_max.style.format({"Weight (%)": "{:.2f}%"}), hide_index=True)
                
            with col_w2:
                st.markdown("**Minimum Volatility Portfolio Weights**")
                w_min = min_vol_port[[f"w_{n[:15]}" for n in port_funds]].values
                df_w_min = pd.DataFrame({"Fund": port_funds, "Weight (%)": w_min * 100})
                fig_w_min = px.bar(df_w_min, x="Fund", y="Weight (%)", color="Fund", text_auto=".1f%", color_discrete_sequence=px.colors.qualitative.T10)
                fig_w_min = style_plotly_figure(fig_w_min)
                fig_w_min.update_layout(showlegend=False, height=300)
                st.plotly_chart(fig_w_min, use_container_width=True)
                st.dataframe(df_w_min.style.format({"Weight (%)": "{:.2f}%"}), hide_index=True)


# ── Page 6: Advanced Risk & Cohort Analytics (Day 6) ──────────────────────────

elif page == "Advanced Risk & Cohort Analytics":
    st.markdown("""
        <div class="terminal-header">
            <h1>Advanced Risk & Cohort Analytics</h1>
            <p>Assess tail-risk metrics (VaR & CVaR), analyze rolling Sharpe ratios, track investor cohorts and SIP continuity rates, and review sector concentrations.</p>
        </div>
    """, unsafe_allow_html=True)
    
    risk_tabs = st.tabs([
        "VaR & CVaR Tail Risk", 
        "Rolling Sharpe Timelines", 
        "Cohort & SIP Continuity", 
        "Sector Concentration (HHI)",
        "Fund Recommender"
    ])
    
    # ── TAB 1: VaR & CVaR ──────────────────────────────────────────────────────
    with risk_tabs[0]:
        st.markdown("### Historical Value at Risk (VaR) & Conditional VaR (CVaR)")
        st.markdown("Metrics calculated at a **95% confidence level** using daily returns on business days (weekends/holidays forward-filled).")
        
        df_var_cvar = load_var_cvar_report()
        
        if df_var_cvar.empty:
            st.warning("VaR & CVaR report file not found. Please run scripts/generate_advanced_analytics.py first.")
        else:
            col_v1, col_v2 = st.columns(2)
            with col_v1:
                search_scheme = st.text_input("Search Scheme Name", "")
            with col_v2:
                max_var_slider = st.slider("Filter by Max 95% Daily VaR Loss (%)", -3.0, 0.0, 0.0, 0.1)
                
            df_var_filtered = df_var_cvar.copy()
            if search_scheme:
                df_var_filtered = df_var_filtered[df_var_filtered["scheme_name"].str.contains(search_scheme, case=False)]
            df_var_filtered = df_var_filtered[df_var_filtered["var_95"] >= (max_var_slider / 100.0)]
            
            # KPIs
            col_k1, col_k2, col_k3 = st.columns(3)
            highest_risk_row = df_var_cvar.sort_values("var_95").iloc[0]
            lowest_risk_row = df_var_cvar.sort_values("var_95", ascending=False).iloc[0]
            
            with col_k1:
                st.markdown(f"""
                    <div class="kpi-card-cyber" style="border-color: rgba(239, 68, 68, 0.3);">
                        <div class="kpi-label" style="color: #ef4444;">Highest Tail Risk Fund</div>
                        <div class="kpi-val" style="color: #ef4444; font-size:13px; font-weight:normal;">{highest_risk_row['scheme_name'][:30]}...</div>
                        <div style="font-size:14px; font-family:'Share Tech Mono'; color:#f87171; margin-top:5px;">VaR: {highest_risk_row['var_95']*100:.2f}% | CVaR: {highest_risk_row['cvar_95']*100:.2f}%</div>
                    </div>
                """, unsafe_allow_html=True)
            with col_k2:
                st.markdown(f"""
                    <div class="kpi-card-cyber" style="border-color: rgba(34, 197, 94, 0.3);">
                        <div class="kpi-label" style="color: #22c55e;">Lowest Tail Risk Fund</div>
                        <div class="kpi-val" style="color: #22c55e; font-size:13px; font-weight:normal;">{lowest_risk_row['scheme_name'][:30]}...</div>
                        <div style="font-size:14px; font-family:'Share Tech Mono'; color:#4ade80; margin-top:5px;">VaR: {lowest_risk_row['var_95']*100:.2f}% | CVaR: {lowest_risk_row['cvar_95']*100:.2f}%</div>
                    </div>
                """, unsafe_allow_html=True)
            with col_k3:
                st.markdown(f"""
                    <div class="kpi-card-cyber">
                        <div class="kpi-label">Average 95% Daily VaR</div>
                        <div class="kpi-val">{(df_var_cvar['var_95'].mean()*100):.2f}%</div>
                        <div style="font-size:11px; color:#94a3b8; margin-top:8px;">Avg. 95% CVaR: {(df_var_cvar['cvar_95'].mean()*100):.2f}%</div>
                    </div>
                """, unsafe_allow_html=True)
                
            st.markdown("#### Tail-Risk Metrics by Scheme")
            df_var_display = df_var_filtered.copy()
            df_var_display.columns = ["AMFI Code", "Scheme Name", "95% Daily VaR (%)", "95% Daily CVaR (%)"]
            st.dataframe(
                df_var_display.style.format({
                    "95% Daily VaR (%)": "{:.2%}",
                    "95% Daily CVaR (%)": "{:.2%}"
                }),
                use_container_width=True,
                hide_index=True
            )
            
    # ── TAB 2: Rolling Sharpe Timelines ────────────────────────────────────────
    with risk_tabs[1]:
        st.markdown("### Dynamic Rolling Sharpe Ratio Timeline")
        st.markdown("Analyze how the risk-adjusted return profiles of schemes evolve over time.")
        
        col_s1, col_s2 = st.columns([3, 1])
        with col_s1:
            selected_sharpe_funds = st.multiselect(
                "Select Funds to Compare (Up to 5)",
                options=df_scorecard["scheme_name"].tolist(),
                default=df_scorecard["scheme_name"].head(3).tolist(),
                key="sharpe_funds_sel"
            )
        with col_s2:
            rolling_window_days = st.slider("Rolling Window (Trading Days)", 30, 180, 90, 10)
            
        if not selected_sharpe_funds:
            st.warning("Please select at least one fund.")
        else:
            selected_codes = df_scorecard[df_scorecard["scheme_name"].isin(selected_sharpe_funds)]["amfi_code"].tolist()
            df_nav_selected = load_nav_history(selected_codes)
            
            df_rolling_sharpe = compute_rolling_sharpe(df_nav_selected, window=rolling_window_days)
            
            if df_rolling_sharpe.empty:
                st.info("No rolling data available for the selected range.")
            else:
                fig_rs = px.line(
                    df_rolling_sharpe,
                    x="Date",
                    y="Rolling Sharpe",
                    color="Scheme Name",
                    color_discrete_sequence=px.colors.qualitative.Plotly
                )
                fig_rs = style_plotly_figure(fig_rs, f"Rolling {rolling_window_days}-Day Sharpe Ratios")
                fig_rs.update_layout(
                    xaxis_title="Date",
                    yaxis_title="Sharpe Ratio (Annualized)",
                    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
                )
                st.plotly_chart(fig_rs, use_container_width=True)
                
    # ── TAB 3: Cohort & SIP Continuity ─────────────────────────────────────────
    with risk_tabs[2]:
        st.markdown("### Investor Cohort Analysis & SIP Continuity")
        
        df_cohorts = load_cohort_analysis()
        tot_eligible, at_risk, cont_rate = load_sip_continuity()
        
        st.markdown("#### SIP Continuity Risk Indicators")
        col_c1, col_c2, col_c3 = st.columns(3)
        with col_c1:
            st.markdown(f"""
                <div class="kpi-card-cyber">
                    <div class="kpi-label">Eligible Long-Term Investors (6+ SIPs)</div>
                    <div class="kpi-val">{tot_eligible:,}</div>
                </div>
            """, unsafe_allow_html=True)
        with col_c2:
            st.markdown(f"""
                <div class="kpi-card-cyber" style="border-color: rgba(239, 68, 68, 0.3);">
                    <div class="kpi-label" style="color: #ef4444;">Flagged At-Risk Investors (Gap > 35 Days)</div>
                    <div class="kpi-val" style="color: #ef4444;">{at_risk:,}</div>
                </div>
            """, unsafe_allow_html=True)
        with col_c3:
            st.markdown(f"""
                <div class="kpi-card-cyber" style="border-color: rgba(34, 197, 94, 0.3);">
                    <div class="kpi-label" style="color: #22c55e;">Overall SIP Continuity Rate</div>
                    <div class="kpi-val" style="color: #22c55e;">{cont_rate:.2f}%</div>
                </div>
            """, unsafe_allow_html=True)
            
        st.markdown("#### Investor Cohort Metrics (by first transaction year)")
        st.dataframe(
            df_cohorts.style.format({
                "Avg. SIP Amount (₹)": "₹{:,.2f}",
                "Total Invested (₹ Cr)": "₹{:,.4f} Cr"
            }),
            use_container_width=True,
            hide_index=True
        )
        
    # ── TAB 4: Sector Concentration (HHI) ──────────────────────────────────────
    with risk_tabs[3]:
        st.markdown("### Herfindahl-Hirschman Index (HHI) Concentrations")
        st.markdown("HHI measures diversification. Higher HHI means higher concentration in few sectors/stocks. Formula: $\\text{HHI} = \\sum (\\text{weight\\_pct}_i^2)$.")
        
        df_hhi = load_hhi_concentration()
        
        col_h1, col_h2 = st.columns(2)
        with col_h1:
            search_hhi_fund = st.text_input("Search Equity Fund Name", "", key="hhi_search")
        with col_h2:
            min_sector_hhi = st.slider("Minimum Sector HHI (Concentration Floor)", 1000.0, 3000.0, 1000.0, 100.0)
            
        df_hhi_filtered = df_hhi.copy()
        if search_hhi_fund:
            df_hhi_filtered = df_hhi_filtered[df_hhi_filtered["Scheme Name"].str.contains(search_hhi_fund, case=False)]
        df_hhi_filtered = df_hhi_filtered[df_hhi_filtered["Sector HHI"] >= min_sector_hhi]
        
        if df_hhi_filtered.empty:
            st.info("No funds match the filter criteria.")
        else:
            fig_hhi = go.Figure()
            fig_hhi.add_trace(go.Bar(
                x=df_hhi_filtered["Scheme Name"],
                y=df_hhi_filtered["Sector HHI"],
                name="Sector HHI",
                marker_color="#a855f7"
            ))
            fig_hhi.add_trace(go.Bar(
                x=df_hhi_filtered["Scheme Name"],
                y=df_hhi_filtered["Stock HHI"],
                name="Stock HHI",
                marker_color="#06b6d4"
            ))
            
            fig_hhi = style_plotly_figure(fig_hhi, "Equity Funds HHI Concentration Comparison")
            fig_hhi.update_layout(
                xaxis_title="Fund Scheme",
                yaxis_title="HHI Score",
                barmode="group",
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
            )
            st.plotly_chart(fig_hhi, use_container_width=True)
            
            st.dataframe(
                df_hhi_filtered.style.format({
                    "Sector HHI": "{:.2f}",
                    "Stock HHI": "{:.2f}"
                }),
                use_container_width=True,
                hide_index=True
            )
            
    # ── TAB 5: Fund Recommender ────────────────────────────────────────────────
    with risk_tabs[4]:
        st.markdown("### Quantitative Fund Recommender")
        st.markdown("Select your risk tolerance profile to get the top 3 recommended mutual funds based on historical Sharpe ratios.")
        
        selected_risk = st.selectbox(
            "Select Risk Appetite Profile",
            ["Low", "Moderate", "High"],
            index=1,
            key="recommender_risk_profile"
        )
        
        df_recs = get_recommendations_df(selected_risk)
        
        if df_recs.empty:
            st.warning("No matching recommendations found. Ensure the database contains valid performance and risk records.")
        else:
            st.markdown(f"#### Top 3 Recommended Funds for **{selected_risk}** Risk Appetite:")
            
            df_recs_display = df_recs.copy()
            df_recs_display.columns = ["AMFI Code", "Scheme Name", "Fund House", "Risk Grade", "Sharpe Ratio", "3-Year Return"]
            
            st.dataframe(
                df_recs_display.style.format({
                    "Sharpe Ratio": "{:.2f}",
                    "3-Year Return": "{:.2%}"
                }),
                use_container_width=True,
                hide_index=True
            )
            
            st.info("Disclaimer: Mutual fund investments are subject to market risks. Past performance is not indicative of future returns.")

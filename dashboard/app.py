"""
app.py — Bluestock Mutual Fund Capstone: Interactive Dashboard (B2, B3, B4)
A comprehensive Streamlit web app serving as an interactive alternative to Power BI.
Features multiple pages with slicers, Plotly visualizations, Monte Carlo NAV projections (B3),
and Markowitz Efficient Frontier portfolio optimization (B4).
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
    page_title="Bluestock Mutual Fund Analytics",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Custom CSS for Premium Design ──────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif;
    }
    
    /* Header card */
    .header-box {
        background: linear-gradient(135deg, #4f46e5 0%, #312e81 100%);
        padding: 2.5rem;
        border-radius: 16px;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 10px 15px -3px rgba(79, 70, 229, 0.2);
    }
    
    .header-box h1 {
        margin: 0;
        font-size: 2.5rem;
        font-weight: 700;
        letter-spacing: -0.05em;
    }
    
    .header-box p {
        margin: 0.5rem 0 0 0;
        opacity: 0.9;
        font-size: 1.1rem;
    }
    
    /* Metric Card Styling */
    .metric-card {
        background-color: #1e1b4b;
        border-left: 5px solid #6366f1;
        padding: 1.25rem;
        border-radius: 8px;
        margin-bottom: 1rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        transition: transform 0.2s;
    }
    .metric-card:hover {
        transform: translateY(-2px);
    }
    .metric-title {
        font-size: 0.9rem;
        color: #94a3b8;
        font-weight: 600;
        text-transform: uppercase;
    }
    .metric-value {
        font-size: 1.8rem;
        font-weight: 700;
        color: #f8fafc;
        margin-top: 0.25rem;
    }
</style>
""", unsafe_allow_html=True)


# ── Database & CSV Loaders ──────────────────────────────────────────────────────

def get_connection():
    """Create a sqlite connection."""
    return sqlite3.connect(DB_PATH)


@st.cache_data
def load_scorecard():
    """Load the performance scorecard csv."""
    if SCORECARD_PATH.exists():
        return pd.read_csv(SCORECARD_PATH)
    else:
        st.error("fund_scorecard.csv not found. Please run scripts/generate_analytics.py first.")
        return pd.DataFrame()


@st.cache_data
def load_alpha_beta():
    """Load the alpha & beta regression data."""
    if ALPHA_BETA_PATH.exists():
        return pd.read_csv(ALPHA_BETA_PATH)
    return pd.DataFrame()


@st.cache_data
def load_nav_history(amfi_codes=None):
    """Load NAV history for selected schemes, sorted by date."""
    conn = get_connection()
    if amfi_codes:
        # Prevent SQL injection by parameterizing list
        placeholders = ",".join("?" for _ in amfi_codes)
        query = f"""
            SELECT n.nav_date, n.nav_value, n.amfi_code, f.scheme_name, f.fund_house
            FROM fact_nav n
            JOIN dim_fund f ON n.amfi_code = f.amfi_code
            WHERE n.amfi_code IN ({placeholders})
            ORDER BY n.nav_date
        """
        df = pd.read_sql_query(query, conn, params=amfi_codes)
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
    """Load Nifty index close histories."""
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
    """Load investor transaction demographic parameters."""
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
    """Load aggregated fund house AUM growth."""
    conn = get_connection()
    df = pd.read_sql_query("SELECT aum_date, fund_house, aum_lakh_crore, aum_crore, num_schemes FROM fact_aum", conn)
    conn.close()
    df["aum_date"] = pd.to_datetime(df["aum_date"])
    return df


@st.cache_data
def load_sip_inflows():
    """Load monthly SIP inflow timeseries."""
    conn = get_connection()
    df = pd.read_sql_query("SELECT month, sip_inflow_crore, active_sip_accounts_crore, new_sip_accounts_lakh FROM monthly_sip_inflows", conn)
    conn.close()
    return df


@st.cache_data
def load_category_inflows():
    """Load category wise net inflows."""
    conn = get_connection()
    df = pd.read_sql_query("SELECT month, category, net_inflow_crore FROM category_inflows", conn)
    conn.close()
    return df


@st.cache_data
def load_folio_growth():
    """Load industry folio counts."""
    conn = get_connection()
    df = pd.read_sql_query("SELECT month, total_folios_crore, equity_folios_crore, debt_folios_crore FROM industry_folio_count", conn)
    conn.close()
    return df


@st.cache_data
def load_portfolio_sectors(amfi_code):
    """Load sector allocation weights for a specific scheme."""
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


# ── App Layout & Sidebar Navigation ────────────────────────────────────────────

st.sidebar.markdown(
    "<h2 style='text-align: center; color: #6366f1; font-weight:700;'>Bluestock MF</h2>", 
    unsafe_allow_html=True
)
st.sidebar.markdown("<p style='text-align: center; color: #94a3b8; font-size: 0.9rem;'>Day 5 & Bonus Dashboard</p>", unsafe_allow_html=True)
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Navigation Workspace",
    [
        "Fund Scorecard & Benchmark",
        "NAV Analysis & Correlation",
        "Industry & AUM Growth",
        "Investor Demographics",
        "Advanced Simulation & Optimization"
    ]
)

# ── Load Global Data ───────────────────────────────────────────────────────────
df_scorecard = load_scorecard()
df_ab = load_alpha_beta()

# ── Page 1: Fund Scorecard & Benchmark ──────────────────────────────────────────

if page == "Fund Scorecard & Benchmark":
    st.markdown("""
        <div class="header-box">
            <h1>Fund Scorecard & Performance Leaderboard</h1>
            <p>Explore calculated CAGR return parameters, risk metrics (Sharpe, Sortino, Alpha, Beta, Max Drawdown), and composite rankings.</p>
        </div>
    """, unsafe_allow_html=True)
    
    # ── Page-Level Slicers (At least 2 required) ───────────────────
    st.markdown("### Filters")
    col_f1, col_f2, col_f3 = st.columns(3)
    with col_f1:
        f_fund_house = st.selectbox("Select Fund House", ["All"] + list(df_scorecard["fund_house"].unique()))
    with col_f2:
        f_min_score = st.slider("Minimum Composite Score (0-100)", 0.0, 100.0, 0.0, 1.0)
    with col_f3:
        # Retrieve distinct categories from dim_fund using connection
        conn = get_connection()
        cats = pd.read_sql_query("SELECT DISTINCT category FROM dim_fund", conn)["category"].tolist()
        conn.close()
        f_category = st.multiselect("Select Fund Category", cats, default=cats)
        
    # Apply Slicers
    df_filtered = df_scorecard.copy()
    
    # Connect with dim_fund to filter by category
    conn = get_connection()
    df_dim_fund = pd.read_sql_query("SELECT amfi_code, category FROM dim_fund", conn)
    conn.close()
    df_filtered = df_filtered.merge(df_dim_fund, on="amfi_code")
    
    if f_fund_house != "All":
        df_filtered = df_filtered[df_filtered["fund_house"] == f_fund_house]
    df_filtered = df_filtered[df_filtered["composite_score"] >= f_min_score]
    df_filtered = df_filtered[df_filtered["category"].isin(f_category)]
    
    # KPIs Rows
    if not df_filtered.empty:
        col_m1, col_m2, col_m3, col_m4 = st.columns(4)
        with col_m1:
            st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-title">Leader Fund</div>
                    <div class="metric-value">{df_filtered.iloc[0]['scheme_name'][:25]}...</div>
                </div>
            """, unsafe_allow_html=True)
        with col_m2:
            st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-title">Avg. 3-Year CAGR</div>
                    <div class="metric-value">{(df_filtered['cagr_3y'].mean()*100):.2f}%</div>
                </div>
            """, unsafe_allow_html=True)
        with col_m3:
            st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-title">Avg. Sharpe Ratio</div>
                    <div class="metric-value">{df_filtered['sharpe_ratio'].mean():.2f}</div>
                </div>
            """, unsafe_allow_html=True)
        with col_m4:
            st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-title">Funds Count</div>
                    <div class="metric-value">{len(df_filtered)} / 40</div>
                </div>
            """, unsafe_allow_html=True)
            
    # Leaderboard Dataframe
    st.markdown("### Overall Scoreboard Ranking")
    df_display = df_filtered[[
        "amfi_code", "scheme_name", "fund_house", "category", "cagr_3y", "sharpe_ratio", "alpha", 
        "expense_ratio_pct", "max_drawdown", "composite_score"
    ]].copy()
    
    # Rename columns to clearly display units
    df_display.columns = [
        "AMFI Code", "Scheme Name", "Fund House", "Category", "3-Year CAGR", "Sharpe Ratio", "Alpha (Annual)", 
        "Expense Ratio (%)", "Max Drawdown", "Composite Score (0-100)"
    ]
    
    # Format percentages and ratios
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
    
    # ── Dynamic Benchmark Comparison ──────────────────────────────
    st.markdown("---")
    st.markdown("### Dynamic Benchmark Comparison & Tracking Error")
    
    # Sub-slicers
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
        # Date range slider
        start_date_slider = st.date_input("Start Date", datetime(2023, 5, 29))
        end_date_slider = st.date_input("End Date", datetime(2026, 5, 29))
        
    if len(selected_funds) > 5:
        st.warning("Please select a maximum of 5 funds.")
    elif len(selected_funds) == 0:
        st.info("Select at least 1 fund to compare return values.")
    else:
        # Convert selected scheme names to AMFI codes
        selected_codes = df_scorecard[df_scorecard["scheme_name"].isin(selected_funds)]["amfi_code"].tolist()
        
        # Load histories
        df_navs = load_nav_history(selected_codes)
        df_indices = load_index_history()
        
        # Filter dates
        start_dt = pd.to_datetime(start_date_slider)
        end_dt = pd.to_datetime(end_date_slider)
        
        df_navs_f = df_navs[(df_navs["nav_date"] >= start_dt) & (df_navs["nav_date"] <= end_dt)]
        df_indices_f = df_indices[(df_indices["date"] >= start_dt) & (df_indices["date"] <= end_dt)]
        
        if df_navs_f.empty or df_indices_f.empty:
            st.error("No trading data found for the selected date range.")
        else:
            # Pivot & Normalize Index returns
            df_ind_pivot = df_indices_f.pivot(index="date", columns="index_name", values="close_value")
            
            # Reindex indices to avoid weekend gaps (handling holidays / weekends)
            df_ind_pivot = df_ind_pivot.reindex(pd.date_range(df_ind_pivot.index.min(), df_ind_pivot.index.max(), freq='D')).ffill().bfill()
            
            # Normalize index prices starting from 0%
            idx_norm = df_ind_pivot[benchmark_name].divide(df_ind_pivot[benchmark_name].iloc[0]).subtract(1).multiply(100)
            
            # Create Plotly Graph
            fig_compare = go.Figure()
            
            # Plot Benchmark index
            fig_compare.add_trace(go.Scatter(
                x=idx_norm.index,
                y=idx_norm,
                name=f"{benchmark_name} (Benchmark)",
                line=dict(color="#1e293b", width=2.5, dash="dash")
            ))
            
            # Plot each selected fund and calculate tracking error
            for code in selected_codes:
                fund_df = df_navs_f[df_navs_f["amfi_code"] == code].copy()
                fund_df.set_index("nav_date", inplace=True)
                fund_df.sort_index(inplace=True)
                
                # Reindex to full calendar range and forward fill weekends/holidays (Avoid weekend/holiday gaps)
                full_range = pd.date_range(fund_df.index.min(), fund_df.index.max(), freq="D")
                fund_df = fund_df.reindex(full_range).ffill().bfill()
                
                # Calculate normalized cumulative returns (%)
                fund_norm = fund_df["nav_value"].divide(fund_df["nav_value"].iloc[0]).subtract(1).multiply(100)
                
                # Calculate daily returns (excluding weekends for standard volatility scaling)
                # Filter weekend dates
                fund_days = fund_df[fund_df.index.dayofweek < 5].copy()
                fund_returns = fund_days["nav_value"].pct_change().dropna()
                
                idx_days = df_ind_pivot[df_ind_pivot.index.dayofweek < 5].copy()
                idx_returns = idx_days[benchmark_name].pct_change().dropna()
                
                aligned = pd.concat([fund_returns, idx_returns], axis=1, join="inner").dropna()
                aligned.columns = ["fund", "benchmark"]
                
                # Tracking Error = Standard Deviation of Return Differences * sqrt(252)
                diff = aligned["fund"] - aligned["benchmark"]
                tracking_error = diff.std() * np.sqrt(252) * 100 # In percentage
                
                f_name = df_scorecard[df_scorecard["amfi_code"] == code]["scheme_name"].values[0]
                short_name = f_name[:28] + "..." if len(f_name) > 30 else f_name
                
                fig_compare.add_trace(go.Scatter(
                    x=fund_norm.index,
                    y=fund_norm,
                    name=f"{short_name} (TE: {tracking_error:.2f}%)",
                    line=dict(width=2)
                ))
                
            fig_compare.update_layout(
                title=dict(text=f"Cumulative Returns Comparison vs {benchmark_name}", font=dict(size=16, weight="bold")),
                xaxis_title="Date",
                yaxis_title="Cumulative Return (%)",
                template="plotly_white",
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                margin=dict(l=40, r=40, t=80, b=40),
                hovermode="x unified"
            )
            
            st.plotly_chart(fig_compare, use_container_width=True)

# ── Page 2: NAV Analysis & Correlation ──────────────────────────────────────────

elif page == "NAV Analysis & Correlation":
    st.markdown("""
        <div class="header-box">
            <h1>NAV Trends, Correlations & Allocations</h1>
            <p>Plot historic scheme NAV movements, analyze return correlations, and view portfolio sector donut weights.</p>
        </div>
    """, unsafe_allow_html=True)
    
    # ── Page-Level Slicers (At least 2 required) ───────────────────
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
    
    # Fetch and filter NAV
    df_navs = load_nav_history([primary_code])
    start_dt = pd.to_datetime(start_date)
    end_dt = pd.to_datetime(end_date)
    
    df_navs_f = df_navs[(df_navs["nav_date"] >= start_dt) & (df_navs["nav_date"] <= end_dt)].copy()
    df_navs_f.set_index("nav_date", inplace=True)
    df_navs_f.sort_index(inplace=True)
    
    # Reindex to full calendar range and forward fill weekends/holidays (Avoid weekend/holiday gaps)
    full_range = pd.date_range(df_navs_f.index.min(), df_navs_f.index.max(), freq="D")
    df_navs_f = df_navs_f.reindex(full_range).ffill().bfill()
    
    # Plotly NAV Trend Chart
    fig_nav = go.Figure()
    fig_nav.add_trace(go.Scatter(
        x=df_navs_f.index,
        y=df_navs_f["nav_value"],
        name="NAV Value",
        line=dict(color="#4f46e5", width=2.5)
    ))
    
    # Shading regions
    # 2023 Bull Run: Jan 2023 - Dec 2023
    if highlight_bull:
        fig_nav.add_vrect(
            x0="2023-01-01", x1="2023-12-31",
            fillcolor="#f59e0b", opacity=0.12,
            layer="below", line_width=0,
            annotation_text="2023 Bull Run",
            annotation_position="top left"
        )
    # 2024 Market Corrections: Mar 2024 - June 2024
    if highlight_corr:
        fig_nav.add_vrect(
            x0="2024-03-01", x1="2024-06-30",
            fillcolor="#ef4444", opacity=0.12,
            layer="below", line_width=0,
            annotation_text="2024 Market Corrections",
            annotation_position="top left"
        )
        
    fig_nav.update_layout(
        title=dict(text=f"NAV Trend — {f_primary_fund}", font=dict(size=16, weight="bold")),
        xaxis_title="Date",
        yaxis_title="NAV (₹)",
        template="plotly_white",
        margin=dict(l=40, r=40, t=60, b=40),
        hovermode="x unified"
    )
    
    col_chart1, col_chart2 = st.columns([2, 1])
    with col_chart1:
        st.plotly_chart(fig_nav, use_container_width=True)
    with col_chart2:
        # Sector Allocation Donut Chart
        st.markdown("### Sector Allocation")
        df_sectors = load_portfolio_sectors(primary_code)
        if df_sectors.empty:
            st.info("No sector holdings data available for this scheme.")
        else:
            fig_sectors = px.pie(
                df_sectors,
                names="sector",
                values="weight_pct",
                hole=0.4,
                color_discrete_sequence=px.colors.qualitative.Indigo
            )
            fig_sectors.update_layout(
                margin=dict(l=10, r=10, t=10, b=10),
                legend=dict(orientation="h", y=-0.1)
            )
            st.plotly_chart(fig_sectors, use_container_width=True)
            
    # ── Pairwise daily returns correlation matrix of 10 selected funds ──
    st.markdown("---")
    st.markdown("### Pairwise daily returns correlation matrix of 10 selected funds")
    
    # Filters
    col_c1, col_c2 = st.columns(2)
    with col_c1:
        selected_corr_funds = st.multiselect(
            "Select 10 Funds for Correlation Analysis",
            options=df_scorecard["scheme_name"].tolist(),
            default=df_scorecard["scheme_name"].head(10).tolist()
        )
    with col_c2:
        corr_date_range = st.date_input("Correlation Period", [datetime(2022, 1, 3), datetime(2026, 5, 29)])
        
    if len(selected_corr_funds) < 2:
        st.info("Select at least 2 funds to see correlations.")
    else:
        corr_codes = df_scorecard[df_scorecard["scheme_name"].isin(selected_corr_funds)]["amfi_code"].tolist()
        
        # Load and pivot returns
        df_all_navs = load_nav_history(corr_codes)
        
        # Filter date
        if len(corr_date_range) == 2:
            c_start, c_end = pd.to_datetime(corr_date_range[0]), pd.to_datetime(corr_date_range[1])
            df_all_navs = df_all_navs[(df_all_navs["nav_date"] >= c_start) & (df_all_navs["nav_date"] <= c_end)]
            
        df_pivot_navs = df_all_navs.pivot(index="nav_date", columns="scheme_name", values="nav_value")
        
        # Handle weekends/holidays: reindex and forward fill
        df_pivot_navs = df_pivot_navs.reindex(pd.date_range(df_pivot_navs.index.min(), df_pivot_navs.index.max(), freq='D')).ffill().bfill()
        
        # Calculate daily percentage returns (business days only)
        df_pivot_returns = df_pivot_navs[df_pivot_navs.index.dayofweek < 5].pct_change().dropna()
        
        corr_matrix = df_pivot_returns.corr()
        
        # Truncate names for heatmap axis labels
        short_labels = [n[:20] + "..." if len(n) > 20 else n for n in corr_matrix.columns]
        
        fig_corr = go.Figure(data=go.Heatmap(
            z=corr_matrix.values,
            x=short_labels,
            y=short_labels,
            colorscale="Viridis",
            zmin=-1, zmax=1,
            text=np.round(corr_matrix.values, 2),
            texttemplate="%{text}",
            hoverongaps=False
        ))
        
        fig_corr.update_layout(
            title=dict(text="Pairwise Return Correlation Heatmap", font=dict(size=15, weight="bold")),
            xaxis=dict(tickangle=-45),
            margin=dict(l=80, r=40, t=60, b=80),
            height=600
        )
        st.plotly_chart(fig_corr, use_container_width=True)

# ── Page 3: Industry & AUM Growth ──────────────────────────────────────────────

elif page == "Industry & AUM Growth":
    st.markdown("""
        <div class="header-box">
            <h1>Mutual Fund Industry Inflows & AUM growth</h1>
            <p>Analyze grouped fund house AUM growth, monthly SIP time-series trends, category heatmaps, and folio growth milestones.</p>
        </div>
    """, unsafe_allow_html=True)
    
    # ── Page-Level Slicers (At least 2 required) ───────────────────
    st.markdown("### Filters")
    col_a1, col_a2 = st.columns(2)
    with col_a1:
        # Load AUM data
        df_aum = load_industry_aum()
        f_aum_houses = st.multiselect("Select Fund House Filter", options=list(df_aum["fund_house"].unique()), default=list(df_aum["fund_house"].unique()))
    with col_a2:
        f_years = st.slider("Select Year Horizon (2022-2025)", 2022, 2025, (2022, 2025))
        
    # Apply filters to AUM
    df_aum_f = df_aum[df_aum["fund_house"].isin(f_aum_houses)].copy()
    df_aum_f["year"] = df_aum_f["aum_date"].dt.year
    df_aum_f = df_aum_f[(df_aum_f["year"] >= f_years[0]) & (df_aum_f["year"] <= f_years[1])]
    
    # 1. AUM Grouped Bar Chart
    st.markdown("### Total AUM Growth by Fund House (Highlighting SBI ₹12.5L Cr)")
    
    # Group by Year and Fund House
    df_aum_grouped = df_aum_f.groupby(["year", "fund_house"])["aum_lakh_crore"].sum().reset_index()
    
    fig_aum = px.bar(
        df_aum_grouped,
        x="year",
        y="aum_lakh_crore",
        color="fund_house",
        barmode="group",
        labels={"aum_lakh_crore": "Total AUM (₹ Lakh Crore)", "year": "Year"},
        color_discrete_sequence=px.colors.qualitative.D3
    )
    
    # Add annotation for SBI's dominance (approx 12.5 Lakh Cr in late 2025)
    fig_aum.add_annotation(
        x=2025,
        y=12.5,
        text="SBI Dominance: ₹12.5 Lakh Crore",
        showarrow=True,
        arrowhead=2,
        arrowcolor="red",
        arrowsize=1.5,
        arrowwidth=2,
        ax=-80,
        ay=-40,
        font=dict(size=12, color="white", weight="bold"),
        bgcolor="red",
        opacity=0.85
    )
    fig_aum.update_layout(template="plotly_white", margin=dict(t=40, b=40))
    st.plotly_chart(fig_aum, use_container_width=True)
    
    # 2. SIP Inflows monthly timeseries
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
            line=dict(color="#10b981", width=2.5),
            name="SIP Inflow (₹ Crore)"
        ))
        
        # Annotate all time high of 31,002 Crore in Dec 2025
        # The month column is string format "YYYY-MM"
        fig_sip.add_annotation(
            x="2025-12",
            y=31002,
            text="All-Time High: ₹31,002 Cr (Dec 2025)",
            showarrow=True,
            arrowhead=3,
            ax=-90,
            ay=-50,
            arrowcolor="#059669",
            font=dict(color="white", size=11, weight="bold"),
            bgcolor="#059669"
        )
        fig_sip.update_layout(
            template="plotly_white",
            xaxis_title="Month",
            yaxis_title="SIP Inflow (₹ Crore)",
            margin=dict(l=40, r=40, t=40, b=40)
        )
        st.plotly_chart(fig_sip, use_container_width=True)
        
    with col_heat:
        st.markdown("### Category Net Inflow Heatmap")
        df_cat = load_category_inflows()
        df_cat_pivot = df_cat.pivot(index="category", columns="month", values="net_inflow_crore")
        
        fig_cat = go.Figure(data=go.Heatmap(
            z=df_cat_pivot.values,
            x=df_cat_pivot.columns,
            y=df_cat_pivot.index,
            colorscale="Tealgrn",
            hoverongaps=False
        ))
        fig_cat.update_layout(
            xaxis_title="Month",
            yaxis_title="Category",
            margin=dict(l=100, r=40, t=40, b=40)
        )
        st.plotly_chart(fig_cat, use_container_width=True)
        
    # 3. Folio growth milestones
    st.markdown("---")
    st.markdown("### Folio Count Growth Milestones")
    df_folio = load_folio_growth()
    
    fig_folio = go.Figure()
    fig_folio.add_trace(go.Scatter(
        x=df_folio["month"],
        y=df_folio["total_folios_crore"],
        name="Total Folios (Cr)",
        line=dict(color="#6366f1", width=3)
    ))
    
    # Milestone 1: Jan 2022 -> 13.26 Cr
    fig_folio.add_annotation(
        x="2022-01",
        y=13.26,
        text="Start: 13.26 Cr",
        showarrow=True,
        arrowhead=1,
        ax=50,
        ay=40
    )
    
    # Milestone 2: Dec 2025 -> 26.12 Cr
    fig_folio.add_annotation(
        x="2025-12",
        y=26.12,
        text="Peak: 26.12 Cr",
        showarrow=True,
        arrowhead=1,
        ax=-50,
        ay=-40
    )
    
    fig_folio.update_layout(
        template="plotly_white",
        xaxis_title="Month",
        yaxis_title="Folios Count (Crore)",
        margin=dict(l=40, r=40, t=40, b=40)
    )
    st.plotly_chart(fig_folio, use_container_width=True)

# ── Page 4: Investor Demographics ──────────────────────────────────────────────

elif page == "Investor Demographics":
    st.markdown("""
        <div class="header-box">
            <h1>Investor Demographics & State Distributions</h1>
            <p>Analyze demographic segments, age distributions, gender splits, and regional SIP allocations.</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Load demographics
    df_demo = load_demographics_data()
    
    # ── Page-Level Slicers (At least 2 required) ───────────────────
    st.markdown("### Filters")
    col_d1, col_d2, col_d3 = st.columns(3)
    with col_d1:
        f_state = st.multiselect("Select State Filter", options=["All"] + list(df_demo["state"].unique()), default="All")
    with col_d2:
        f_tier = st.selectbox("Select City Tier", ["All", "T30", "B30"])
    with col_d3:
        f_gender = st.selectbox("Select Gender", ["All", "Male", "Female"])
        
    # Apply Slicers
    df_demo_f = df_demo.copy()
    if "All" not in f_state and len(f_state) > 0:
        df_demo_f = df_demo_f[df_demo_f["state"].isin(f_state)]
    if f_tier != "All":
        df_demo_f = df_demo_f[df_demo_f["city_tier"] == f_tier]
    if f_gender != "All":
        df_demo_f = df_demo_f[df_demo_f["gender"] == f_gender]
        
    if df_demo_f.empty:
        st.warning("No data matches selected filter criteria.")
    else:
        # Demographic charts row 1
        col_c1, col_c2, col_c3 = st.columns(3)
        
        with col_c1:
            st.markdown("#### Age Group Distribution")
            df_age = df_demo_f["age_group"].value_counts().reset_index()
            fig_age = px.pie(df_age, names="age_group", values="count", color_discrete_sequence=px.colors.qualitative.Pastel)
            fig_age.update_layout(margin=dict(t=20, b=20, l=10, r=10))
            st.plotly_chart(fig_age, use_container_width=True)
            
        with col_c2:
            st.markdown("#### SIP Amount Boxplot by Age Group")
            # Only transaction_type = 'SIP'
            df_sip_only = df_demo_f[df_demo_f["transaction_type"] == "SIP"]
            if df_sip_only.empty:
                st.info("No SIP transactions found.")
            else:
                fig_box = px.box(df_sip_only, x="age_group", y="amount_inr", color="age_group", labels={"amount_inr": "SIP Amount (₹)", "age_group": "Age Group"})
                fig_box.update_layout(showlegend=False, margin=dict(t=20, b=20))
                st.plotly_chart(fig_box, use_container_width=True)
                
        with col_c3:
            st.markdown("#### Gender Split")
            df_gender_cnt = df_demo_f["gender"].value_counts().reset_index()
            fig_gender = px.pie(df_gender_cnt, names="gender", values="count", hole=0.3, color_discrete_sequence=px.colors.qualitative.Pastel1)
            fig_gender.update_layout(margin=dict(t=20, b=20, l=10, r=10))
            st.plotly_chart(fig_gender, use_container_width=True)
            
        # Geographic distribution row 2
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
                color_continuous_scale="Purples"
            )
            fig_state.update_layout(margin=dict(t=20, b=20), coloraxis_showscale=False)
            st.plotly_chart(fig_state, use_container_width=True)
            
        with col_g2:
            st.markdown("#### T30 vs B30 City Tier distribution")
            df_tier_cnt = df_demo_f["city_tier"].value_counts().reset_index()
            fig_tier = px.pie(df_tier_cnt, names="city_tier", values="count", hole=0.4, color_discrete_sequence=px.colors.qualitative.Set2)
            fig_tier.update_layout(margin=dict(t=20, b=20))
            st.plotly_chart(fig_tier, use_container_width=True)

# ── Page 5: Advanced Simulation & Optimization (B3 & B4) ──────────────────────

elif page == "Advanced Simulation & Optimization":
    st.markdown("""
        <div class="header-box">
            <h1>Advanced Analytics & Portfolio Projections</h1>
            <p>Perform Monte Carlo growth projections using Geometric Brownian Motion (GBM) and build optimal portfolios using Markowitz Efficient Frontier models.</p>
        </div>
    """, unsafe_allow_html=True)
    
    sim_mode = st.tabs(["B3: Monte Carlo Simulator", "B4: Markowitz Efficient Frontier"])
    
    # ── TAB 1: Monte Carlo Simulation (B3) ─────────────────────────────────────
    with sim_mode[0]:
        st.markdown("### Monte Carlo Projection (Geometric Brownian Motion)")
        st.write("Projects future NAV distributions based on historical log-return drift and volatility parameters.")
        
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
        
        # Load returns to calculate mean and volatility
        df_f_nav = load_nav_history([mc_code])
        df_f_nav.set_index("nav_date", inplace=True)
        df_f_nav.sort_index(inplace=True)
        
        # Handle weekends: reindex & ffill
        df_f_nav = df_f_nav.reindex(pd.date_range(df_f_nav.index.min(), df_f_nav.index.max(), freq='D')).ffill().bfill()
        
        # Log returns on trading days only (to avoid weekend flat returns deflating stats)
        df_trading = df_f_nav[df_f_nav.index.dayofweek < 5].copy()
        df_trading["log_return"] = np.log(df_trading["nav_value"] / df_trading["nav_value"].shift(1))
        log_returns = df_trading["log_return"].dropna()
        
        # Calculate daily drift (mean) and volatility (std dev)
        mu_d = log_returns.mean()
        sigma_d = log_returns.std()
        
        # Setup simulation
        T_days = int(mc_years * 252) # 252 trading days per year
        N_paths = mc_paths
        
        # GBM Equation: S_t = S_0 * exp(cumsum( (mu - 0.5 * sigma^2) + sigma * Z ))
        drift = mu_d - 0.5 * (sigma_d ** 2)
        
        # Generate random shock increments
        np.random.seed(42) # set seed for reproducibility
        shocks = np.random.normal(0, 1, (T_days, N_paths))
        increments = drift + sigma_d * shocks
        
        # Cumulative return path matrix
        cum_increments = np.vstack([np.zeros((1, N_paths)), np.cumsum(increments, axis=0)])
        paths = mc_investment * np.exp(cum_increments)
        
        # Percentiles
        p10 = np.percentile(paths, 10, axis=1)
        p50 = np.percentile(paths, 50, axis=1)
        p90 = np.percentile(paths, 90, axis=1)
        
        # Generate dates
        last_date = df_f_nav.index.max()
        future_dates = pd.date_range(last_date + pd.Timedelta(days=1), periods=T_days + 1, freq="B") # only business days
        
        # Plotly chart
        fig_mc = go.Figure()
        
        # Add percentile bands
        fig_mc.add_trace(go.Scatter(
            x=future_dates, y=p90,
            line=dict(color="rgba(99, 102, 241, 0.1)"),
            showlegend=False,
            hoverinfo="skip"
        ))
        fig_mc.add_trace(go.Scatter(
            x=future_dates, y=p10,
            fill="tonexty",
            fillcolor="rgba(99, 102, 241, 0.15)",
            line=dict(color="rgba(99, 102, 241, 0.1)"),
            name="Uncertainty Band (10th - 90th percentile)"
        ))
        
        # Plot Median (50th percentile)
        fig_mc.add_trace(go.Scatter(
            x=future_dates, y=p50,
            line=dict(color="#4f46e5", width=3),
            name="Median Projection (50th percentile)"
        ))
        
        # Plot a few sample individual paths (e.g. 5 paths)
        for i in range(min(5, N_paths)):
            fig_mc.add_trace(go.Scatter(
                x=future_dates, y=paths[:, i],
                line=dict(width=1, dash="dot"),
                name=f"Sample Path {i+1}",
                opacity=0.5
            ))
            
        fig_mc.update_layout(
            title=dict(text=f"5-Year Growth Projections for {mc_fund}", font=dict(size=15, weight="bold")),
            xaxis_title="Future Date",
            yaxis_title="Portfolio Value (₹)",
            template="plotly_white",
            hovermode="x unified",
            margin=dict(l=40, r=40, t=60, b=40)
        )
        st.plotly_chart(fig_mc, use_container_width=True)
        
        # Details Box
        st.markdown("#### Simulation Statistics")
        col_s1, col_s2, col_s3 = st.columns(3)
        with col_s1:
            st.metric("Expected Median Value", f"₹{p50[-1]:,.2f}", f"{((p50[-1]/mc_investment - 1)*100):.2f}% Growth")
        with col_s2:
            st.metric("Optimistic (90th percentile)", f"₹{p90[-1]:,.2f}")
        with col_s3:
            st.metric("Conservative (10th percentile)", f"₹{p10[-1]:,.2f}")

    # ── TAB 2: Markowitz Portfolio Optimization (B4) ───────────────────────────
    with sim_mode[1]:
        st.markdown("### Markowitz Efficient Frontier")
        st.write("Select exactly 5 funds to simulate random portfolios, calculate risk-return parameters, and identify the optimal allocations.")
        
        # Slicers (At least 2 required)
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
            st.warning("Please select exactly 5 funds to construct the Efficient Frontier.")
        else:
            # Get amfi codes
            port_codes = df_scorecard[df_scorecard["scheme_name"].isin(port_funds)]["amfi_code"].tolist()
            
            # Load NAV histories
            df_port_navs = load_nav_history(port_codes)
            
            # Pivot & clean
            df_port_pivot = df_port_navs.pivot(index="nav_date", columns="scheme_name", values="nav_value")
            
            # Handle weekends: reindex and forward fill
            df_port_pivot = df_port_pivot.reindex(pd.date_range(df_port_pivot.index.min(), df_port_pivot.index.max(), freq='D')).ffill().bfill()
            
            # Daily returns (trading days only)
            df_port_returns = df_port_pivot[df_port_pivot.index.dayofweek < 5].pct_change().dropna()
            
            # Annualized returns and covariance
            ann_returns = df_port_returns.mean() * 252
            ann_cov = df_port_returns.cov() * 252
            
            # Portfolios simulation
            num_ports = sim_portfolios
            results = np.zeros((3 + len(port_codes), num_ports))
            
            rf_daily_proxy = rf_rate / 100.0
            
            np.random.seed(101)
            for i in range(num_ports):
                # Generate random weights summing to 1
                w = np.random.random(5)
                w /= np.sum(w)
                
                # Portfolio Return
                p_ret = np.sum(w * ann_returns)
                
                # Portfolio Volatility
                p_vol = np.sqrt(np.dot(w.T, np.dot(ann_cov, w)))
                
                # Sharpe Ratio
                p_sharpe = (p_ret - rf_daily_proxy) / p_vol
                
                results[0, i] = p_ret
                results[1, i] = p_vol
                results[2, i] = p_sharpe
                
                # store weights
                for j in range(len(w)):
                    results[3 + j, i] = w[j]
                    
            # Dataframe for plotting
            columns_w = [f"w_{name[:15]}" for name in port_funds]
            df_sim_ports = pd.DataFrame(results.T, columns=["Return", "Volatility", "Sharpe"] + columns_w)
            
            # Find key portfolios
            max_sharpe_idx = df_sim_ports["Sharpe"].idxmax()
            max_sharpe_port = df_sim_ports.iloc[max_sharpe_idx]
            
            min_vol_idx = df_sim_ports["Volatility"].idxmin()
            min_vol_port = df_sim_ports.iloc[min_vol_idx]
            
            # Plotly scatter
            fig_ef = go.Figure()
            
            # Sim portfolios
            fig_ef.add_trace(go.Scatter(
                x=df_sim_ports["Volatility"] * 100,
                y=df_sim_ports["Return"] * 100,
                mode="markers",
                marker=dict(
                    color=df_sim_ports["Sharpe"],
                    colorscale="Viridis",
                    showscale=True,
                    colorbar=dict(title="Sharpe Ratio"),
                    size=5
                ),
                text=[f"Sharpe: {s:.2f}" for s in df_sim_ports["Sharpe"]],
                name="Simulated Portfolios",
                showlegend=False
            ))
            
            # Max Sharpe Portfolio
            fig_ef.add_trace(go.Scatter(
                x=[max_sharpe_port["Volatility"] * 100],
                y=[max_sharpe_port["Return"] * 100],
                mode="markers",
                marker=dict(color="red", size=15, symbol="star"),
                name=f"Max Sharpe Ratio ({max_sharpe_port['Sharpe']:.2f})"
            ))
            
            # Min Volatility Portfolio
            fig_ef.add_trace(go.Scatter(
                x=[min_vol_port["Volatility"] * 100],
                y=[min_vol_port["Return"] * 100],
                mode="markers",
                marker=dict(color="green", size=15, symbol="star"),
                name=f"Min Volatility ({min_vol_port['Volatility']*100:.2f}%)"
            ))
            
            fig_ef.update_layout(
                title=dict(text="Efficient Frontier Scatter Plot", font=dict(size=15, weight="bold")),
                xaxis_title="Annualized Volatility (Standard Deviation %)",
                yaxis_title="Expected Annualized Return (%)",
                template="plotly_white",
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                margin=dict(l=40, r=40, t=60, b=40)
            )
            st.plotly_chart(fig_ef, use_container_width=True)
            
            # Display Weights comparison
            st.markdown("#### Optimal Weights Comparison")
            
            col_w1, col_w2 = st.columns(2)
            
            with col_w1:
                st.markdown("**Maximum Sharpe Ratio Portfolio Weights**")
                w_max = max_sharpe_port[[f"w_{n[:15]}" for n in port_funds]].values
                df_w_max = pd.DataFrame({"Fund": port_funds, "Weight (%)": w_max * 100})
                
                fig_w_max = px.bar(df_w_max, x="Fund", y="Weight (%)", color="Fund", text_auto=".1f%", color_discrete_sequence=px.colors.qualitative.Prism)
                fig_w_max.update_layout(showlegend=False, margin=dict(t=20, b=20), height=300)
                st.plotly_chart(fig_w_max, use_container_width=True)
                
                st.dataframe(df_w_max.style.format({"Weight (%)": "{:.2f}%"}), hide_index=True)
                
            with col_w2:
                st.markdown("**Minimum Volatility Portfolio Weights**")
                w_min = min_vol_port[[f"w_{n[:15]}" for n in port_funds]].values
                df_w_min = pd.DataFrame({"Fund": port_funds, "Weight (%)": w_min * 100})
                
                fig_w_min = px.bar(df_w_min, x="Fund", y="Weight (%)", color="Fund", text_auto=".1f%", color_discrete_sequence=px.colors.qualitative.Safe)
                fig_w_min.update_layout(showlegend=False, margin=dict(t=20, b=20), height=300)
                st.plotly_chart(fig_w_min, use_container_width=True)
                
                st.dataframe(df_w_min.style.format({"Weight (%)": "{:.2f}%"}), hide_index=True)

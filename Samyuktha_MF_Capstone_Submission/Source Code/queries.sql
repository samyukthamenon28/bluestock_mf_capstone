-- queries.sql — Bluestock MF Capstone: 10 Analytical SQL Queries (D2)
-- SQLite-compatible SQL

-- ─────────────────────────────────────────────────────────────────────────────
-- Query 1: Top 5 Funds by AUM
-- Identifies the top 5 funds from fact_performance by their assets under management.
-- ─────────────────────────────────────────────────────────────────────────────
SELECT
    f.amfi_code,
    f.scheme_name,
    p.aum_crore,
    p.morningstar_rating
FROM dim_fund f
JOIN fact_performance p ON f.amfi_code = p.amfi_code
ORDER BY p.aum_crore DESC
LIMIT 5;


-- ─────────────────────────────────────────────────────────────────────────────
-- Query 2: Average NAV Per Month for Each Fund
-- Calculates the average NAV value per calendar month for each scheme.
-- ─────────────────────────────────────────────────────────────────────────────
SELECT
    f.scheme_name,
    d.year,
    d.month,
    ROUND(AVG(n.nav_value), 4) AS avg_nav_value
FROM fact_nav n
JOIN dim_fund f ON n.amfi_code = f.amfi_code
JOIN dim_date d ON n.nav_date = d.date_id
GROUP BY f.scheme_name, d.year, d.month
ORDER BY f.scheme_name, d.year, d.month;


-- ─────────────────────────────────────────────────────────────────────────────
-- Query 3: SIP YoY Growth
-- Computes the Year-on-Year growth rate of SIP inflows comparing 2024 vs 2025.
-- ─────────────────────────────────────────────────────────────────────────────
WITH sip_yearly AS (
    SELECT
        d.year,
        SUM(t.amount_inr) AS total_sip_amount
    FROM fact_transactions t
    JOIN dim_date d ON t.transaction_date = d.date_id
    WHERE t.transaction_type = 'SIP'
    GROUP BY d.year
)
SELECT
    curr.year AS current_year,
    curr.total_sip_amount AS current_year_sip,
    prev.year AS previous_year,
    prev.total_sip_amount AS previous_year_sip,
    ROUND((curr.total_sip_amount - prev.total_sip_amount) * 100.0 / prev.total_sip_amount, 2) AS yoy_growth_pct
FROM sip_yearly curr
JOIN sip_yearly prev ON curr.year = prev.year + 1;


-- ─────────────────────────────────────────────────────────────────────────────
-- Query 4: Total Transaction Count and Volume by State
-- Summarizes transactions and aggregate investment amounts for each state.
-- ─────────────────────────────────────────────────────────────────────────────
SELECT
    state,
    COUNT(transaction_id) AS total_transactions,
    SUM(amount_inr) AS total_amount_inr,
    ROUND(AVG(amount_inr), 2) AS avg_transaction_amount_inr
FROM fact_transactions
GROUP BY state
ORDER BY total_amount_inr DESC;


-- ─────────────────────────────────────────────────────────────────────────────
-- Query 5: Funds with Expense Ratio < 1%
-- Retrieves schemes with low operating costs (< 1.0%), sorted by efficiency.
-- ─────────────────────────────────────────────────────────────────────────────
SELECT
    f.amfi_code,
    f.scheme_name,
    p.expense_ratio_pct,
    p.aum_crore
FROM dim_fund f
JOIN fact_performance p ON f.amfi_code = p.amfi_code
WHERE p.expense_ratio_pct < 1.0
ORDER BY p.expense_ratio_pct ASC;


-- ─────────────────────────────────────────────────────────────────────────────
-- Query 6: KYC Verification Status vs Transaction Metrics (Custom)
-- Compares count and average sizes of transactions by KYC status and type.
-- ─────────────────────────────────────────────────────────────────────────────
SELECT
    t.kyc_status,
    t.transaction_type,
    COUNT(t.transaction_id) AS transaction_count,
    SUM(t.amount_inr) AS total_amount_inr,
    ROUND(AVG(t.amount_inr), 2) AS avg_transaction_amount_inr
FROM fact_transactions t
GROUP BY t.kyc_status, t.transaction_type
ORDER BY t.kyc_status, transaction_count DESC;


-- ─────────────────────────────────────────────────────────────────────────────
-- Query 7: Risk Category Performance Profile (Custom)
-- Groups funds by risk category to observe average 3y return and Sharpe ratios.
-- ─────────────────────────────────────────────────────────────────────────────
SELECT
    f.risk_category,
    COUNT(f.amfi_code) AS fund_count,
    ROUND(AVG(p.return_3yr_pct), 2) AS avg_3yr_return_pct,
    ROUND(AVG(p.sharpe_ratio), 2) AS avg_sharpe_ratio,
    ROUND(AVG(p.beta), 2) AS avg_beta
FROM dim_fund f
JOIN fact_performance p ON f.amfi_code = p.amfi_code
GROUP BY f.risk_category
ORDER BY avg_3yr_return_pct DESC;


-- ─────────────────────────────────────────────────────────────────────────────
-- Query 8: Payment Mode Preference by City Tier (Custom)
-- Analyzes payment mode adoption share within Top-30 vs Beyond-30 city tiers.
-- ─────────────────────────────────────────────────────────────────────────────
WITH tier_totals AS (
    SELECT
        city_tier,
        payment_mode,
        COUNT(transaction_id) AS transaction_count,
        SUM(amount_inr) AS total_amount_inr
    FROM fact_transactions
    GROUP BY city_tier, payment_mode
)
SELECT
    city_tier,
    payment_mode,
    transaction_count,
    total_amount_inr,
    ROUND(transaction_count * 100.0 / SUM(transaction_count) OVER(PARTITION BY city_tier), 2) AS tier_share_pct
FROM tier_totals
ORDER BY city_tier, transaction_count DESC;


-- ─────────────────────────────────────────────────────────────────────────────
-- Query 9: Top 10 Portfolio Stock Exposures Across All Funds (Custom)
-- Evaluates the largest underlying equity holdings aggregated across funds.
-- ─────────────────────────────────────────────────────────────────────────────
SELECT
    ph.stock_name,
    ph.stock_symbol,
    ph.sector,
    COUNT(DISTINCT ph.amfi_code) AS holding_funds_count,
    ROUND(SUM(ph.market_value_cr), 2) AS aggregate_market_value_cr,
    ROUND(AVG(ph.weight_pct), 2) AS avg_weight_pct
FROM portfolio_holdings ph
JOIN dim_fund f ON ph.amfi_code = f.amfi_code
GROUP BY ph.stock_name, ph.stock_symbol, ph.sector
ORDER BY aggregate_market_value_cr DESC
LIMIT 10;


-- ─────────────────────────────────────────────────────────────────────────────
-- Query 10: Index Benchmark Correlation with Monthly Scheme NAV (Custom)
-- Compares average scheme NAVs with index values (NIFTY50/NIFTY100) over time.
-- ─────────────────────────────────────────────────────────────────────────────
SELECT
    d.year,
    d.month,
    f.scheme_name,
    ROUND(AVG(n.nav_value), 2) AS avg_nav_value,
    ROUND(AVG(bi.close_value), 2) AS avg_benchmark_value
FROM fact_nav n
JOIN dim_fund f ON n.amfi_code = f.amfi_code
JOIN dim_date d ON n.nav_date = d.date_id
LEFT JOIN benchmark_indices bi ON bi.date = n.nav_date AND bi.index_name = (
    CASE
        WHEN f.benchmark LIKE '%100%' THEN 'NIFTY100'
        ELSE 'NIFTY50'
    END
)
GROUP BY d.year, d.month, f.scheme_name
ORDER BY f.scheme_name, d.year, d.month
LIMIT 20;

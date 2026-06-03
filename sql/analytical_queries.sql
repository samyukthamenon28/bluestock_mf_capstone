-- sql/analytical_queries.sql — Bluestock MF Capstone: Analytical Queries (D2)
-- SQLite-compatible SQL

-- ─────────────────────────────────────────────────────────────────────────────
-- Query 1: Total Transaction Volume and Net Inflows by Fund House
-- Summarizes total transaction counts, investments, redemptions, and net flows.
-- ─────────────────────────────────────────────────────────────────────────────
-- EXPLAIN: Grouping facts by dim_schemes.fund_house to understand market activity.
SELECT
    s.fund_house,
    COUNT(t.transaction_id) AS total_transaction_count,
    SUM(CASE WHEN t.transaction_type IN ('SIP', 'Lumpsum') THEN t.amount_inr ELSE 0 END) AS total_investment_amount_inr,
    SUM(CASE WHEN t.transaction_type = 'Redemption' THEN t.amount_inr ELSE 0 END) AS total_redemption_amount_inr,
    SUM(CASE WHEN t.transaction_type IN ('SIP', 'Lumpsum') THEN t.amount_inr ELSE -t.amount_inr END) AS net_inflow_inr
FROM fact_transactions t
JOIN dim_schemes s ON t.amfi_code = s.amfi_code
GROUP BY s.fund_house
ORDER BY net_inflow_inr DESC;


-- ─────────────────────────────────────────────────────────────────────────────
-- Query 2: Top 3 Performing Schemes within Each Category (by 3-Year Return)
-- Ranks schemes using window functions to find the top performers per category.
-- ─────────────────────────────────────────────────────────────────────────────
-- EXPLAIN: Window DENSE_RANK() partitioned by category to rank schemes dynamically.
WITH RankedSchemes AS (
    SELECT
        category,
        scheme_name,
        return_3yr_pct,
        sharpe_ratio,
        aum_crore,
        DENSE_RANK() OVER (PARTITION BY category ORDER BY return_3yr_pct DESC) as rank
    FROM dim_schemes
)
SELECT category, rank, scheme_name, return_3yr_pct, sharpe_ratio, aum_crore
FROM RankedSchemes
WHERE rank <= 3
ORDER BY category, rank;


-- ─────────────────────────────────────────────────────────────────────────────
-- Query 3: Underperforming Schemes Relative to Their 3-Year Benchmarks
-- Highlights schemes where returns lag the benchmark, including risk statistics.
-- ─────────────────────────────────────────────────────────────────────────────
-- EXPLAIN: Comparative join of performance and benchmark returns to flag underperformance.
SELECT
    amfi_code,
    scheme_name,
    category,
    return_3yr_pct,
    benchmark_3yr_pct,
    ROUND((return_3yr_pct - benchmark_3yr_pct), 2) AS underperformance_pct,
    alpha,
    beta
FROM dim_schemes
WHERE return_3yr_pct < benchmark_3yr_pct
ORDER BY underperformance_pct ASC;


-- ─────────────────────────────────────────────────────────────────────────────
-- Query 4: Geographic Investment Distribution by State and City Tier
-- Analyzes where the capital is flowing from, including average ticket size.
-- ─────────────────────────────────────────────────────────────────────────────
-- EXPLAIN: Joins transaction facts with dim_investors to show geographic contribution.
SELECT
    i.state,
    i.city_tier,
    COUNT(t.transaction_id) AS transaction_count,
    SUM(t.amount_inr) AS total_amount_inr,
    ROUND(AVG(t.amount_inr), 2) AS avg_transaction_amount_inr
FROM fact_transactions t
JOIN dim_investors i ON t.investor_id = i.investor_id
GROUP BY i.state, i.city_tier
ORDER BY total_amount_inr DESC;


-- ─────────────────────────────────────────────────────────────────────────────
-- Query 5: Monthly Inflow Trends (SIP vs Lumpsum vs Redemption Counts & Volumes)
-- Identifies seasonal trends and transaction behavior over time.
-- ─────────────────────────────────────────────────────────────────────────────
-- EXPLAIN: Utilizes shared dim_dates to aggregate facts month-over-month.
SELECT
    d.year,
    d.month,
    SUM(CASE WHEN t.transaction_type = 'SIP' THEN 1 ELSE 0 END) AS sip_count,
    SUM(CASE WHEN t.transaction_type = 'SIP' THEN t.amount_inr ELSE 0 END) AS sip_volume_inr,
    SUM(CASE WHEN t.transaction_type = 'Lumpsum' THEN 1 ELSE 0 END) AS lumpsum_count,
    SUM(CASE WHEN t.transaction_type = 'Lumpsum' THEN t.amount_inr ELSE 0 END) AS lumpsum_volume_inr,
    SUM(CASE WHEN t.transaction_type = 'Redemption' THEN 1 ELSE 0 END) AS redemption_count,
    SUM(CASE WHEN t.transaction_type = 'Redemption' THEN t.amount_inr ELSE 0 END) AS redemption_volume_inr
FROM fact_transactions t
JOIN dim_dates d ON t.transaction_date = d.date_id
GROUP BY d.year, d.month
ORDER BY d.year, d.month;


-- ─────────────────────────────────────────────────────────────────────────────
-- Query 6: Demographic Profiling (Age Group and Gender Investment Behaviors)
-- Analyzes unique investor counts and ticket sizes by cohort.
-- ─────────────────────────────────────────────────────────────────────────────
-- EXPLAIN: Combines transaction values and unique investor counts across demographics.
SELECT
    i.age_group,
    i.gender,
    COUNT(DISTINCT t.investor_id) AS unique_investor_count,
    COUNT(t.transaction_id) AS total_transaction_count,
    SUM(t.amount_inr) AS total_amount_inr,
    ROUND(SUM(t.amount_inr) * 1.0 / COUNT(t.transaction_id), 2) AS avg_ticket_size_inr
FROM fact_transactions t
JOIN dim_investors i ON t.investor_id = i.investor_id
GROUP BY i.age_group, i.gender
ORDER BY i.age_group, i.gender;


-- ─────────────────────────────────────────────────────────────────────────────
-- Query 7: Income Bracket Correlation with Transaction Sizes
-- Groups investors into annual income brackets to observe ticket size variances.
-- ─────────────────────────────────────────────────────────────────────────────
-- EXPLAIN: Bins continuous income figures using a CTE, then runs aggregates.
WITH binned_income AS (
    SELECT
        CASE
            WHEN annual_income_lakh < 10 THEN '1. 0-10 Lakh'
            WHEN annual_income_lakh >= 10 AND annual_income_lakh < 25 THEN '2. 10-25 Lakh'
            WHEN annual_income_lakh >= 25 AND annual_income_lakh < 50 THEN '3. 25-50 Lakh'
            WHEN annual_income_lakh >= 50 AND annual_income_lakh < 75 THEN '4. 50-75 Lakh'
            ELSE '5. 75+ Lakh'
        END AS income_bracket,
        t.amount_inr
    FROM fact_transactions t
    JOIN dim_investors i ON t.investor_id = i.investor_id
)
SELECT
    income_bracket,
    COUNT(*) AS transaction_count,
    SUM(amount_inr) AS total_amount_inr,
    ROUND(AVG(amount_inr), 2) AS avg_transaction_amount_inr
FROM binned_income
GROUP BY income_bracket
ORDER BY income_bracket;


-- ─────────────────────────────────────────────────────────────────────────────
-- Query 8: Payment Mode Preferences by City Tier
-- Displays distribution and share of payment methods in Top-30 vs Beyond-30 cities.
-- ─────────────────────────────────────────────────────────────────────────────
-- EXPLAIN: Grouping by tier and payment mode with window SUM to calculate percentages.
WITH tier_totals AS (
    SELECT
        i.city_tier,
        t.payment_mode,
        COUNT(t.transaction_id) AS transaction_count,
        SUM(t.amount_inr) AS total_amount_inr
    FROM fact_transactions t
    JOIN dim_investors i ON t.investor_id = i.investor_id
    GROUP BY i.city_tier, t.payment_mode
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
-- Query 9: KYC Verification Status vs Investment Activity
-- Investigates if KYC status affects transaction counts and investment volumes.
-- ─────────────────────────────────────────────────────────────────────────────
-- EXPLAIN: Aggregates total transactions and ticket size by KYC and transaction type.
SELECT
    t.kyc_status,
    t.transaction_type,
    COUNT(t.transaction_id) AS transaction_count,
    SUM(t.amount_inr) AS total_amount_inr,
    ROUND(AVG(t.amount_inr), 2) AS avg_amount_inr
FROM fact_transactions t
GROUP BY t.kyc_status, t.transaction_type
ORDER BY t.kyc_status, transaction_count DESC;


-- ─────────────────────────────────────────────────────────────────────────────
-- Query 10: Top 10 Stock Holdings Across All Portfolios by Market Value
-- Integrates scheme facts with scheme portfolio holdings to find biggest positions.
-- ─────────────────────────────────────────────────────────────────────────────
-- EXPLAIN: Joins D1 portfolio_holdings with dim_schemes to find overall exposure.
SELECT
    h.stock_name,
    h.stock_symbol,
    h.sector,
    COUNT(DISTINCT h.amfi_code) AS holding_schemes_count,
    ROUND(SUM(h.market_value_cr), 2) AS total_market_value_cr,
    ROUND(AVG(h.weight_pct), 2) AS avg_weight_pct
FROM `09_portfolio_holdings` h
JOIN dim_schemes s ON h.amfi_code = s.amfi_code
GROUP BY h.stock_name, h.stock_symbol, h.sector
ORDER BY total_market_value_cr DESC
LIMIT 10;

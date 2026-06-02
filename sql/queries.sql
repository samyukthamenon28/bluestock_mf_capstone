-- queries.sql — Bluestock MF Capstone: Common Analytical Queries

-- ─── 1. Latest NAV for all schemes ───────────────────────────────────────────
SELECT
    scheme_code,
    scheme_name,
    fund_house,
    MAX(nav_date)  AS latest_date,
    nav_value      AS latest_nav
FROM nav_history
WHERE nav_date = (
    SELECT MAX(nav_date) FROM nav_history nh2
    WHERE nh2.scheme_code = nav_history.scheme_code
)
GROUP BY scheme_code
ORDER BY fund_house, scheme_name;


-- ─── 2. 1-Year Absolute Return ────────────────────────────────────────────────
WITH latest AS (
    SELECT scheme_code, nav_value AS nav_now, MAX(nav_date) AS latest_date
    FROM nav_history GROUP BY scheme_code
),
one_year_ago AS (
    SELECT nh.scheme_code,
           nh.nav_value AS nav_1y,
           nh.nav_date  AS date_1y
    FROM nav_history nh
    JOIN latest l ON nh.scheme_code = l.scheme_code
    WHERE nh.nav_date = date(l.latest_date, '-365 days')
)
SELECT
    l.scheme_code,
    ROUND((l.nav_now - o.nav_1y) / o.nav_1y * 100, 2) AS return_1y_pct
FROM latest l
JOIN one_year_ago o ON l.scheme_code = o.scheme_code
ORDER BY return_1y_pct DESC;


-- ─── 3. Fund-house AUM market share (latest month) ───────────────────────────
WITH latest_month AS (SELECT MAX(aum_month) AS m FROM aum_history)
SELECT
    fm.fund_house,
    ROUND(SUM(ah.aum_crore), 2)                               AS total_aum_crore,
    ROUND(SUM(ah.aum_crore) * 100.0 / SUM(SUM(ah.aum_crore)) OVER (), 2) AS share_pct
FROM aum_history ah
JOIN fund_master fm ON ah.scheme_code = fm.scheme_code
JOIN latest_month lm ON ah.aum_month = lm.m
GROUP BY fm.fund_house
ORDER BY total_aum_crore DESC;


-- ─── 4. NAV drawdown per scheme (max-to-trough) ───────────────────────────────
WITH running_max AS (
    SELECT
        scheme_code,
        nav_date,
        nav_value,
        MAX(nav_value) OVER (
            PARTITION BY scheme_code
            ORDER BY nav_date
            ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
        ) AS peak_nav
    FROM nav_history
)
SELECT
    scheme_code,
    MIN(ROUND((nav_value - peak_nav) / peak_nav * 100, 2)) AS max_drawdown_pct
FROM running_max
GROUP BY scheme_code
ORDER BY max_drawdown_pct;


-- ─── 5. Category-wise average returns ─────────────────────────────────────────
SELECT
    fm.scheme_category,
    COUNT(DISTINCT r.scheme_code) AS n_schemes,
    ROUND(AVG(r.return_1y),  2) AS avg_1y_return,
    ROUND(AVG(r.return_3y),  2) AS avg_3y_return,
    ROUND(AVG(r.sharpe_ratio), 3) AS avg_sharpe,
    ROUND(AVG(r.max_drawdown), 2) AS avg_max_drawdown
FROM returns r
JOIN fund_master fm ON r.scheme_code = fm.scheme_code
WHERE r.as_of_date = (SELECT MAX(as_of_date) FROM returns)
GROUP BY fm.scheme_category
ORDER BY avg_1y_return DESC;


-- ─── 6. Validate AMFI codes — codes in fund_master but missing from nav_history
SELECT fm.scheme_code, fm.scheme_name
FROM fund_master fm
LEFT JOIN nav_history nh ON fm.scheme_code = nh.scheme_code
WHERE nh.scheme_code IS NULL;


-- ─── 7. Top 10 best-performing schemes (1-year) ───────────────────────────────
SELECT
    r.scheme_code,
    fm.scheme_name,
    fm.fund_house,
    fm.scheme_category,
    r.return_1y   AS return_1y_pct,
    r.sharpe_ratio,
    r.max_drawdown
FROM returns r
JOIN fund_master fm ON r.scheme_code = fm.scheme_code
WHERE r.as_of_date = (SELECT MAX(as_of_date) FROM returns)
ORDER BY r.return_1y DESC
LIMIT 10;

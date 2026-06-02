-- schema.sql — Bluestock MF Capstone Database Schema
-- SQLite-compatible DDL

-- ─────────────────────────────────────────────────────────────────────────────
-- fund_master: One row per mutual fund scheme
-- ─────────────────────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS fund_master (
    scheme_code         INTEGER PRIMARY KEY,
    scheme_name         TEXT    NOT NULL,
    fund_house          TEXT,
    scheme_type         TEXT,                 -- Open-ended / Close-ended
    scheme_category     TEXT,                 -- Equity / Debt / Hybrid
    scheme_sub_category TEXT,
    risk_grade          TEXT,                 -- Low / Moderate / High / Very High
    launch_date         DATE,
    benchmark_index     TEXT
);

-- ─────────────────────────────────────────────────────────────────────────────
-- nav_history: Daily NAV for each scheme (full calendar, ffill applied)
-- ─────────────────────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS nav_history (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    scheme_code     INTEGER NOT NULL REFERENCES fund_master(scheme_code),
    nav_date        DATE    NOT NULL,
    nav_value       REAL    NOT NULL,
    scheme_name     TEXT,
    scheme_category TEXT,
    scheme_type     TEXT,
    fund_house      TEXT,
    UNIQUE (scheme_code, nav_date)
);

CREATE INDEX IF NOT EXISTS idx_nav_scheme_date ON nav_history(scheme_code, nav_date);
CREATE INDEX IF NOT EXISTS idx_nav_date ON nav_history(nav_date);

-- ─────────────────────────────────────────────────────────────────────────────
-- aum_history: Monthly AUM in INR Crore (scheme-level, NOT lakh-crore)
-- ─────────────────────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS aum_history (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    scheme_code     INTEGER NOT NULL REFERENCES fund_master(scheme_code),
    aum_month       DATE    NOT NULL,             -- First day of month
    aum_crore       REAL,                         -- AUM in INR Crore
    UNIQUE (scheme_code, aum_month)
);

-- ─────────────────────────────────────────────────────────────────────────────
-- portfolio_holdings: Top-N holdings for a scheme at a point in time
-- ─────────────────────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS portfolio_holdings (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    scheme_code     INTEGER NOT NULL REFERENCES fund_master(scheme_code),
    holding_date    DATE    NOT NULL,
    isin            TEXT,
    company_name    TEXT,
    sector          TEXT,
    weight_pct      REAL,                         -- % allocation
    market_value_cr REAL                          -- Market value in INR Crore
);

-- ─────────────────────────────────────────────────────────────────────────────
-- returns: Pre-computed return metrics (populated by compute_metrics.py)
-- ─────────────────────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS returns (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    scheme_code     INTEGER NOT NULL REFERENCES fund_master(scheme_code),
    as_of_date      DATE    NOT NULL,
    return_1m       REAL,
    return_3m       REAL,
    return_6m       REAL,
    return_1y       REAL,
    return_3y       REAL,
    return_5y       REAL,
    cagr_since_launch REAL,
    sharpe_ratio    REAL,
    beta            REAL,
    alpha           REAL,
    std_dev_ann     REAL,
    max_drawdown    REAL,
    var_95          REAL,                         -- 95% Historical VaR
    UNIQUE (scheme_code, as_of_date)
);

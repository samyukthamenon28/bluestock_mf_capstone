-- sql/star_schema.sql — Bluestock MF Capstone: Star Schema Definition
-- SQLite-compatible DDL

-- Enable foreign keys (needs to be run per connection in SQLite, but documented here)
PRAGMA foreign_keys = ON;

-- ─────────────────────────────────────────────────────────────────────────────
-- Dimension: dim_schemes
-- Combines master static data (from 01_fund_master) and performance metrics (from 07_scheme_performance)
-- ─────────────────────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS dim_schemes (
    amfi_code               INTEGER PRIMARY KEY,
    scheme_name             TEXT NOT NULL,
    fund_house              TEXT,
    category                TEXT,
    sub_category            TEXT,
    plan                    TEXT,                 -- Regular / Direct
    launch_date             TEXT,                 -- YYYY-MM-DD
    benchmark               TEXT,
    expense_ratio_pct       REAL,
    exit_load_pct           REAL,
    min_sip_amount          REAL,
    min_lumpsum_amount      REAL,
    fund_manager            TEXT,
    sebi_category_code      TEXT,
    risk_grade              TEXT,                 -- e.g. Low, Moderate, High, Very High
    morningstar_rating      INTEGER,
    return_1yr_pct          REAL,
    return_3yr_pct          REAL,
    return_5yr_pct          REAL,
    benchmark_3yr_pct       REAL,
    alpha                   REAL,
    beta                    REAL,
    sharpe_ratio            REAL,
    sortino_ratio           REAL,
    std_dev_ann_pct         REAL,
    max_drawdown_pct        REAL,
    aum_crore               REAL                  -- Scheme-level AUM in INR Crore
);

-- ─────────────────────────────────────────────────────────────────────────────
-- Dimension: dim_investors
-- Unique investors and their demographic properties extracted from transactions
-- ─────────────────────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS dim_investors (
    investor_id             TEXT PRIMARY KEY,
    state                   TEXT,
    city                    TEXT,
    city_tier               TEXT,                 -- T30 / B30
    age_group               TEXT,                 -- 18-25, 26-35, etc.
    gender                  TEXT,                 -- Male / Female
    annual_income_lakh      REAL
);

-- ─────────────────────────────────────────────────────────────────────────────
-- Dimension: dim_dates
-- Shared calendar date dimension to simplify time-based queries
-- ─────────────────────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS dim_dates (
    date_id                 TEXT PRIMARY KEY,     -- 'YYYY-MM-DD'
    day                     INTEGER NOT NULL,
    month                   INTEGER NOT NULL,
    year                    INTEGER NOT NULL,
    quarter                 INTEGER NOT NULL,     -- 1, 2, 3, 4
    day_of_week             TEXT NOT NULL,        -- Monday, Tuesday, etc.
    is_weekend              INTEGER NOT NULL      -- 0 (False), 1 (True)
);

-- ─────────────────────────────────────────────────────────────────────────────
-- Fact Table: fact_transactions
-- Granular transaction facts (SIP, Lumpsum, Redemption)
-- ─────────────────────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS fact_transactions (
    transaction_id          INTEGER PRIMARY KEY AUTOINCREMENT,
    investor_id             TEXT NOT NULL REFERENCES dim_investors(investor_id),
    transaction_date        TEXT NOT NULL REFERENCES dim_dates(date_id),
    amfi_code               INTEGER NOT NULL REFERENCES dim_schemes(amfi_code),
    transaction_type        TEXT NOT NULL,        -- SIP / Lumpsum / Redemption
    amount_inr              REAL NOT NULL,
    payment_mode            TEXT,
    kyc_status              TEXT                  -- Verified / Pending
);

CREATE INDEX IF NOT EXISTS idx_fact_trans_investor ON fact_transactions(investor_id);
CREATE INDEX IF NOT EXISTS idx_fact_trans_date ON fact_transactions(transaction_date);
CREATE INDEX IF NOT EXISTS idx_fact_trans_scheme ON fact_transactions(amfi_code);

-- ─────────────────────────────────────────────────────────────────────────────
-- Fact Table: fact_nav_history
-- Periodic daily snapshot of NAV for all schemes (full calendar, ffill applied)
-- ─────────────────────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS fact_nav_history (
    id                      INTEGER PRIMARY KEY AUTOINCREMENT,
    amfi_code               INTEGER NOT NULL REFERENCES dim_schemes(amfi_code),
    nav_date                TEXT NOT NULL REFERENCES dim_dates(date_id),
    nav_value               REAL NOT NULL,
    UNIQUE (amfi_code, nav_date)
);

CREATE INDEX IF NOT EXISTS idx_fact_nav_scheme_date ON fact_nav_history(amfi_code, nav_date);
CREATE INDEX IF NOT EXISTS idx_fact_nav_date ON fact_nav_history(nav_date);

-- schema.sql — Bluestock MF Capstone: Custom Star Schema Definition
-- SQLite-compatible DDL

PRAGMA foreign_keys = ON;

-- ─────────────────────────────────────────────────────────────────────────────
-- Dimension: dim_fund
-- Static properties of mutual fund schemes
-- ─────────────────────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS dim_fund (
    amfi_code               INTEGER PRIMARY KEY,
    fund_house              TEXT,
    scheme_name             TEXT NOT NULL,
    category                TEXT,
    sub_category            TEXT,
    plan                    TEXT,                 -- Regular / Direct
    launch_date             TEXT,                 -- YYYY-MM-DD
    benchmark               TEXT,
    min_sip_amount          REAL,
    min_lumpsum_amount      REAL,
    fund_manager            TEXT,
    risk_category           TEXT,                 -- from fund master
    sebi_category_code      TEXT
);

-- ─────────────────────────────────────────────────────────────────────────────
-- Dimension: dim_date
-- Shared calendar date dimension
-- ─────────────────────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS dim_date (
    date_id                 TEXT PRIMARY KEY,     -- 'YYYY-MM-DD' or 'YYYY-MM'
    day                     INTEGER,
    month                   INTEGER NOT NULL,
    year                    INTEGER NOT NULL,
    quarter                 INTEGER NOT NULL,     -- 1, 2, 3, 4
    day_of_week             TEXT,                 -- Monday, Tuesday, etc.
    is_weekend              INTEGER               -- 0 (False), 1 (True)
);

-- ─────────────────────────────────────────────────────────────────────────────
-- Fact Table: fact_nav
-- Daily Net Asset Value facts
-- ─────────────────────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS fact_nav (
    id                      INTEGER PRIMARY KEY AUTOINCREMENT,
    amfi_code               INTEGER NOT NULL REFERENCES dim_fund(amfi_code),
    nav_date                TEXT NOT NULL REFERENCES dim_date(date_id),
    nav_value               REAL NOT NULL,
    UNIQUE (amfi_code, nav_date)
);

CREATE INDEX IF NOT EXISTS idx_fact_nav_fund_date ON fact_nav(amfi_code, nav_date);
CREATE INDEX IF NOT EXISTS idx_fact_nav_date ON fact_nav(nav_date);

-- ─────────────────────────────────────────────────────────────────────────────
-- Fact Table: fact_transactions
-- Detailed transaction facts and investor attributes
-- ─────────────────────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS fact_transactions (
    transaction_id          INTEGER PRIMARY KEY AUTOINCREMENT,
    investor_id             TEXT NOT NULL,
    transaction_date        TEXT NOT NULL REFERENCES dim_date(date_id),
    amfi_code               INTEGER NOT NULL REFERENCES dim_fund(amfi_code),
    transaction_type        TEXT NOT NULL,        -- SIP / Lumpsum / Redemption
    amount_inr              REAL NOT NULL,
    payment_mode            TEXT,
    kyc_status              TEXT,                 -- Verified / Pending
    state                   TEXT,
    city                    TEXT,
    city_tier               TEXT,                 -- T30 / B30
    age_group               TEXT,
    gender                  TEXT,
    annual_income_lakh      REAL
);

CREATE INDEX IF NOT EXISTS idx_fact_trans_date ON fact_transactions(transaction_date);
CREATE INDEX IF NOT EXISTS idx_fact_trans_fund ON fact_transactions(amfi_code);
CREATE INDEX IF NOT EXISTS idx_fact_trans_investor ON fact_transactions(investor_id);

-- ─────────────────────────────────────────────────────────────────────────────
-- Fact Table: fact_performance
-- Performance metrics facts for each scheme
-- ─────────────────────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS fact_performance (
    amfi_code               INTEGER PRIMARY KEY REFERENCES dim_fund(amfi_code),
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
    aum_crore               REAL,
    expense_ratio_pct       REAL,
    morningstar_rating      INTEGER,
    risk_grade              TEXT                  -- from scheme performance
);

-- ─────────────────────────────────────────────────────────────────────────────
-- Fact Table: fact_aum
-- Monthly AUM facts by fund house
-- ─────────────────────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS fact_aum (
    id                      INTEGER PRIMARY KEY AUTOINCREMENT,
    aum_date                TEXT NOT NULL REFERENCES dim_date(date_id),
    fund_house              TEXT NOT NULL,
    aum_lakh_crore          REAL,
    aum_crore               REAL,
    num_schemes             INTEGER
);

CREATE INDEX IF NOT EXISTS idx_fact_aum_date ON fact_aum(aum_date);

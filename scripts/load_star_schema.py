"""
load_star_schema.py — Bluestock MF Capstone: Load All Cleaned Datasets (D2)
Orchestrates table creation and populates the SQLite database,
verifying that loaded row counts match all 10 source CSVs.
"""

import os
import logging
import sqlite3
from pathlib import Path
import pandas as pd
from sqlalchemy import create_engine

# ── Paths ──────────────────────────────────────────────────────────────────────
ROOT = Path(__file__).resolve().parent.parent
PROC_DIR = ROOT / "data" / "processed"
DB_PATH = ROOT / "data" / "db" / "bluestock_mf.db"
SQL_DDL_PATH = ROOT / "schema.sql"

# ── Logging ────────────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(ROOT / "etl_load.log"),
    ],
)
log = logging.getLogger(__name__)


def drop_existing_tables(conn: sqlite3.Connection):
    """Drop all tables in correct dependency order."""
    log.info("Dropping existing tables to start fresh...")
    cursor = conn.cursor()
    # Drop facts
    cursor.execute("DROP TABLE IF EXISTS fact_transactions;")
    cursor.execute("DROP TABLE IF EXISTS fact_nav;")
    cursor.execute("DROP TABLE IF EXISTS fact_performance;")
    cursor.execute("DROP TABLE IF EXISTS fact_aum;")
    # Drop dimensions
    cursor.execute("DROP TABLE IF EXISTS dim_fund;")
    cursor.execute("DROP TABLE IF EXISTS dim_date;")
    # Drop other tables
    cursor.execute("DROP TABLE IF EXISTS portfolio_holdings;")
    cursor.execute("DROP TABLE IF EXISTS benchmark_indices;")
    cursor.execute("DROP TABLE IF EXISTS monthly_sip_inflows;")
    cursor.execute("DROP TABLE IF EXISTS category_inflows;")
    cursor.execute("DROP TABLE IF EXISTS industry_folio_count;")
    conn.commit()


def run_ddl(conn: sqlite3.Connection):
    """Execute the DDL script."""
    log.info("Executing DDL script from %s ...", SQL_DDL_PATH.name)
    with open(SQL_DDL_PATH, "r", encoding="utf-8") as f:
        ddl_script = f.read()
    conn.executescript(ddl_script)
    conn.commit()


def load_data():
    """Load all 10 cleaned datasets into SQLite and verify row counts."""
    engine = create_engine(f"sqlite:///{DB_PATH}")
    
    # Drop and recreate schema
    conn_raw = sqlite3.connect(DB_PATH)
    drop_existing_tables(conn_raw)
    run_ddl(conn_raw)
    conn_raw.close()

    log.info("Populating Database Tables...")

    # Load 10 Cleaned CSVs
    # 1. dim_fund (from fund_master_clean.csv)
    fund_df = pd.read_csv(PROC_DIR / "fund_master_clean.csv")
    dim_fund = fund_df[[
        "amfi_code", "fund_house", "scheme_name", "category", "sub_category",
        "plan", "launch_date", "benchmark", "min_sip_amount", "min_lumpsum_amount",
        "fund_manager", "risk_category", "sebi_category_code"
    ]]
    dim_fund.to_sql("dim_fund", engine, if_exists="append", index=False)
    log.info("Loaded dim_fund: %d rows", len(dim_fund))

    # 2. dim_date (generated calendar)
    nav_df = pd.read_csv(PROC_DIR / "nav_history_clean.csv")
    trans_df = pd.read_csv(PROC_DIR / "investor_transactions_clean.csv")
    aum_df = pd.read_csv(PROC_DIR / "aum_by_fund_house_clean.csv")
    
    all_dates = pd.concat([
        nav_df["date"],
        trans_df["transaction_date"],
        aum_df["date"]
    ]).dropna().unique()
    
    dates_df = pd.DataFrame({"date_id": all_dates})
    dates_df["date_id"] = pd.to_datetime(dates_df["date_id"])
    dates_df.sort_values("date_id", inplace=True)
    
    dates_df["day"] = dates_df["date_id"].dt.day
    dates_df["month"] = dates_df["date_id"].dt.month
    dates_df["year"] = dates_df["date_id"].dt.year
    dates_df["quarter"] = dates_df["date_id"].dt.quarter
    dates_df["day_of_week"] = dates_df["date_id"].dt.day_name()
    dates_df["is_weekend"] = dates_df["date_id"].dt.dayofweek.isin([5, 6]).astype(int)
    dates_df["date_id"] = dates_df["date_id"].dt.strftime("%Y-%m-%d")
    
    dates_df.to_sql("dim_date", engine, if_exists="append", index=False)
    log.info("Loaded dim_date: %d rows", len(dates_df))

    # 3. fact_nav (from nav_history_clean.csv)
    fact_nav = nav_df[["amfi_code", "date", "nav"]].rename(
        columns={"date": "nav_date", "nav": "nav_value"}
    )
    fact_nav.to_sql("fact_nav", engine, if_exists="append", index=False)
    log.info("Loaded fact_nav: %d rows", len(fact_nav))

    # 4. fact_transactions (from investor_transactions_clean.csv)
    fact_trans = trans_df[[
        "investor_id", "transaction_date", "amfi_code", "transaction_type",
        "amount_inr", "payment_mode", "kyc_status", "state", "city",
        "city_tier", "age_group", "gender", "annual_income_lakh"
    ]]
    fact_trans.to_sql("fact_transactions", engine, if_exists="append", index=False)
    log.info("Loaded fact_transactions: %d rows", len(fact_trans))

    # 5. fact_performance (from scheme_performance_clean.csv)
    perf_df = pd.read_csv(PROC_DIR / "scheme_performance_clean.csv")
    fact_perf = perf_df[[
        "amfi_code", "return_1yr_pct", "return_3yr_pct", "return_5yr_pct",
        "benchmark_3yr_pct", "alpha", "beta", "sharpe_ratio", "sortino_ratio",
        "std_dev_ann_pct", "max_drawdown_pct", "aum_crore", "expense_ratio_pct",
        "morningstar_rating", "risk_grade"
    ]]
    fact_perf.to_sql("fact_performance", engine, if_exists="append", index=False)
    log.info("Loaded fact_performance: %d rows", len(fact_perf))

    # 6. fact_aum (from aum_by_fund_house_clean.csv)
    fact_aum = aum_df[["date", "fund_house", "aum_lakh_crore", "aum_crore", "num_schemes"]].rename(
        columns={"date": "aum_date"}
    )
    fact_aum.to_sql("fact_aum", engine, if_exists="append", index=False)
    log.info("Loaded fact_aum: %d rows", len(fact_aum))

    # Load remaining 5 cleaned CSVs as supporting tables
    # 7. portfolio_holdings (from portfolio_holdings_clean.csv)
    ph_df = pd.read_csv(PROC_DIR / "portfolio_holdings_clean.csv")
    ph_df.to_sql("portfolio_holdings", engine, if_exists="replace", index=False)
    log.info("Loaded portfolio_holdings: %d rows", len(ph_df))

    # 8. benchmark_indices (from benchmark_indices_clean.csv)
    bi_df = pd.read_csv(PROC_DIR / "benchmark_indices_clean.csv")
    bi_df.to_sql("benchmark_indices", engine, if_exists="replace", index=False)
    log.info("Loaded benchmark_indices: %d rows", len(bi_df))

    # 9. monthly_sip_inflows (from monthly_sip_inflows_clean.csv)
    msi_df = pd.read_csv(PROC_DIR / "monthly_sip_inflows_clean.csv")
    msi_df.to_sql("monthly_sip_inflows", engine, if_exists="replace", index=False)
    log.info("Loaded monthly_sip_inflows: %d rows", len(msi_df))

    # 10. category_inflows (from category_inflows_clean.csv)
    ci_df = pd.read_csv(PROC_DIR / "category_inflows_clean.csv")
    ci_df.to_sql("category_inflows", engine, if_exists="replace", index=False)
    log.info("Loaded category_inflows: %d rows", len(ci_df))

    # 11. industry_folio_count (from industry_folio_count_clean.csv)
    ifc_df = pd.read_csv(PROC_DIR / "industry_folio_count_clean.csv")
    ifc_df.to_sql("industry_folio_count", engine, if_exists="replace", index=False)
    log.info("Loaded industry_folio_count: %d rows", len(ifc_df))

    # ── Strict Assertions ──────────────────────────────────────────────────────
    log.info("Verifying row counts match source CSVs...")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Assert DDL Table row counts
    checks = [
        ("dim_fund", fund_df),
        ("fact_nav", nav_df),
        ("fact_transactions", trans_df),
        ("fact_performance", perf_df),
        ("fact_aum", aum_df),
        ("portfolio_holdings", ph_df),
        ("benchmark_indices", bi_df),
        ("monthly_sip_inflows", msi_df),
        ("category_inflows", ci_df),
        ("industry_folio_count", ifc_df)
    ]

    for tbl_name, src_df in checks:
        cursor.execute(f"SELECT COUNT(*) FROM `{tbl_name}`")
        db_cnt = cursor.fetchone()[0]
        assert db_cnt == len(src_df), f"Row count mismatch in table {tbl_name}: DB={db_cnt}, CSV={len(src_df)}"
        log.info("Assertion passed: %s matches source (%d rows)", tbl_name, db_cnt)

    conn.close()
    log.info("All 10 cleaned datasets loaded and verified against source CSVs successfully! OK")


def main():
    try:
        load_data()
    except Exception as e:
        log.error("Fatal loader error: %s", e)
        raise e


if __name__ == "__main__":
    main()

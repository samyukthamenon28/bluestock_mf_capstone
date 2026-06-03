"""
load_star_schema.py — Bluestock MF Capstone: Load Star Schema (D2)
Orchestrates table creation and populates the SQLite Star Schema database.
"""

import os
import logging
import sqlite3
from pathlib import Path
import pandas as pd
import numpy as np

# ── Paths ──────────────────────────────────────────────────────────────────────
ROOT = Path(__file__).resolve().parent.parent
PROC_DIR = ROOT / "data" / "processed"
RAW_DIR = ROOT / "data" / "raw"
DB_PATH = ROOT / "data" / "db" / "bluestock_mf.db"
SQL_DDL_PATH = ROOT / "sql" / "star_schema.sql"

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
    """Drop tables in correct order of dependency."""
    log.info("Dropping existing star schema tables to start fresh...")
    cursor = conn.cursor()
    # Drop facts first
    cursor.execute("DROP TABLE IF EXISTS fact_transactions;")
    cursor.execute("DROP TABLE IF EXISTS fact_nav_history;")
    # Drop dimensions
    cursor.execute("DROP TABLE IF EXISTS dim_investors;")
    cursor.execute("DROP TABLE IF EXISTS dim_schemes;")
    cursor.execute("DROP TABLE IF EXISTS dim_dates;")
    conn.commit()


def run_ddl(conn: sqlite3.Connection):
    """Execute the DDL script."""
    log.info("Executing DDL script from %s ...", SQL_DDL_PATH.name)
    with open(SQL_DDL_PATH, "r") as f:
        ddl_script = f.read()
    conn.executescript(ddl_script)
    conn.commit()


def load_dimensions(conn: sqlite3.Connection):
    """Populates dim_investors, dim_schemes, and dim_dates."""
    log.info("Loading Dimension tables...")

    # 1. Load dim_investors
    log.info("Populating dim_investors...")
    trans_clean = pd.read_csv(PROC_DIR / "investor_transactions_clean.csv")
    dim_investors = trans_clean[
        ["investor_id", "state", "city", "city_tier", "age_group", "gender", "annual_income_lakh"]
    ].drop_duplicates(subset=["investor_id"])
    
    dim_investors.to_sql("dim_investors", conn, if_exists="append", index=False)
    log.info("Loaded dim_investors: %d rows", len(dim_investors))

    # 2. Load dim_schemes (merging master + performance)
    log.info("Populating dim_schemes...")
    fm = pd.read_csv(RAW_DIR / "01_fund_master.csv")
    perf = pd.read_csv(PROC_DIR / "scheme_performance_clean.csv")
    
    # Strip spaces from columns if any overlap
    fm.columns = fm.columns.str.strip()
    perf.columns = perf.columns.str.strip()
    
    merged = pd.merge(fm, perf, on="amfi_code", suffixes=("_fm", "_perf"))
    
    # Map to schema fields
    dim_schemes_cols = {
        "amfi_code": merged["amfi_code"],
        "scheme_name": merged["scheme_name_fm"],
        "fund_house": merged["fund_house_fm"],
        "category": merged["category_fm"],
        "sub_category": merged["sub_category"],
        "plan": merged["plan_fm"],
        "launch_date": merged["launch_date"],
        "benchmark": merged["benchmark"],
        "expense_ratio_pct": merged["expense_ratio_pct_perf"],
        "exit_load_pct": merged["exit_load_pct"],
        "min_sip_amount": merged["min_sip_amount"],
        "min_lumpsum_amount": merged["min_lumpsum_amount"],
        "fund_manager": merged["fund_manager"],
        "sebi_category_code": merged["sebi_category_code"],
        "risk_grade": merged["risk_grade"],
        "morningstar_rating": merged["morningstar_rating"],
        "return_1yr_pct": merged["return_1yr_pct"],
        "return_3yr_pct": merged["return_3yr_pct"],
        "return_5yr_pct": merged["return_5yr_pct"],
        "benchmark_3yr_pct": merged["benchmark_3yr_pct"],
        "alpha": merged["alpha"],
        "beta": merged["beta"],
        "sharpe_ratio": merged["sharpe_ratio"],
        "sortino_ratio": merged["sortino_ratio"],
        "std_dev_ann_pct": merged["std_dev_ann_pct"],
        "max_drawdown_pct": merged["max_drawdown_pct"],
        "aum_crore": merged["aum_crore"]
    }
    dim_schemes_df = pd.DataFrame(dim_schemes_cols)
    dim_schemes_df.to_sql("dim_schemes", conn, if_exists="append", index=False)
    log.info("Loaded dim_schemes: %d rows", len(dim_schemes_df))

    # 3. Load dim_dates
    log.info("Populating dim_dates...")
    nav_clean = pd.read_csv(PROC_DIR / "nav_history_clean.csv")
    
    unique_dates = pd.concat([nav_clean["date"], trans_clean["transaction_date"]]).dropna().unique()
    dates_df = pd.DataFrame({"date_id": unique_dates})
    dates_df["date_id"] = pd.to_datetime(dates_df["date_id"])
    dates_df.sort_values("date_id", inplace=True)
    
    dates_df["day"] = dates_df["date_id"].dt.day
    dates_df["month"] = dates_df["date_id"].dt.month
    dates_df["year"] = dates_df["date_id"].dt.year
    dates_df["quarter"] = dates_df["date_id"].dt.quarter
    dates_df["day_of_week"] = dates_df["date_id"].dt.day_name()
    dates_df["is_weekend"] = dates_df["date_id"].dt.dayofweek.isin([5, 6]).astype(int)
    
    dates_df["date_id"] = dates_df["date_id"].dt.strftime("%Y-%m-%d")
    
    dates_df.to_sql("dim_dates", conn, if_exists="append", index=False)
    log.info("Loaded dim_dates: %d rows", len(dates_df))


def load_facts(conn: sqlite3.Connection):
    """Populates fact_transactions and fact_nav_history."""
    log.info("Loading Fact tables...")

    # 1. Load fact_transactions
    log.info("Populating fact_transactions...")
    trans_clean = pd.read_csv(PROC_DIR / "investor_transactions_clean.csv")
    fact_transactions = trans_clean[
        [
            "investor_id",
            "transaction_date",
            "amfi_code",
            "transaction_type",
            "amount_inr",
            "payment_mode",
            "kyc_status",
        ]
    ].rename(columns={"transaction_date": "transaction_date"})
    
    fact_transactions.to_sql("fact_transactions", conn, if_exists="append", index=False)
    log.info("Loaded fact_transactions: %d rows", len(fact_transactions))

    # 2. Load fact_nav_history
    log.info("Populating fact_nav_history...")
    nav_clean = pd.read_csv(PROC_DIR / "nav_history_clean.csv")
    fact_nav = nav_clean[["amfi_code", "date", "nav"]].rename(
        columns={"date": "nav_date", "nav": "nav_value"}
    )
    
    fact_nav.to_sql("fact_nav_history", conn, if_exists="append", index=False)
    log.info("Loaded fact_nav_history: %d rows", len(fact_nav))


def verify_integrity(conn: sqlite3.Connection):
    """Run verification checks on the loaded data."""
    log.info("Running referential integrity verification checks...")
    cursor = conn.cursor()

    # 1. Check for orphaned transactions (investors)
    cursor.execute("""
        SELECT COUNT(*) FROM fact_transactions t
        LEFT JOIN dim_investors i ON t.investor_id = i.investor_id
        WHERE i.investor_id IS NULL;
    """)
    orphaned_investors = cursor.fetchone()[0]
    if orphaned_investors > 0:
        raise ValueError(f"Integrity Violation: Found {orphaned_investors} transactions referencing invalid investor_id!")
        
    # 2. Check for orphaned transactions (schemes)
    cursor.execute("""
        SELECT COUNT(*) FROM fact_transactions t
        LEFT JOIN dim_schemes s ON t.amfi_code = s.amfi_code
        WHERE s.amfi_code IS NULL;
    """)
    orphaned_schemes_t = cursor.fetchone()[0]
    if orphaned_schemes_t > 0:
        raise ValueError(f"Integrity Violation: Found {orphaned_schemes_t} transactions referencing invalid amfi_code!")

    # 3. Check for orphaned transactions (dates)
    cursor.execute("""
        SELECT COUNT(*) FROM fact_transactions t
        LEFT JOIN dim_dates d ON t.transaction_date = d.date_id
        WHERE d.date_id IS NULL;
    """)
    orphaned_dates_t = cursor.fetchone()[0]
    if orphaned_dates_t > 0:
        raise ValueError(f"Integrity Violation: Found {orphaned_dates_t} transactions referencing invalid date_id!")

    # 4. Check for orphaned NAVs (schemes)
    cursor.execute("""
        SELECT COUNT(*) FROM fact_nav_history n
        LEFT JOIN dim_schemes s ON n.amfi_code = s.amfi_code
        WHERE s.amfi_code IS NULL;
    """)
    orphaned_schemes_n = cursor.fetchone()[0]
    if orphaned_schemes_n > 0:
        raise ValueError(f"Integrity Violation: Found {orphaned_schemes_n} NAV records referencing invalid amfi_code!")

    # 5. Check for orphaned NAVs (dates)
    cursor.execute("""
        SELECT COUNT(*) FROM fact_nav_history n
        LEFT JOIN dim_dates d ON n.nav_date = d.date_id
        WHERE d.date_id IS NULL;
    """)
    orphaned_dates_n = cursor.fetchone()[0]
    if orphaned_dates_n > 0:
        raise ValueError(f"Integrity Violation: Found {orphaned_dates_n} NAV records referencing invalid date_id!")

    log.info("Integrity checks passed successfully! No orphaned records found. OK")


def main():
    log.info("Connecting to SQLite database at %s ...", DB_PATH)
    conn = sqlite3.connect(DB_PATH)
    try:
        # Enable foreign key verification
        conn.execute("PRAGMA foreign_keys = ON;")
        
        # 1. Drop existing tables
        drop_existing_tables(conn)
        
        # 2. Run DDL DDL
        run_ddl(conn)
        
        # 3. Load Dimensions
        load_dimensions(conn)
        
        # 4. Load Facts
        load_facts(conn)
        
        # 5. Commit and verify
        conn.commit()
        verify_integrity(conn)
        
        log.info("Star Schema loading completed successfully. OK")
    except Exception as e:
        conn.rollback()
        log.error("Failed to load Star Schema database: %s", e)
        raise e
    finally:
        conn.close()


if __name__ == "__main__":
    main()

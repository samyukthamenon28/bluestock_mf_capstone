"""
clean_data.py — Bluestock MF Capstone: Data Cleaning (D2)
Cleans and standardizes raw CSVs: nav_history, investor_transactions, scheme_performance.
Outputs cleaned CSVs to data/processed/.
"""

import os
import logging
from pathlib import Path
import pandas as pd
import numpy as np

# ── Paths ──────────────────────────────────────────────────────────────────────
ROOT = Path(__file__).resolve().parent.parent
RAW_DIR = ROOT / "data" / "raw"
PROC_DIR = ROOT / "data" / "processed"

PROC_DIR.mkdir(parents=True, exist_ok=True)

# ── Logging ────────────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(ROOT / "etl_cleaning.log"),
    ],
)
log = logging.getLogger(__name__)


def clean_nav_history() -> pd.DataFrame:
    """
    Cleans nav_history:
    - Standardizes column names and data types.
    - Reindexes each scheme to a full calendar range and ffills NAV values.
    """
    raw_path = RAW_DIR / "02_nav_history.csv"
    log.info("Cleaning NAV history from %s ...", raw_path.name)
    
    df = pd.read_csv(raw_path)
    df.columns = df.columns.str.strip()
    
    # Strip string fields
    for col in df.select_dtypes(include=["object"]).columns:
        df[col] = df[col].astype(str).str.strip()
        
    df["amfi_code"] = df["amfi_code"].astype(int)
    df["date"] = pd.to_datetime(df["date"])
    df["nav"] = pd.to_numeric(df["nav"], errors="coerce")
    
    # Check for duplicates
    dups = df.duplicated(subset=["amfi_code", "date"]).sum()
    if dups > 0:
        log.warning("Found %d duplicate (amfi_code, date) rows. Dropping them.", dups)
        df.drop_duplicates(subset=["amfi_code", "date"], keep="last", inplace=True)
        
    # Reindex for each scheme code to cover weekends and holidays
    log.info("Reindexing NAV history to full calendar range and forward-filling...")
    reindexed_dfs = []
    for code, group in df.groupby("amfi_code"):
        group = group.set_index("date")
        full_range = pd.date_range(start=group.index.min(), end=group.index.max(), freq="D")
        group = group.reindex(full_range)
        group.index.name = "date"
        
        # Propagate amfi_code and ffill/bfill nav
        group["amfi_code"] = code
        group["nav"] = group["nav"].ffill().bfill()
        
        reindexed_dfs.append(group.reset_index())
        
    cleaned_df = pd.concat(reindexed_dfs, ignore_index=True)
    cleaned_df["date"] = cleaned_df["date"].dt.strftime("%Y-%m-%d")
    
    out_path = PROC_DIR / "nav_history_clean.csv"
    cleaned_df.to_csv(out_path, index=False)
    log.info("Cleaned NAV history saved -> %s | shape=%s", out_path.name, cleaned_df.shape)
    return cleaned_df


def clean_investor_transactions() -> pd.DataFrame:
    """
    Cleans investor_transactions:
    - Strips whitespace from columns and values.
    - Standardizes dates.
    - Converts numbers.
    """
    raw_path = RAW_DIR / "08_investor_transactions.csv"
    log.info("Cleaning investor transactions from %s ...", raw_path.name)
    
    df = pd.read_csv(raw_path)
    df.columns = df.columns.str.strip()
    
    # Strip string fields
    for col in df.select_dtypes(include=["object"]).columns:
        df[col] = df[col].astype(str).str.strip()
        
    # Standardize data types
    df["amfi_code"] = df["amfi_code"].astype(int)
    df["transaction_date"] = pd.to_datetime(df["transaction_date"]).dt.strftime("%Y-%m-%d")
    df["amount_inr"] = pd.to_numeric(df["amount_inr"], errors="coerce")
    df["annual_income_lakh"] = pd.to_numeric(df["annual_income_lakh"], errors="coerce")
    
    # Check for nulls/duplicates
    nulls = df.isnull().sum().sum()
    if nulls > 0:
        log.warning("Found %d null values after type conversions in transactions.", nulls)
        
    dups = df.duplicated().sum()
    if dups > 0:
        log.warning("Found %d duplicate rows in transactions. Dropping them.", dups)
        df.drop_duplicates(inplace=True)
        
    out_path = PROC_DIR / "investor_transactions_clean.csv"
    df.to_csv(out_path, index=False)
    log.info("Cleaned investor transactions saved -> %s | shape=%s", out_path.name, df.shape)
    return df


def clean_scheme_performance() -> pd.DataFrame:
    """
    Cleans scheme_performance:
    - Standardizes column names and types.
    - Ensures uniqueness of amfi_code.
    """
    raw_path = RAW_DIR / "07_scheme_performance.csv"
    log.info("Cleaning scheme performance from %s ...", raw_path.name)
    
    df = pd.read_csv(raw_path)
    df.columns = df.columns.str.strip()
    
    # Strip string fields
    for col in df.select_dtypes(include=["object"]).columns:
        df[col] = df[col].astype(str).str.strip()
        
    # Standardize data types
    df["amfi_code"] = df["amfi_code"].astype(int)
    
    # Check for duplicate amfi_code
    dups = df["amfi_code"].duplicated().sum()
    if dups > 0:
        log.warning("Found %d duplicate amfi_code in scheme performance. Dropping duplicates.", dups)
        df.drop_duplicates(subset=["amfi_code"], keep="first", inplace=True)
        
    out_path = PROC_DIR / "scheme_performance_clean.csv"
    df.to_csv(out_path, index=False)
    log.info("Cleaned scheme performance saved -> %s | shape=%s", out_path.name, df.shape)
    return df


def main():
    log.info("Starting Day 2 Data Cleaning Task...")
    clean_nav_history()
    clean_investor_transactions()
    clean_scheme_performance()
    log.info("All data cleaning tasks completed successfully. OK")


if __name__ == "__main__":
    main()

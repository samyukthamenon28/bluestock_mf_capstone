"""
clean_data.py — Bluestock MF Capstone: Advanced Data Cleaning (D2)
Cleans and standardizes all 10 raw CSVs and outputs them to data/processed/.
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


def clean_string_df(df: pd.DataFrame) -> pd.DataFrame:
    """Strips whitespace from columns and object fields."""
    df.columns = df.columns.str.strip()
    for col in df.select_dtypes(include=["object"]).columns:
        df[col] = df[col].astype(str).str.strip()
    return df


def clean_01_fund_master() -> pd.DataFrame:
    log.info("Cleaning 01_fund_master.csv ...")
    df = pd.read_csv(RAW_DIR / "01_fund_master.csv")
    df = clean_string_df(df)
    
    # Types
    df["amfi_code"] = df["amfi_code"].astype(int)
    df["expense_ratio_pct"] = pd.to_numeric(df["expense_ratio_pct"], errors="coerce")
    df["exit_load_pct"] = pd.to_numeric(df["exit_load_pct"], errors="coerce")
    df["min_sip_amount"] = pd.to_numeric(df["min_sip_amount"], errors="coerce")
    df["min_lumpsum_amount"] = pd.to_numeric(df["min_lumpsum_amount"], errors="coerce")
    df["launch_date"] = pd.to_datetime(df["launch_date"]).dt.strftime("%Y-%m-%d")
    
    df.to_csv(PROC_DIR / "fund_master_clean.csv", index=False)
    log.info("Saved fund_master_clean.csv | shape=%s", df.shape)
    return df


def clean_02_nav_history() -> pd.DataFrame:
    log.info("Cleaning 02_nav_history.csv ...")
    df = pd.read_csv(RAW_DIR / "02_nav_history.csv")
    df = clean_string_df(df)
    
    df["amfi_code"] = df["amfi_code"].astype(int)
    df["date"] = pd.to_datetime(df["date"])
    df["nav"] = pd.to_numeric(df["nav"], errors="coerce")
    
    # Validation: NAV > 0
    invalid_nav = df[df["nav"] <= 0]
    if not invalid_nav.empty:
        log.warning("Found %d rows with NAV <= 0! Removing them.", len(invalid_nav))
        df = df[df["nav"] > 0]
        
    # Sort by amfi_code + date
    df.sort_values(["amfi_code", "date"], inplace=True)
    
    # Remove duplicates
    dups = df.duplicated(subset=["amfi_code", "date"]).sum()
    if dups > 0:
        log.warning("Found %d duplicate (amfi_code, date) rows. Dropping them.", dups)
        df.drop_duplicates(subset=["amfi_code", "date"], keep="last", inplace=True)
        
    # Reindex to full calendar range and forward-fill NAV
    reindexed_dfs = []
    for code, group in df.groupby("amfi_code"):
        group = group.set_index("date")
        full_range = pd.date_range(start=group.index.min(), end=group.index.max(), freq="D")
        group = group.reindex(full_range)
        group.index.name = "date"
        group["amfi_code"] = code
        group["nav"] = group["nav"].ffill().bfill()
        reindexed_dfs.append(group.reset_index())
        
    cleaned_df = pd.concat(reindexed_dfs, ignore_index=True)
    cleaned_df["date"] = cleaned_df["date"].dt.strftime("%Y-%m-%d")
    
    cleaned_df.to_csv(PROC_DIR / "nav_history_clean.csv", index=False)
    log.info("Saved nav_history_clean.csv | shape=%s", cleaned_df.shape)
    return cleaned_df


def clean_03_aum_by_fund_house() -> pd.DataFrame:
    log.info("Cleaning 03_aum_by_fund_house.csv ...")
    df = pd.read_csv(RAW_DIR / "03_aum_by_fund_house.csv")
    df = clean_string_df(df)
    
    df["date"] = pd.to_datetime(df["date"]).dt.strftime("%Y-%m-%d")
    df["aum_lakh_crore"] = pd.to_numeric(df["aum_lakh_crore"], errors="coerce")
    df["aum_crore"] = pd.to_numeric(df["aum_crore"], errors="coerce")
    df["num_schemes"] = pd.to_numeric(df["num_schemes"], errors="coerce").astype(int)
    
    df.to_csv(PROC_DIR / "aum_by_fund_house_clean.csv", index=False)
    log.info("Saved aum_by_fund_house_clean.csv | shape=%s", df.shape)
    return df


def clean_04_monthly_sip_inflows() -> pd.DataFrame:
    log.info("Cleaning 04_monthly_sip_inflows.csv ...")
    df = pd.read_csv(RAW_DIR / "04_monthly_sip_inflows.csv")
    df = clean_string_df(df)
    
    df["month"] = pd.to_datetime(df["month"], format="%Y-%m").dt.strftime("%Y-%m")
    df["sip_inflow_crore"] = pd.to_numeric(df["sip_inflow_crore"], errors="coerce")
    df["active_sip_accounts_crore"] = pd.to_numeric(df["active_sip_accounts_crore"], errors="coerce")
    df["new_sip_accounts_lakh"] = pd.to_numeric(df["new_sip_accounts_lakh"], errors="coerce")
    df["sip_aum_lakh_crore"] = pd.to_numeric(df["sip_aum_lakh_crore"], errors="coerce")
    df["yoy_growth_pct"] = pd.to_numeric(df["yoy_growth_pct"], errors="coerce")
    
    df.to_csv(PROC_DIR / "monthly_sip_inflows_clean.csv", index=False)
    log.info("Saved monthly_sip_inflows_clean.csv | shape=%s", df.shape)
    return df


def clean_05_category_inflows() -> pd.DataFrame:
    log.info("Cleaning 05_category_inflows.csv ...")
    df = pd.read_csv(RAW_DIR / "05_category_inflows.csv")
    df = clean_string_df(df)
    
    df["month"] = pd.to_datetime(df["month"], format="%Y-%m").dt.strftime("%Y-%m")
    df["net_inflow_crore"] = pd.to_numeric(df["net_inflow_crore"], errors="coerce")
    
    df.to_csv(PROC_DIR / "category_inflows_clean.csv", index=False)
    log.info("Saved category_inflows_clean.csv | shape=%s", df.shape)
    return df


def clean_06_industry_folio_count() -> pd.DataFrame:
    log.info("Cleaning 06_industry_folio_count.csv ...")
    df = pd.read_csv(RAW_DIR / "06_industry_folio_count.csv")
    df = clean_string_df(df)
    
    df["month"] = pd.to_datetime(df["month"], format="%Y-%m").dt.strftime("%Y-%m")
    for col in df.columns:
        if col != "month":
            df[col] = pd.to_numeric(df[col], errors="coerce")
            
    df.to_csv(PROC_DIR / "industry_folio_count_clean.csv", index=False)
    log.info("Saved industry_folio_count_clean.csv | shape=%s", df.shape)
    return df


def clean_07_scheme_performance() -> pd.DataFrame:
    log.info("Cleaning 07_scheme_performance.csv ...")
    df = pd.read_csv(RAW_DIR / "07_scheme_performance.csv")
    df = clean_string_df(df)
    
    df["amfi_code"] = df["amfi_code"].astype(int)
    
    # Validate returns are numeric and flag anomalies
    return_cols = ["return_1yr_pct", "return_3yr_pct", "return_5yr_pct", "benchmark_3yr_pct"]
    for col in return_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")
        # Check for missing values or extreme anomalies (e.g. returns > 100% or < -50%)
        anoms = df[(df[col] > 100) | (df[col] < -50)]
        if not anoms.empty:
            log.warning("Anomaly: Scheme performance returns out of bounds in %s: %s", col, anoms[["amfi_code", col]].to_dict())
            
    # Check expense_ratio range (0.1% – 2.5%)
    df["expense_ratio_pct"] = pd.to_numeric(df["expense_ratio_pct"], errors="coerce")
    out_of_range_expense = df[(df["expense_ratio_pct"] < 0.1) | (df["expense_ratio_pct"] > 2.5)]
    if not out_of_range_expense.empty:
        log.warning("Anomaly: Expense ratio out of range (0.1% - 2.5%)! Count: %d", len(out_of_range_expense))
        log.warning("Out of range: %s", out_of_range_expense[["amfi_code", "expense_ratio_pct"]].to_dict())
        
    # Map other numeric columns
    for col in ["alpha", "beta", "sharpe_ratio", "sortino_ratio", "std_dev_ann_pct", "max_drawdown_pct", "aum_crore", "morningstar_rating"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")
        
    df.to_csv(PROC_DIR / "scheme_performance_clean.csv", index=False)
    log.info("Saved scheme_performance_clean.csv | shape=%s", df.shape)
    return df


def clean_08_investor_transactions() -> pd.DataFrame:
    log.info("Cleaning 08_investor_transactions.csv ...")
    df = pd.read_csv(RAW_DIR / "08_investor_transactions.csv")
    df = clean_string_df(df)
    
    df["amfi_code"] = df["amfi_code"].astype(int)
    
    # Fix date formats
    df["transaction_date"] = pd.to_datetime(df["transaction_date"]).dt.strftime("%Y-%m-%d")
    
    # Standardise transaction_type (SIP/Lumpsum/Redemption)
    # Check current types
    log.info("Transaction types before standardization: %s", df["transaction_type"].unique().tolist())
    df["transaction_type"] = df["transaction_type"].str.replace("sip", "SIP", case=False)
    df["transaction_type"] = df["transaction_type"].str.replace("lumpsum", "Lumpsum", case=False)
    df["transaction_type"] = df["transaction_type"].str.replace("redemption", "Redemption", case=False)
    
    # Validate amount > 0
    df["amount_inr"] = pd.to_numeric(df["amount_inr"], errors="coerce")
    invalid_amt = df[df["amount_inr"] <= 0]
    if not invalid_amt.empty:
        log.warning("Found %d rows with amount_inr <= 0! Removing them.", len(invalid_amt))
        df = df[df["amount_inr"] > 0]
        
    # Check KYC status enum values
    log.info("KYC status unique values: %s", df["kyc_status"].unique().tolist())
    # Standardize enum (Pending/Verified)
    df["kyc_status"] = df["kyc_status"].str.capitalize()
    
    df["annual_income_lakh"] = pd.to_numeric(df["annual_income_lakh"], errors="coerce")
    
    df.to_csv(PROC_DIR / "investor_transactions_clean.csv", index=False)
    log.info("Saved investor_transactions_clean.csv | shape=%s", df.shape)
    return df


def clean_09_portfolio_holdings() -> pd.DataFrame:
    log.info("Cleaning 09_portfolio_holdings.csv ...")
    df = pd.read_csv(RAW_DIR / "09_portfolio_holdings.csv")
    df = clean_string_df(df)
    
    df["amfi_code"] = df["amfi_code"].astype(int)
    df["weight_pct"] = pd.to_numeric(df["weight_pct"], errors="coerce")
    df["market_value_cr"] = pd.to_numeric(df["market_value_cr"], errors="coerce")
    df["current_price_inr"] = pd.to_numeric(df["current_price_inr"], errors="coerce")
    df["portfolio_date"] = pd.to_datetime(df["portfolio_date"]).dt.strftime("%Y-%m-%d")
    
    df.to_csv(PROC_DIR / "portfolio_holdings_clean.csv", index=False)
    log.info("Saved portfolio_holdings_clean.csv | shape=%s", df.shape)
    return df


def clean_10_benchmark_indices() -> pd.DataFrame:
    log.info("Cleaning 10_benchmark_indices ...")
    # File has space in name
    df = pd.read_csv(RAW_DIR / "10_benchmark_indices - 10_benchmark_indices.csv")
    df = clean_string_df(df)
    
    df["date"] = pd.to_datetime(df["date"]).dt.strftime("%Y-%m-%d")
    df["close_value"] = pd.to_numeric(df["close_value"], errors="coerce")
    
    df.sort_values(["index_name", "date"], inplace=True)
    
    df.to_csv(PROC_DIR / "benchmark_indices_clean.csv", index=False)
    log.info("Saved benchmark_indices_clean.csv | shape=%s", df.shape)
    return df


def main():
    log.info("Starting Detailed Data Cleaning for all 10 CSVs...")
    clean_01_fund_master()
    clean_02_nav_history()
    clean_03_aum_by_fund_house()
    clean_04_monthly_sip_inflows()
    clean_05_category_inflows()
    clean_06_industry_folio_count()
    clean_07_scheme_performance()
    clean_08_investor_transactions()
    clean_09_portfolio_holdings()
    clean_10_benchmark_indices()
    log.info("All 10 CSV data cleaning tasks completed successfully. OK")


if __name__ == "__main__":
    main()

"""
etl_pipeline.py — Bluestock MF Capstone: Full ETL Pipeline (D1)
Runs without manual steps. Handles errors gracefully.
"""

import os
import json
import time
import logging
from pathlib import Path

import pandas as pd
import requests
from sqlalchemy import create_engine, text

# ── Paths ──────────────────────────────────────────────────────────────────────
ROOT       = Path(__file__).resolve().parent.parent
RAW_DIR    = ROOT / "data" / "raw"
PROC_DIR   = ROOT / "data" / "processed"
DB_DIR     = ROOT / "data" / "db"
SQL_DIR    = ROOT / "sql"

for d in [RAW_DIR, PROC_DIR, DB_DIR, SQL_DIR]:
    d.mkdir(parents=True, exist_ok=True)

DB_PATH = DB_DIR / "bluestock_mf.db"

# ── Logging ────────────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(ROOT / "etl.log"),
    ],
)
log = logging.getLogger(__name__)

# ── Constants ──────────────────────────────────────────────────────────────────
MFAPI_BASE = "https://api.mfapi.in/mf"

KEY_SCHEMES = {
    "HDFC_Top100_Direct":    125497,
    "SBI_Bluechip":          119551,
    "ICICI_Bluechip":        120503,
    "Nippon_LargeCap":       118632,
    "Axis_Bluechip":         119092,
    "Kotak_Bluechip":        120841,
}

# ── Helpers ────────────────────────────────────────────────────────────────────

def fetch_mfapi(scheme_code: int, retries: int = 3, backoff: float = 2.0) -> dict:
    """Fetch NAV history from mfapi.in with retry logic."""
    url = f"{MFAPI_BASE}/{scheme_code}"
    for attempt in range(1, retries + 1):
        try:
            resp = requests.get(url, timeout=15)
            resp.raise_for_status()
            return resp.json()
        except requests.RequestException as exc:
            log.warning("Attempt %d/%d failed for scheme %d: %s", attempt, retries, scheme_code, exc)
            if attempt < retries:
                time.sleep(backoff * attempt)
    raise RuntimeError(f"All {retries} attempts failed for scheme {scheme_code}")


def parse_nav_response(data: dict, scheme_code: int) -> pd.DataFrame:
    """Convert mfapi JSON → clean DataFrame."""
    meta = data.get("meta", {})
    records = data.get("data", [])

    df = pd.DataFrame(records)                        # columns: date, nav
    df.rename(columns={"date": "nav_date", "nav": "nav_value"}, inplace=True)
    df["nav_date"]   = pd.to_datetime(df["nav_date"], format="%d-%m-%Y")
    df["nav_value"]  = pd.to_numeric(df["nav_value"], errors="coerce")
    df["scheme_code"]       = scheme_code
    df["scheme_name"]       = meta.get("scheme_name", "")
    df["scheme_category"]   = meta.get("scheme_category", "")
    df["scheme_type"]       = meta.get("scheme_type", "")
    df["fund_house"]        = meta.get("fund_house", "")
    df.sort_values("nav_date", inplace=True)
    df.reset_index(drop=True, inplace=True)
    return df


def fill_missing_trading_days(df: pd.DataFrame) -> pd.DataFrame:
    """Reindex to full calendar range and forward-fill NAV for weekends/holidays."""
    df = df.set_index("nav_date")
    full_range = pd.date_range(df.index.min(), df.index.max(), freq="D")
    df = df.reindex(full_range)
    df.index.name = "nav_date"
    # Forward-fill NAV; back-fill the very first rows if needed
    df["nav_value"] = df["nav_value"].ffill().bfill()
    # Propagate scalar columns
    for col in ["scheme_code", "scheme_name", "scheme_category", "scheme_type", "fund_house"]:
        if col in df.columns:
            df[col] = df[col].ffill().bfill()
    return df.reset_index()


def load_csv_datasets(raw_dir: Path) -> dict[str, pd.DataFrame]:
    """
    Load all CSV files in raw/ directory.
    Prints shape, dtypes, head, and anomalies for each.
    """
    datasets: dict[str, pd.DataFrame] = {}
    csv_files = sorted(raw_dir.glob("*.csv"))

    if not csv_files:
        log.warning("No CSV files found in %s — skipping local dataset load.", raw_dir)
        return datasets

    for fpath in csv_files:
        name = fpath.stem
        try:
            df = pd.read_csv(fpath, low_memory=False)
            datasets[name] = df
            log.info("Loaded %-35s | shape=%s", name, df.shape)
            print(f"\n{'='*60}")
            print(f"Dataset : {name}")
            print(f"Shape   : {df.shape}")
            print(f"Dtypes  :\n{df.dtypes}")
            print(f"Head    :\n{df.head(3)}")

            # Anomaly checks
            null_pct = df.isnull().mean().mul(100).round(2)
            high_null = null_pct[null_pct > 20]
            if not high_null.empty:
                log.warning("High nulls in '%s': %s", name, high_null.to_dict())
            dups = df.duplicated().sum()
            if dups:
                log.warning("Duplicate rows in '%s': %d", name, dups)

        except Exception as exc:
            log.error("Failed to load %s: %s", fpath.name, exc)

    return datasets


# ── Stage 1: Fetch live NAV ────────────────────────────────────────────────────

def stage_fetch_live_nav() -> dict[str, pd.DataFrame]:
    """Fetch NAV for all KEY_SCHEMES and save raw JSON + CSV."""
    all_dfs: dict[str, pd.DataFrame] = {}

    for label, code in KEY_SCHEMES.items():
        log.info("Fetching NAV for %s (code=%d) …", label, code)
        try:
            raw_data = fetch_mfapi(code)

            # Save raw JSON
            json_path = RAW_DIR / f"nav_{label}_{code}.json"
            with open(json_path, "w") as fh:
                json.dump(raw_data, fh, indent=2)
            log.info("Saved raw JSON → %s", json_path.name)

            df = parse_nav_response(raw_data, code)
            df = fill_missing_trading_days(df)

            csv_path = RAW_DIR / f"nav_{label}_{code}.csv"
            df.to_csv(csv_path, index=False)
            log.info("Saved raw CSV  → %s  | rows=%d", csv_path.name, len(df))

            all_dfs[label] = df

        except Exception as exc:
            log.error("Could not fetch %s: %s", label, exc)

    return all_dfs


# ── Stage 2: Merge & process ───────────────────────────────────────────────────

def stage_merge_nav(all_dfs: dict[str, pd.DataFrame]) -> pd.DataFrame:
    """Concatenate all scheme NAV DataFrames into one master table."""
    if not all_dfs:
        log.warning("No NAV data to merge.")
        return pd.DataFrame()

    master = pd.concat(all_dfs.values(), ignore_index=True)
    master.sort_values(["scheme_code", "nav_date"], inplace=True)
    master.drop_duplicates(subset=["scheme_code", "nav_date"], keep="last", inplace=True)
    master.reset_index(drop=True, inplace=True)

    out = PROC_DIR / "nav_master.csv"
    master.to_csv(out, index=False)
    log.info("Merged NAV master → %s | rows=%d", out.name, len(master))
    return master


# ── Stage 3: Load SQLite ───────────────────────────────────────────────────────

def stage_load_sqlite(
    nav_master: pd.DataFrame,
    local_datasets: dict[str, pd.DataFrame],
) -> None:
    """Load all DataFrames into SQLite and run smoke-test queries."""
    engine = create_engine(f"sqlite:///{DB_PATH}")

    # Nav history
    if not nav_master.empty:
        nav_master.to_sql("nav_history", engine, if_exists="replace", index=False)
        log.info("Loaded nav_history → %d rows", len(nav_master))

    # Local CSVs (fund_master, etc.)
    for name, df in local_datasets.items():
        table = name.lower().replace("-", "_").replace(" ", "_")
        df.to_sql(table, engine, if_exists="replace", index=False)
        log.info("Loaded %-30s → %d rows", table, len(df))

    # Smoke-test queries
    smoke_queries = [
        ("Row count nav_history",
         "SELECT COUNT(*) AS cnt FROM nav_history"),
        ("Distinct schemes",
         "SELECT COUNT(DISTINCT scheme_code) AS n FROM nav_history"),
        ("Latest NAV per scheme",
         """SELECT scheme_code, scheme_name, MAX(nav_date) AS latest_date,
                   ROUND(MAX(CASE WHEN nav_date = (SELECT MAX(nav_date) FROM nav_history nh2
                             WHERE nh2.scheme_code = nav_history.scheme_code)
                             THEN nav_value END), 4) AS latest_nav
            FROM nav_history
            GROUP BY scheme_code"""),
    ]

    with engine.connect() as conn:
        for title, sql in smoke_queries:
            try:
                result = pd.read_sql(text(sql), conn)
                log.info("Query — %s:\n%s", title, result.to_string(index=False))
            except Exception as exc:
                log.warning("Smoke-test query failed (%s): %s", title, exc)

    log.info("SQLite database ready → %s", DB_PATH)


# ── Stage 4: Data quality summary ─────────────────────────────────────────────

def stage_data_quality(
    nav_master: pd.DataFrame,
    local_datasets: dict[str, pd.DataFrame],
) -> None:
    """Write a data-quality summary to processed/data_quality_report.txt."""
    lines = ["DATA QUALITY REPORT — Bluestock MF Capstone", "=" * 60, ""]

    if not nav_master.empty:
        lines.append(f"NAV Master — {len(nav_master):,} rows, {nav_master['scheme_code'].nunique()} schemes")
        null_nav = nav_master["nav_value"].isnull().sum()
        lines.append(f"  Null nav_value  : {null_nav}")
        lines.append(f"  Date range      : {nav_master['nav_date'].min().date()} → {nav_master['nav_date'].max().date()}")
        lines.append("")

    for name, df in local_datasets.items():
        lines.append(f"{name}")
        lines.append(f"  Shape           : {df.shape}")
        null_pct = df.isnull().mean().mul(100).round(2)
        problem_cols = null_pct[null_pct > 0]
        if not problem_cols.empty:
            lines.append(f"  Columns w/ nulls: {problem_cols.to_dict()}")
        dups = df.duplicated().sum()
        lines.append(f"  Duplicate rows  : {dups}")
        lines.append("")

    report_path = PROC_DIR / "data_quality_report.txt"
    report_path.write_text("\n".join(lines))
    log.info("Data quality report → %s", report_path.name)


# ── Main ───────────────────────────────────────────────────────────────────────

def main() -> None:
    log.info("=" * 60)
    log.info("Bluestock MF ETL Pipeline — Day 1")
    log.info("=" * 60)

    # 1. Load any local CSV datasets the team placed in data/raw/
    local_datasets = load_csv_datasets(RAW_DIR)

    # 2. Fetch live NAV for key schemes
    all_nav_dfs = stage_fetch_live_nav()

    # 3. Merge into master
    nav_master = stage_merge_nav(all_nav_dfs)

    # 4. Load into SQLite
    stage_load_sqlite(nav_master, local_datasets)

    # 5. Data quality summary
    stage_data_quality(nav_master, local_datasets)

    log.info("ETL pipeline complete. ✓")


if __name__ == "__main__":
    main()

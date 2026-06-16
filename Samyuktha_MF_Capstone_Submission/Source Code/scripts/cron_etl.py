"""
cron_etl.py — Bluestock MF Capstone: Auto-fetch daily NAV and update database (B1)
Fetches the latest NAV from mfapi.in for all 40 schemes in the database.
If new records are found, they are appended to the SQLite star schema, and performance analytics are updated.
"""

import os
import sys
import time
import logging
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
import pandas as pd
import requests

# ── Paths ──────────────────────────────────────────────────────────────────────
ROOT = Path(__file__).resolve().parent.parent
DB_PATH = ROOT / "data" / "db" / "bluestock_mf.db"
LOG_PATH = ROOT / "cron_etl.log"

# ── Logging ────────────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(LOG_PATH),
    ],
)
log = logging.getLogger(__name__)

MFAPI_BASE = "https://api.mfapi.in/mf"


def fetch_latest_nav(scheme_code: int, retries: int = 3) -> dict | None:
    """Fetch from /mf/{code} and return only the most-recent NAV record."""
    url = f"{MFAPI_BASE}/{scheme_code}"
    for attempt in range(1, retries + 1):
        try:
            resp = requests.get(url, timeout=15)
            resp.raise_for_status()
            data = resp.json()
            records = data.get("data", [])
            if not records:
                log.warning("Empty NAV data for scheme %d", scheme_code)
                return None
            latest = records[0]          # mfapi returns newest first
            return {
                "scheme_code": scheme_code,
                "nav_date": latest["date"],  # Format is DD-MM-YYYY
                "nav_value": float(latest["nav"]),
            }
        except (requests.RequestException, KeyError, ValueError) as exc:
            log.warning("Attempt %d/%d failed for %d: %s", attempt, retries, scheme_code, exc)
            if attempt < retries:
                time.sleep(1.5 * attempt)
    return None


def get_all_schemes() -> list[tuple[int, str]]:
    """Fetch all 40 schemes from the dim_fund table."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT amfi_code, scheme_name FROM dim_fund")
    schemes = cursor.fetchall()
    conn.close()
    return schemes


def check_date_exists(conn: sqlite3.Connection, date_str: str) -> bool:
    """Check if the given date exists in dim_date."""
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM dim_date WHERE date_id = ?", (date_str,))
    return cursor.fetchone() is not None


def insert_date(conn: sqlite3.Connection, date_str: str):
    """Insert a new date record into dim_date."""
    dt = datetime.strptime(date_str, "%Y-%m-%d")
    day = dt.day
    month = dt.month
    year = dt.year
    quarter = (dt.month - 1) // 3 + 1
    day_of_week = dt.strftime("%A")
    is_weekend = 1 if dt.weekday() in (5, 6) else 0

    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO dim_date (date_id, day, month, year, quarter, day_of_week, is_weekend)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (date_str, day, month, year, quarter, day_of_week, is_weekend))
    conn.commit()
    log.info("Inserted new date into dim_date: %s", date_str)


def check_nav_exists(conn: sqlite3.Connection, amfi_code: int, date_str: str) -> bool:
    """Check if NAV record already exists for the given fund and date."""
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM fact_nav WHERE amfi_code = ? AND nav_date = ?", (amfi_code, date_str))
    return cursor.fetchone() is not None


def insert_nav(conn: sqlite3.Connection, amfi_code: int, date_str: str, nav_value: float):
    """Insert a new NAV value into fact_nav."""
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO fact_nav (amfi_code, nav_date, nav_value)
        VALUES (?, ?, ?)
    """, (amfi_code, date_str, nav_value))
    conn.commit()


def main():
    log.info("=" * 60)
    log.info("Cron ETL Job: Starting live NAV update...")
    log.info("=" * 60)

    if not DB_PATH.exists():
        log.error("SQLite database does not exist at %s. Run Day 2 ingestion first.", DB_PATH)
        sys.exit(1)

    schemes = get_all_schemes()
    log.info("Loaded %d schemes from database dim_fund table.", len(schemes))

    conn = sqlite3.connect(DB_PATH)
    updates_count = 0

    for idx, (code, name) in enumerate(schemes, 1):
        log.info("[%d/%d] Fetching %d (%s)...", idx, len(schemes), code, name[:40])
        record = fetch_latest_nav(code)
        
        if record:
            # Parse mfapi date (DD-MM-YYYY) to database format (YYYY-MM-DD)
            try:
                date_parsed = datetime.strptime(record["nav_date"], "%d-%m-%Y")
                date_str = date_parsed.strftime("%Y-%m-%d")
                nav_val = record["nav_value"]
                
                # Check if it already exists in fact_nav
                if check_nav_exists(conn, code, date_str):
                    log.info("  NAV already exists for date %s. Skipping.", date_str)
                else:
                    # Ensure date exists in dim_date
                    if not check_date_exists(conn, date_str):
                        insert_date(conn, date_str)
                    
                    insert_nav(conn, code, date_str, nav_val)
                    log.info("  [OK] Successfully inserted new NAV: %s -> %.4f", date_str, nav_val)
                    updates_count += 1
            except Exception as exc:
                log.error("  Error processing NAV record for scheme %d: %s", code, exc)
        else:
            log.warning("  Failed to fetch NAV for scheme %d.", code)
        
        # Polite rate limiting
        time.sleep(0.1)

    conn.close()
    log.info("Live NAV update completed. Inserted %d new NAV records.", updates_count)

    # If new data was loaded, trigger the performance analytics update to regenerate files
    if updates_count > 0:
        log.info("New data updated in database! Triggering performance analytics update...")
        try:
            # Add scripts directory to path to import generate_analytics
            sys.path.append(str(ROOT / "scripts"))
            import generate_analytics
            
            # Recalculate scorecard and recreate notebook
            generate_analytics.compute_analytics()
            generate_analytics.create_analytics_notebook()
            log.info("Performance analytics updated successfully.")
        except Exception as exc:
            log.error("Failed to automatically update performance analytics: %s", exc)
    else:
        log.info("No database changes detected. Recalculation skipped.")

    log.info("Cron ETL Job completed successfully. OK")


if __name__ == "__main__":
    main()

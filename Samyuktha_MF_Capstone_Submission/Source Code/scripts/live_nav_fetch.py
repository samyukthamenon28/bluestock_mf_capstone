"""
live_nav_fetch.py — Fetch current NAV from mfapi.in and append to raw CSVs.
Designed to be run standalone or as a cron job (B1).

Cron entry (weekdays 8 PM IST):
    0 14 * * 1-5  /usr/bin/python3 /path/to/scripts/live_nav_fetch.py >> /path/to/etl.log 2>&1
"""

import json
import logging
import time
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
import requests

# ── Paths ──────────────────────────────────────────────────────────────────────
ROOT    = Path(__file__).resolve().parent.parent
RAW_DIR = ROOT / "data" / "raw"
RAW_DIR.mkdir(parents=True, exist_ok=True)

# ── Logging ────────────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(ROOT / "live_nav.log"),
    ],
)
log = logging.getLogger(__name__)

# ── Scheme registry ────────────────────────────────────────────────────────────
SCHEMES = {
    125497: "HDFC_Top100_Direct",
    119551: "SBI_Bluechip",
    120503: "ICICI_Bluechip",
    118632: "Nippon_LargeCap",
    119092: "Axis_Bluechip",
    120841: "Kotak_Bluechip",
}

MFAPI_BASE = "https://api.mfapi.in/mf"


# ── Core fetch ─────────────────────────────────────────────────────────────────

def fetch_latest_nav(scheme_code: int, retries: int = 3) -> dict | None:
    """
    Fetch from /mf/{code} and return only the most-recent NAV record.
    Returns None on failure.
    """
    url = f"{MFAPI_BASE}/{scheme_code}"
    for attempt in range(1, retries + 1):
        try:
            resp = requests.get(url, timeout=15)
            resp.raise_for_status()
            data = resp.json()
            records = data.get("data", [])
            if not records:
                log.warning("Empty data for scheme %d", scheme_code)
                return None
            latest = records[0]          # mfapi returns newest first
            meta   = data.get("meta", {})
            return {
                "scheme_code":     scheme_code,
                "scheme_name":     meta.get("scheme_name", ""),
                "fund_house":      meta.get("fund_house", ""),
                "scheme_category": meta.get("scheme_category", ""),
                "nav_date":        latest["date"],
                "nav_value":       float(latest["nav"]),
                "fetched_at":      datetime.now(timezone.utc).isoformat(),
            }
        except (requests.RequestException, KeyError, ValueError) as exc:
            log.warning("Attempt %d/%d failed for %d: %s", attempt, retries, scheme_code, exc)
            if attempt < retries:
                time.sleep(2 * attempt)
    return None


def append_to_csv(record: dict, scheme_label: str, scheme_code: int) -> None:
    """Append a single NAV record to the scheme's raw CSV (avoid duplicates)."""
    csv_path = RAW_DIR / f"nav_{scheme_label}_{scheme_code}.csv"

    row_df = pd.DataFrame([record])
    row_df["nav_date"] = pd.to_datetime(row_df["nav_date"], format="%d-%m-%Y")

    if csv_path.exists():
        existing = pd.read_csv(csv_path, parse_dates=["nav_date"])
        if pd.to_datetime(record["nav_date"], format="%d-%m-%Y") in existing["nav_date"].values:
            log.info("NAV already present for %s on %s — skipping.", scheme_label, record["nav_date"])
            return
        combined = pd.concat([existing, row_df], ignore_index=True)
        combined.sort_values("nav_date", inplace=True)
        combined.drop_duplicates(subset=["nav_date"], keep="last", inplace=True)
        combined.to_csv(csv_path, index=False)
    else:
        row_df.to_csv(csv_path, index=False)

    log.info("Appended NAV for %s: date=%s  nav=%.4f", scheme_label, record["nav_date"], record["nav_value"])


def save_snapshot_json(records: list[dict]) -> None:
    """Save today's full snapshot as a timestamped JSON for audit trail."""
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    out = RAW_DIR / f"nav_snapshot_{ts}.json"
    with open(out, "w") as fh:
        json.dump(records, fh, indent=2, default=str)
    log.info("Snapshot saved → %s", out.name)


# ── Main ───────────────────────────────────────────────────────────────────────

def main() -> None:
    log.info("Live NAV fetch started — %s", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    collected = []
    for code, label in SCHEMES.items():
        record = fetch_latest_nav(code)
        if record:
            append_to_csv(record, label, code)
            collected.append(record)
            log.info("✓  %-30s | NAV = %.4f  | Date = %s", label, record["nav_value"], record["nav_date"])
        else:
            log.error("✗  Failed to fetch %s (%d)", label, code)
        time.sleep(0.5)   # polite rate limiting

    if collected:
        save_snapshot_json(collected)

    log.info("Live NAV fetch complete — %d/%d schemes fetched.", len(collected), len(SCHEMES))

    # Print summary table
    if collected:
        df = pd.DataFrame(collected)[["scheme_name", "nav_date", "nav_value", "fund_house"]]
        print("\n" + df.to_string(index=False))


if __name__ == "__main__":
    main()

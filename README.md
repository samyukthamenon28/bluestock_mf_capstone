# Bluestock MF Capstone

Mutual Fund analytics capstone project — ETL, EDA, performance metrics, and dashboards.

## Quick Start

```bash
git clone <repo-url>
cd bluestock_mf_capstone
pip install -r requirements.txt

# Run full ETL (fetches live NAV + loads SQLite)
python scripts/etl_pipeline.py

# Fetch latest NAV only (cron-friendly)
python scripts/live_nav_fetch.py
```

## Folder Structure

```
bluestock_mf_capstone/
├── data/
│   ├── raw/           ← original downloaded files + mfapi JSONs
│   ├── processed/     ← cleaned, merged CSVs
│   └── db/            ← bluestock_mf.db  (git-ignored; use schema.sql)
├── notebooks/
│   ├── 01_data_ingestion.ipynb
│   ├── 02_data_cleaning.ipynb
│   ├── 03_eda_analysis.ipynb
│   ├── 04_performance_analytics.ipynb
│   └── 05_advanced_analytics.ipynb
├── scripts/
│   ├── etl_pipeline.py       ← D1: full ETL
│   ├── live_nav_fetch.py     ← B1: cron NAV fetcher
│   ├── compute_metrics.py    ← D4: Sharpe/Beta/VaR
│   └── recommender.py        ← D6: fund recommender
├── sql/
│   ├── schema.sql
│   └── queries.sql
├── dashboard/
│   └── bluestock_mf.pbix
└── reports/
    ├── Final_Report.pdf
    └── Presentation.pptx
```

## Cron Job (B1 — Bonus)

Add to crontab for weekday 8 PM IST fetches:

```
0 14 * * 1-5  /usr/bin/python3 /absolute/path/scripts/live_nav_fetch.py >> /absolute/path/live_nav.log 2>&1
```

## Key Schemes

| Label | AMFI Code |
|---|---|
| HDFC Top 100 Direct | 125497 |
| SBI Bluechip | 119551 |
| ICICI Bluechip | 120503 |
| Nippon Large Cap | 118632 |
| Axis Bluechip | 119092 |
| Kotak Bluechip | 120841 |

## Notes

- All NAV series are forward-filled for weekends/holidays after reindex to full calendar range
- CAGR uses 252 trading days, not 365 calendar days
- AUM columns are in **INR Crore** (not lakh-crore) — units in column names
- Never commit `.db` files — use `schema.sql` to recreate
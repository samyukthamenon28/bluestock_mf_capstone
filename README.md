# Bluestock MF Capstone

Mutual Fund analytics capstone project — ETL, EDA, performance metrics, and dashboards.

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run the master E2E pipeline (cleans data, initializes schema, pulls NAVs, runs analytics, and builds documents)
python scripts/run_pipeline.py

# Launch the interactive Streamlit dashboard terminal
streamlit run dashboard/app.py

# Run the CLI recommender
python recommender.py --risk Moderate

# Verify the E2E product integrity
python scripts/verify_product.py
```

## Folder Structure

```
bluestock_mf_capstone/
├── data/
│   ├── raw/                  ← Original source files + downloaded NAVs
│   ├── processed/            ← Cleaned, structured CSVs
│   └── db/                   ← SQLite database (git-ignored; recreated via schema.sql)
├── notebooks/
│   ├── 01_data_ingestion (1).ipynb   ← Raw data exploration
│   ├── EDA_Analysis.ipynb            ← Day 3: Plotly and Seaborn EDA
│   ├── Performance_Analytics.ipynb   ← Day 4: Return and risk-adjusted metrics
│   └── Advanced_Analytics.ipynb      ← Day 6: Tail-risk and cohort notebook
├── scripts/
│   ├── clean_data.py                 ← Clean and format datasets
│   ├── load_star_schema.py           ← Ingestion into SQLite star schema
│   ├── etl_pipeline.py               ← Day 1-2 Master ETL runner
│   ├── cron_etl.py                   ← Day 5: Weekday cron ETL update script
│   ├── schedule_etl.py               ← Day 5: Windows Task Scheduler registrant
│   ├── live_nav_fetch.py             ← API fetching from mfapi.in
│   ├── generate_eda.py               ← Ingestion of EDA and figure export
│   ├── generate_analytics.py         ← Performance calculations and scorecard output
│   ├── generate_advanced_analytics.py ← Day 6: VaR, Sharpe, Cohorts, and HHI
│   ├── run_analysis.py               ← Execute queries and save report
│   ├── email_report.py               ← Day 5: weekly report compiler
│   ├── generate_pdf_report.py        ← Programmatic PDF compiler (ReportLab)
│   ├── generate_pptx_presentation.py  ← Programmatic PowerPoint builder (python-pptx)
│   ├── run_pipeline.py               ← Day 7 Master execution pipeline coordinator
│   └── verify_product.py             ← Day 7 E2E integrity checker
├── sql/
│   ├── schema.sql                    ← SQLite DDL schema definition
│   └── queries.sql                   ← Day 2: 10 analytical queries
├── dashboard/
│   └── app.py                        ← Day 5 & 6 Streamlit financial terminal
└── reports/
    ├── Final_Report.pdf              ← Compiled 15-20 page PDF report
    ├── Bluestock_MF_Presentation.pptx ← Compiled 12-slide PowerPoint presentation
    ├── analytical_report.md          ← Compiled SQL query results
    ├── weekly_performance_report.html ← Weekly HTML summary report
    └── figures/                      ← Saved EDA and performance charts
```

## Dataset Descriptions

The project ingests 10 primary datasets:
1. **01_fund_master.csv**: Scheme registration data including AMFI codes, category, sub-category, plan type (Direct/Regular), benchmark, minimum investment limits, and primary fund manager.
2. **02_nav_history.csv**: Historical day-by-day Net Asset Values (NAV) for all schemes, used to compute daily percentage returns.
3. **03_aum_by_fund_house.csv**: Monthly asset totals under management (AUM) in crores and lakh crores aggregated by AMC (Fund House).
4. **04_monthly_sip_inflows.csv**: Monthly industry-wide systematic investment plan (SIP) inflow totals and active accounts.
5. **05_category_inflows.csv**: Monthly asset class inflows split by broad categories (Equity, Debt, Hybrid).
6. **06_industry_folio_count.csv**: Aggregate account folio registration numbers across asset categories in India.
7. **07_scheme_performance.csv**: Historical annual returns (1-year, 3-year, 5-year), risk categories, and Morningstar ratings.
8. **08_investor_transactions.csv**: Demographics and transactions of investors (32,778 rows) including age, state, city, tier, payment modes, and annual income.
9. **09_portfolio_holdings.csv**: Underlying stock weight allocations and industry sectors for each equity fund.
10. **10_benchmark_indices.csv**: Historical daily closing values for Nifty 50 and Nifty 100 indices, used to calculate Alpha, Beta, and tracking errors.

## Scheduler Configuration (B1)

The NAV update pipeline is scheduled to auto-run every weekday at 8:00 PM IST. 

For Windows, it uses a Windows Task Scheduler task named `Bluestock_MF_ETL` which executes `scripts/cron_etl.py`.

For Linux/MacOS systems, append the following to the crontab:
```
0 20 * * 1-5  /usr/bin/python3 /absolute/path/scripts/cron_etl.py >> /absolute/path/cron_etl.log 2>&1
```

## Key Development Rules

- **Holiday Treatment**: All NAV timelines are reindexed to a full calendar date range and forward-filled (`ffill()`) to prevent weekend/holiday return distortions.
- **CAGR Calculations**: Annualized metrics utilize a 252-day business year instead of a 365-day calendar year to maintain consistency with market trading periods.
- **Interactive Dashboards**: All Streamlit dashboard workspaces feature at least two interactive slicers/filters.
- **Unit Clarity**: Scheme AUM columns are labeled as `aum_crore` to prevent confusion with industry-level AUM in lakh crores.
- **Git Hygiene**: The SQLite `.db` binary file is git-ignored. Codebase structural state is shared and updated via `schema.sql` and `queries.sql`.
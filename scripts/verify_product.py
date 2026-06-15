"""
verify_product.py — Bluestock MF Capstone: E2E Product Verification Script
Checks SQLite database tables, required output files, reports, and code syntax.
"""

import sys
import sqlite3
import json
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
DB_PATH = ROOT / "data" / "db" / "bluestock_mf.db"
REQUIRED_FILES = [
    ROOT / "var_cvar_report.csv",
    ROOT / "fund_scorecard.csv",
    ROOT / "alpha_beta.csv",
    ROOT / "rolling_sharpe_chart.png",
    ROOT / "reports" / "figures" / "benchmark_comparison.png",
    ROOT / "reports" / "analytical_report.md",
    ROOT / "reports" / "weekly_performance_report.html",
    ROOT / "reports" / "Final_Report.pdf",
    ROOT / "reports" / "Bluestock_Presentation_Final.pptx",
    ROOT / "notebooks" / "Advanced_Analytics.ipynb",
    ROOT / "notebooks" / "Performance_Analytics.ipynb",
    ROOT / "notebooks" / "EDA_Analysis.ipynb",
]

TABLES = [
    "dim_fund",
    "dim_date",
    "fact_nav",
    "fact_transactions",
    "fact_performance",
    "fact_aum",
]


def check_files() -> bool:
    print("=== Checking Required Deliverables ===")
    all_ok = True
    for file_path in REQUIRED_FILES:
        rel_path = file_path.relative_to(ROOT)
        if not file_path.exists():
            print(f"[ERROR] Missing file: {rel_path}")
            all_ok = False
        elif file_path.stat().st_size == 0:
            print(f"[ERROR] Empty file: {rel_path}")
            all_ok = False
        else:
            print(f"[OK] Found: {rel_path} ({file_path.stat().st_size} bytes)")
    return all_ok


def check_database() -> bool:
    print("\n=== Checking SQLite Database Table Row Counts ===")
    if not DB_PATH.exists():
        print(f"[ERROR] SQLite Database not found at: {DB_PATH.relative_to(ROOT)}")
        return False
        
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        all_ok = True
        for table in TABLES:
            cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table}'")
            exists = cursor.fetchone()
            if not exists:
                print(f"[ERROR] Table '{table}' does not exist.")
                all_ok = False
                continue
                
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            count = cursor.fetchone()[0]
            if count == 0:
                print(f"[ERROR] Table '{table}' contains 0 rows.")
                all_ok = False
            else:
                print(f"[OK] Table '{table}': {count} rows")
                
        conn.close()
        return all_ok
    except Exception as e:
        print(f"[ERROR] Database error: {e}")
        return False


def check_notebooks() -> bool:
    print("\n=== Checking Jupyter Notebook Formats ===")
    notebook_files = [
        ROOT / "notebooks" / "Advanced_Analytics.ipynb",
        ROOT / "notebooks" / "Performance_Analytics.ipynb",
        ROOT / "notebooks" / "EDA_Analysis.ipynb",
    ]
    all_ok = True
    for nb in notebook_files:
        if not nb.exists():
            print(f"[ERROR] Notebook missing: {nb.relative_to(ROOT)}")
            all_ok = False
            continue
        try:
            with open(nb, "r", encoding="utf-8") as f:
                data = json.load(f)
            # Basic nbformat check
            if "cells" not in data or "nbformat" not in data:
                print(f"[ERROR] Invalid notebook structure: {nb.relative_to(ROOT)}")
                all_ok = False
            else:
                print(f"[OK] Notebook format valid: {nb.relative_to(ROOT)} (cells: {len(data['cells'])})")
        except Exception as e:
            print(f"[ERROR] Failed to read/parse notebook {nb.relative_to(ROOT)}: {e}")
            all_ok = False
    return all_ok


def check_scripts_syntax() -> bool:
    print("\n=== Checking Python Scripts Compilation ===")
    import py_compile
    scripts = list((ROOT / "scripts").glob("*.py")) + [ROOT / "recommender.py"]
    all_ok = True
    for s in scripts:
        try:
            py_compile.compile(str(s), doraise=True)
            print(f"[OK] Compiles: {s.relative_to(ROOT)}")
        except Exception as e:
            print(f"[ERROR] Compilation failed: {s.relative_to(ROOT)} - {e}")
            all_ok = False
    return all_ok


def main():
    f_ok = check_files()
    db_ok = check_database()
    nb_ok = check_notebooks()
    scripts_ok = check_scripts_syntax()
    
    print("\n=========================================")
    if f_ok and db_ok and nb_ok and scripts_ok:
        print("SUCCESS: All product verification checks passed!")
        sys.exit(0)
    else:
        print("FAILURE: Some integrity checks failed. Review errors above.")
        sys.exit(1)


if __name__ == "__main__":
    main()

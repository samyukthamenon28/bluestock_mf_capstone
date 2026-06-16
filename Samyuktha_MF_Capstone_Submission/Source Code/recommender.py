"""
recommender.py — Bluestock MF Capstone: Fund Recommender (Day 6)
Command-line tool that inputs investor risk appetite (Low / Moderate / High) and
recommends the top 3 funds by Sharpe ratio within the matching database risk grades.
"""

import sys
import sqlite3
import argparse
from pathlib import Path
import pandas as pd
from tabulate import tabulate

ROOT = Path(__file__).resolve().parent
DB_PATH = ROOT / "data" / "db" / "bluestock_mf.db"


def get_recommendations(risk_appetite: str) -> pd.DataFrame:
    """Queries the database to find the top 3 funds matching the risk appetite sorted by Sharpe ratio."""
    risk_appetite = risk_appetite.strip().lower()
    
    # Map risk appetite to database risk_grade values
    if risk_appetite == "low":
        grades = ["Low"]
    elif risk_appetite == "moderate":
        grades = ["Moderate", "Moderately High"]
    elif risk_appetite == "high":
        grades = ["High", "Very High"]
    else:
        print(f"Error: Invalid risk appetite '{risk_appetite}'. Must be 'Low', 'Moderate', or 'High'.")
        sys.exit(1)
        
    if not DB_PATH.exists():
        print(f"Error: Database file not found at {DB_PATH}. Please run database ingestion first.")
        sys.exit(1)
        
    conn = sqlite3.connect(DB_PATH)
    
    # SQL query parameter placeholders
    placeholders = ",".join("?" for _ in grades)
    query = f"""
        SELECT f.amfi_code, f.scheme_name, f.fund_house, p.risk_grade, p.sharpe_ratio, p.return_3yr_pct
        FROM dim_fund f
        JOIN fact_performance p ON f.amfi_code = p.amfi_code
        WHERE p.risk_grade IN ({placeholders})
        ORDER BY p.sharpe_ratio DESC
        LIMIT 3
    """
    
    df = pd.read_sql_query(query, conn, params=grades)
    conn.close()
    return df


def main():
    parser = argparse.ArgumentParser(description="Bluestock Mutual Fund Recommender")
    parser.add_argument(
        "--risk", 
        type=str, 
        choices=["Low", "Moderate", "High", "low", "moderate", "high"], 
        help="Investor risk appetite (Low / Moderate / High)"
    )
    
    args = parser.parse_args()
    risk_appetite = args.risk
    
    # Fallback to interactive input if no CLI argument is passed
    if not risk_appetite:
        print("--- Bluestock Mutual Fund Recommender Terminal ---")
        try:
            risk_appetite = input("Enter your risk appetite (Low / Moderate / High): ").strip()
        except KeyboardInterrupt:
            print("\nExiting.")
            sys.exit(0)
            
    df_recs = get_recommendations(risk_appetite)
    
    if df_recs.empty:
        print("\nNo matching recommendations found for this risk appetite in the database.")
    else:
        # Format returns and Sharpe ratios for nice printing
        df_recs["sharpe_ratio"] = df_recs["sharpe_ratio"].map("{:.2f}".format)
        df_recs["return_3yr_pct"] = df_recs["return_3yr_pct"].map("{:.2f}%".format)
        
        # Rename columns for display
        df_recs.columns = ["AMFI Code", "Scheme Name", "Fund House", "Risk Grade", "Sharpe Ratio", "3-Year Return"]
        
        print(f"\nRecommended Top 3 Funds for '{risk_appetite.capitalize()}' Risk Appetite:")
        print(tabulate(df_recs, headers="keys", tablefmt="grid", showindex=False))
        print("\nDisclaimer: Mutual fund investments are subject to market risks. Read all scheme related documents carefully.\n")


if __name__ == "__main__":
    main()

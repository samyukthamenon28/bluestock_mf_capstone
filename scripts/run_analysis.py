"""
run_analysis.py — Bluestock MF Capstone: Run Analytical Queries (D2)
Parses sql/analytical_queries.sql, runs them against SQLite, prints the results,
and compiles them into reports/analytical_report.md.
"""

import os
import re
import sqlite3
import logging
from pathlib import Path
import pandas as pd

# ── Paths ──────────────────────────────────────────────────────────────────────
ROOT = Path(__file__).resolve().parent.parent
DB_PATH = ROOT / "data" / "db" / "bluestock_mf.db"
SQL_QUERIES_PATH = ROOT / "sql" / "analytical_queries.sql"
REPORT_PATH = ROOT / "reports" / "analytical_report.md"

ROOT / "reports"  # ensure directory exists

# ── Logging ────────────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
log = logging.getLogger(__name__)


def parse_queries(sql_path: Path) -> list[dict]:
    """Parses queries from the SQL file based on '-- Query' markers."""
    with open(sql_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Split using regex to catch Query sections
    sections = re.split(r"-- ─+\s*\n-- (Query \d+:[^\n]+)\n-- ([^\n]+)\n-- ─+\n", content)
    
    # The first element is file header
    queries = []
    # sections will have elements: [header, title1, description1, sql1, title2, description2, sql2, ...]
    if len(sections) > 1:
        for i in range(1, len(sections), 3):
            title = sections[i].strip()
            desc = sections[i+1].strip()
            sql_body = sections[i+2].split(";")[0].strip() + ";" # execute only first statement in section
            queries.append({
                "title": title,
                "description": desc,
                "sql": sql_body
            })
    else:
        # Fallback split by semicolons if parser fails
        statements = content.split(";")
        for idx, stmt in enumerate(statements):
            stmt = stmt.strip()
            if stmt:
                queries.append({
                    "title": f"Query {idx+1}",
                    "description": "",
                    "sql": stmt + ";"
                })
    return queries


def run_queries_and_report():
    log.info("Connecting to SQLite database at %s ...", DB_PATH)
    conn = sqlite3.connect(DB_PATH)
    
    queries = parse_queries(SQL_QUERIES_PATH)
    log.info("Parsed %d queries from %s", len(queries), SQL_QUERIES_PATH.name)
    
    report_lines = [
        "# Analytical SQL Report — Bluestock MF Capstone",
        "This report compiles the results of the 10 analytical SQL queries executed on the Star Schema database.",
        "",
    ]
    
    for idx, q in enumerate(queries, 1):
        title = q["title"]
        desc = q["description"]
        sql = q["sql"]
        
        log.info("Executing %s ...", title)
        print(f"\n=========================================")
        print(f"{title}")
        print(f"Description: {desc}")
        print(f"=========================================")
        
        try:
            df = pd.read_sql_query(sql, conn)
            # Display first 15 rows in console
            print(df.head(15).to_string(index=False))
            print()
            
            # Format report
            report_lines.append(f"## {title}")
            report_lines.append(f"*{desc}*")
            report_lines.append("")
            report_lines.append("### SQL Query")
            report_lines.append(f"```sql\n{sql}\n```")
            report_lines.append("")
            report_lines.append("### Results")
            report_lines.append(df.to_markdown(index=False))
            report_lines.append("")
            report_lines.append("---")
            report_lines.append("")
            
        except Exception as e:
            log.error("Error executing query %d (%s): %s", idx, title, e)
            print(f"Error: {e}\n")
            
    conn.close()
    
    # Save Report
    with open(REPORT_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(report_lines))
    log.info("Analysis report saved -> %s", REPORT_PATH.name)


def main():
    run_queries_and_report()


if __name__ == "__main__":
    main()

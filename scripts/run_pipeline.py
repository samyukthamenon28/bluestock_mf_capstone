"""
run_pipeline.py — Bluestock MF Capstone: Master Execution Pipeline Runner
Sequentially executes every script in the analytics lifecycle:
1. Clean local CSV datasets
2. Ingest schema DDL & raw clean data into SQLite
3. Fetch live NAV values from API & forward-fill holiday sequences
4. Generate EDA visualizations (16+ charts)
5. Calculate returns scorecards (CAGR, Sharpe, Sortino)
6. Calculate tail-risk parameters (VaR/CVaR, cohorts, continuity, HHI)
7. Execute analytical queries & compile report
8. Programmatically compile the final PDF report and presentation.
"""

import sys
import subprocess
from pathlib import Path
import logging

ROOT = Path(__file__).resolve().parent.parent

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
log = logging.getLogger("MasterPipeline")


def run_script(script_name: str, args: list = None) -> bool:
    """Executes a Python script in a subprocess and logs output."""
    script_path = ROOT / "scripts" / script_name
    if not script_path.exists():
        script_path = ROOT / script_name # check root for recommender
        
    if not script_path.exists():
        log.error("Script not found: %s", script_name)
        return False
        
    cmd = [sys.executable, str(script_path)]
    if args:
        cmd.extend(args)
        
    log.info("Running script: %s ...", script_name)
    try:
        res = subprocess.run(cmd, check=True, capture_output=True, text=True)
        log.info("Success: %s", script_name)
        if res.stdout:
            print(res.stdout.strip())
        return True
    except subprocess.CalledProcessError as err:
        log.error("Failed running %s: exit code %d", script_name, err.returncode)
        if err.stdout:
            print("Stdout:\n", err.stdout)
        if err.stderr:
            print("Stderr:\n", err.stderr)
        return False


def main():
    log.info("Starting Bluestock Mutual Fund Capstone E2E Execution Pipeline")
    print("=" * 70)
    
    steps = [
        ("clean_data.py", None),
        ("load_star_schema.py", None),
        ("etl_pipeline.py", None),
        ("generate_eda.py", None),
        ("generate_analytics.py", None),
        ("generate_advanced_analytics.py", None),
        ("run_analysis.py", None),
        ("generate_pdf_report.py", None),
        ("generate_pptx_presentation.py", None),
    ]
    
    for script, args in steps:
        ok = run_script(script, args)
        if not ok:
            log.critical("Pipeline halted due to error in %s", script)
            sys.exit(1)
            
    print("=" * 70)
    log.info("E2E Execution Pipeline completed successfully! All deliverables generated.")
    sys.exit(0)


if __name__ == "__main__":
    main()

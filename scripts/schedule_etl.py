"""
schedule_etl.py — Bluestock MF Capstone: Schedule Weekday ETL task (B1)
Configures Windows Task Scheduler to run cron_etl.py every weekday at 8:00 PM.
Supports fallback printing for Linux/macOS crontab configurations.
"""

import sys
import os
import subprocess
import logging
from pathlib import Path

# ── Paths ──────────────────────────────────────────────────────────────────────
ROOT = Path(__file__).resolve().parent.parent
CRON_ETL_PATH = ROOT / "scripts" / "cron_etl.py"

# ── Logging ────────────────────────────────────────────────────────────────────
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger(__name__)


def schedule_windows():
    """Register the task in Windows Task Scheduler using schtasks.exe."""
    task_name = "Bluestock_MF_ETL"
    python_exe = sys.executable  # Use current environment's Python executable
    
    # Task scheduler arguments
    # Run every weekly on weekdays (MON, TUE, WED, THU, FRI) at 20:00 (8:00 PM)
    cmd = [
        "schtasks", "/create",
        "/tn", task_name,
        "/tr", f'"{python_exe}" "{CRON_ETL_PATH}"',
        "/sc", "weekly",
        "/d", "MON,TUE,WED,THU,FRI",
        "/st", "20:00",
        "/f"  # force overwrite if task exists
    ]
    
    log.info("Registering Windows Task Scheduler task: %s", task_name)
    log.info("Command: %s", " ".join(cmd))
    
    try:
        res = subprocess.run(cmd, capture_output=True, text=True, check=True)
        log.info("✓ Success: %s", res.stdout.strip())
        
        # Verify the task
        verify_cmd = ["schtasks", "/query", "/tn", task_name, "/fo", "LIST"]
        res_verify = subprocess.run(verify_cmd, capture_output=True, text=True)
        if res_verify.returncode == 0:
            log.info("Task Scheduler Verification:\n%s", res_verify.stdout.strip())
        else:
            log.warning("Could not query created task (this is normal if permission limits apply): %s", res_verify.stderr)
    except subprocess.CalledProcessError as exc:
        log.error("✗ Failed to create task scheduler task: %s", exc.stderr)
        log.warning("Note: Task Scheduler might require Administrator permissions to schedule from the terminal.")
        log.warning("You can run this script inside an Administrator Command Prompt or PowerShell window.")


def print_cron_format():
    """Print the crontab configuration for Linux/macOS."""
    python_exe = sys.executable
    cron_line = f"0 20 * * 1-5 {python_exe} {CRON_ETL_PATH} >> {ROOT}/cron_etl.log 2>&1"
    
    print("\n" + "=" * 60)
    print("Linux / macOS Crontab Equivalent (Weekdays 8:00 PM):")
    print("=" * 60)
    print("Run `crontab -e` and append the following line:")
    print(cron_line)
    print("=" * 60 + "\n")


def main():
    if os.name == "nt":
        schedule_windows()
        print_cron_format()
    else:
        log.info("Non-Windows OS detected. Printing crontab configurations.")
        print_cron_format()


if __name__ == "__main__":
    main()

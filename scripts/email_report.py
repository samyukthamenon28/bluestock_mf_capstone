"""
email_report.py — Bluestock MF Capstone: Weekly Performance Report Generator (B5)
Compiles computed mutual fund performance analytics into a premium styled HTML report.
Saves the HTML file to reports/weekly_performance_report.html for easy browser preview
and provides an option to send it via SMTP if mail server variables are configured.
"""

import os
import sys
import logging
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path
import pandas as pd
from dotenv import load_dotenv

# Load env variables if present
load_dotenv()

# ── Paths ──────────────────────────────────────────────────────────────────────
ROOT = Path(__file__).resolve().parent.parent
SCORECARD_PATH = ROOT / "fund_scorecard.csv"
ALPHA_BETA_PATH = ROOT / "alpha_beta.csv"
REPORT_OUT_PATH = ROOT / "reports" / "weekly_performance_report.html"

# ── Logging ────────────────────────────────────────────────────────────────────
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger(__name__)


def generate_html_report() -> str:
    """Read calculations and compile into an HTML string with premium CSS styles."""
    if not SCORECARD_PATH.exists() or not ALPHA_BETA_PATH.exists():
        log.error("Scorecard files do not exist. Please run analytics calculations first.")
        raise FileNotFoundError("Calculated scorecard CSVs missing.")

    # Read CSVs
    df_sc = pd.read_csv(SCORECARD_PATH)
    df_ab = pd.read_csv(ALPHA_BETA_PATH)

    # Compile KPI summaries
    top_3 = df_sc.head(3)
    avg_cagr_3y = df_sc["cagr_3y"].mean() * 100
    avg_sharpe = df_sc["sharpe_ratio"].mean()
    avg_expense = df_sc["expense_ratio_pct"].mean()

    # Generate Top 10 Leaderboard HTML table rows
    leaderboard_rows = ""
    for idx, row in df_sc.head(10).iterrows():
        leaderboard_rows += f"""
        <tr>
            <td style="padding: 12px; border-bottom: 1px solid #e2e8f0; font-weight: bold; color: #1e293b;">{idx+1}</td>
            <td style="padding: 12px; border-bottom: 1px solid #e2e8f0; color: #334155;">{row['scheme_name']}</td>
            <td style="padding: 12px; border-bottom: 1px solid #e2e8f0; color: #64748b;">{row['fund_house']}</td>
            <td style="padding: 12px; border-bottom: 1px solid #e2e8f0; color: #10b981; font-weight: 600;">{row['cagr_3y']*100:.2f}%</td>
            <td style="padding: 12px; border-bottom: 1px solid #e2e8f0; color: #334155;">{row['sharpe_ratio']:.2f}</td>
            <td style="padding: 12px; border-bottom: 1px solid #e2e8f0; color: #ef4444;">{row['max_drawdown']*100:.2f}%</td>
            <td style="padding: 12px; border-bottom: 1px solid #e2e8f0; text-align: right; font-weight: bold; color: #4f46e5;">{row['composite_score']:.2f}</td>
        </tr>
        """

    # Premium CSS styled HTML template
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>Bluestock Mutual Fund Weekly Performance Summary</title>
        <style>
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background-color: #f8fafc;
                margin: 0;
                padding: 0;
                color: #1e293b;
            }}
            .container {{
                max-width: 800px;
                margin: 40px auto;
                background: #ffffff;
                border-radius: 12px;
                box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
                overflow: hidden;
                border: 1px solid #e2e8f0;
            }}
            .header {{
                background: linear-gradient(135deg, #4f46e5 0%, #312e81 100%);
                padding: 40px;
                color: white;
                text-align: center;
            }}
            .header h1 {{
                margin: 0;
                font-size: 28px;
                font-weight: 700;
                letter-spacing: -0.05em;
            }}
            .header p {{
                margin: 10px 0 0 0;
                font-size: 16px;
                opacity: 0.9;
            }}
            .content {{
                padding: 40px;
            }}
            .kpi-row {{
                display: flex;
                justify-content: space-between;
                margin-bottom: 30px;
                gap: 20px;
            }}
            .kpi-card {{
                flex: 1;
                background-color: #f1f5f9;
                border-left: 4px solid #6366f1;
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0 1px 3px rgba(0,0,0,0.02);
            }}
            .kpi-title {{
                font-size: 12px;
                color: #64748b;
                text-transform: uppercase;
                font-weight: 600;
                letter-spacing: 0.05em;
            }}
            .kpi-value {{
                font-size: 22px;
                font-weight: 700;
                color: #1e293b;
                margin-top: 5px;
            }}
            .section-title {{
                font-size: 18px;
                font-weight: 700;
                color: #1e293b;
                border-bottom: 2px solid #e2e8f0;
                padding-bottom: 8px;
                margin-top: 40px;
                margin-bottom: 20px;
            }}
            table {{
                width: 100%;
                border-collapse: collapse;
                margin-bottom: 30px;
            }}
            th {{
                background-color: #f8fafc;
                color: #475569;
                font-weight: 600;
                text-align: left;
                padding: 12px;
                border-bottom: 2px solid #e2e8f0;
                font-size: 13px;
                text-transform: uppercase;
            }}
            .footer {{
                background-color: #f8fafc;
                padding: 20px;
                text-align: center;
                font-size: 12px;
                color: #64748b;
                border-top: 1px solid #e2e8f0;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>📈 Mutual Fund Weekly Performance</h1>
                <p>Bluestock Capstone Performance Analytics Report</p>
            </div>
            
            <div class="content">
                <!-- KPI Section -->
                <div class="kpi-row">
                    <div class="kpi-card">
                        <div class="kpi-title">Average 3Y CAGR</div>
                        <div class="kpi-value">{avg_cagr_3y:.2f}%</div>
                    </div>
                    <div class="kpi-card">
                        <div class="kpi-title">Average Sharpe</div>
                        <div class="kpi-value">{avg_sharpe:.2f}</div>
                    </div>
                    <div class="kpi-card">
                        <div class="kpi-title">Average Expense</div>
                        <div class="kpi-value">{avg_expense:.2f}%</div>
                    </div>
                </div>

                <!-- Top 3 Leaders Section -->
                <div class="section-title">🏆 Top 3 Leaderboard Funds</div>
                <div style="background-color: #eff6ff; border: 1px solid #bfdbfe; border-radius: 8px; padding: 20px; margin-bottom: 30px;">
                    <ol style="margin: 0; padding-left: 20px; font-size: 15px; color: #1e3a8a;">
                        <li style="margin-bottom: 10px;"><strong>{top_3.iloc[0]['scheme_name']}</strong> (Score: {top_3.iloc[0]['composite_score']:.2f}) | 3Y CAGR: {top_3.iloc[0]['cagr_3y']*100:.2f}%</li>
                        <li style="margin-bottom: 10px;"><strong>{top_3.iloc[1]['scheme_name']}</strong> (Score: {top_3.iloc[1]['composite_score']:.2f}) | 3Y CAGR: {top_3.iloc[1]['cagr_3y']*100:.2f}%</li>
                        <li style="margin-bottom: 0;"><strong>{top_3.iloc[2]['scheme_name']}</strong> (Score: {top_3.iloc[2]['composite_score']:.2f}) | 3Y CAGR: {top_3.iloc[2]['cagr_3y']*100:.2f}%</li>
                    </ol>
                </div>

                <!-- Leaderboard Table -->
                <div class="section-title">📊 Top 10 Fund Performance Details</div>
                <table>
                    <thead>
                        <tr>
                            <th>Rank</th>
                            <th>Scheme Name</th>
                            <th>Fund House</th>
                            <th>3Y CAGR</th>
                            <th>Sharpe</th>
                            <th>Max DD</th>
                            <th style="text-align: right;">Score</th>
                        </tr>
                    </thead>
                    <tbody>
                        {leaderboard_rows}
                    </tbody>
                </table>
                
                <p style="font-size: 13px; color: #64748b; font-style: italic; margin-top: 20px;">
                    * Risk calculations use 6.5% annually as the risk-free rate proxy. CAGRs are calculated on trading days (252 trading days per year).
                </p>
            </div>
            
            <div class="footer">
                <p>Sent by Bluestock Automated Analytics Scheduler. Please do not reply directly to this email.</p>
                <p>&copy; 2026 Bluestock Mutual Fund Capstone Project.</p>
            </div>
        </div>
    </body>
    </html>
    """
    return html_content


def send_report_email(html_body: str):
    """Attempt to send the HTML report via SMTP if environment variables are set."""
    smtp_server = os.getenv("SMTP_SERVER")
    smtp_port = os.getenv("SMTP_PORT")
    sender_email = os.getenv("SMTP_SENDER_EMAIL")
    sender_pass = os.getenv("SMTP_SENDER_PASSWORD")
    recipient_email = os.getenv("SMTP_RECIPIENT_EMAIL")

    if not all([smtp_server, smtp_port, sender_email, sender_pass, recipient_email]):
        log.info("SMTP variables are not configured in environment/.env file. Skipping email transmission.")
        log.info("Weekly report drafted successfully and written to reports directory.")
        return

    log.info("Attempting to send email via SMTP to %s...", recipient_email)
    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = "Weekly Mutual Fund Performance Summary Report"
        msg["From"] = sender_email
        msg["To"] = recipient_email

        part_html = MIMEText(html_body, "html")
        msg.attach(part_html)

        # Connect and send
        server = smtplib.SMTP(smtp_server, int(smtp_port))
        server.starttls()
        server.login(sender_email, sender_pass)
        server.sendmail(sender_email, recipient_email, msg.as_string())
        server.quit()
        log.info("✓ Weekly Performance Report email sent successfully!")
    except Exception as exc:
        log.error("✗ Failed to send email via SMTP: %s", exc)


def main():
    log.info("Generating Weekly Performance HTML Report...")
    try:
        # Create reports output directory
        REPORT_OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
        
        html_body = generate_html_report()
        
        # Write report to disk
        REPORT_OUT_PATH.write_text(html_body, encoding="utf-8")
        log.info("✓ Report successfully saved to disk → %s", REPORT_OUT_PATH.name)
        
        # Attempt to email it
        send_report_email(html_body)
        log.info("Report generation complete. OK")
        
    except Exception as e:
        log.error("Fatal error during report generator: %s", e)
        sys.exit(1)


if __name__ == "__main__":
    main()

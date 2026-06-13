"""
generate_pptx_presentation.py — Bluestock MF Capstone: 12-Slide PowerPoint Builder (python-pptx)
Compiles a 12-slide presentation summarizing the problem, data sources, star schema,
EDA, performance leaderboards, advanced risk simulations, and final recommendations.
"""

import sys
from pathlib import Path
from datetime import datetime
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

# ── Paths ──────────────────────────────────────────────────────────────────────
ROOT = Path(__file__).resolve().parent.parent
PPTX_OUT = ROOT / "reports" / "Bluestock_MF_Presentation.pptx"

# Ensure reports directory exists
PPTX_OUT.parent.mkdir(parents=True, exist_ok=True)

# ── Slide Color Constants ──────────────────────────────────────────────────────
BG_COLOR = RGBColor(15, 23, 42)        # Dark Slate / Navy (0f172a)
CARD_COLOR = RGBColor(30, 41, 59)      # Slate Card (1e293b)
TEXT_WHITE = RGBColor(255, 255, 255)   # White
TEXT_GRAY = RGBColor(148, 163, 184)    # Cool Gray (94a6b8)
ACCENT_INDIGO = RGBColor(129, 140, 248) # Neon Indigo/Lavender (818cf8)
ACCENT_RED = RGBColor(248, 113, 113)   # Soft Red (f87171)


def add_slide_background(slide, color):
    """Set slide background fill color."""
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = color


def add_slide_header(slide, title_text):
    """Create a uniform slide header title."""
    title_box = slide.shapes.add_textbox(Inches(0.5), Inches(0.4), Inches(9.0), Inches(0.8))
    tf = title_box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = title_text.upper()
    p.font.name = "Arial"
    p.font.size = Pt(28)
    p.font.bold = True
    p.font.color.rgb = ACCENT_INDIGO
    return title_box


def add_bullet_points(slide, points, left, top, width, height, font_size=15):
    """Add a bullet point text frame on the slide."""
    txBox = slide.shapes.add_textbox(left, top, width, height)
    tf = txBox.text_frame
    tf.word_wrap = True
    
    for idx, pt in enumerate(points):
        if idx == 0:
            p = tf.paragraphs[0]
        else:
            p = tf.add_paragraph()
        p.text = pt
        p.font.name = "Arial"
        p.font.size = Pt(font_size)
        p.font.color.rgb = TEXT_WHITE
        p.space_after = Pt(8)
        if pt.startswith("• "):
            p.text = pt[2:]
            p.level = 0
        elif pt.startswith("  - "):
            p.text = pt[4:]
            p.level = 1
    return txBox


def build_presentation():
    prs = Presentation()
    # Set standard widescreen 16:9 layout size
    prs.slide_width = Inches(10)
    prs.slide_height = Inches(5.625)
    
    # ── SLIDE 1: Title Slide ───────────────────────────────────────────────────
    slide_layout = prs.slide_layouts[6] # Blank Layout
    slide1 = prs.slides.add_slide(slide_layout)
    add_slide_background(slide1, BG_COLOR)
    
    # Decorative Accent Line
    accent = slide1.shapes.add_shape(
        1, Inches(0.5), Inches(1.8), Inches(9.0), Inches(0.08) # MSO_SHAPE_RECTANGLE = 1
    )
    accent.fill.solid()
    accent.fill.fore_color.rgb = ACCENT_INDIGO
    accent.line.fill.background()
    
    # Title Text Frame
    title_box = slide1.shapes.add_textbox(Inches(0.5), Inches(2.0), Inches(9.0), Inches(2.0))
    tf = title_box.text_frame
    tf.word_wrap = True
    
    p = tf.paragraphs[0]
    p.text = "BLUESTOCK MUTUAL FUND ANALYTICS"
    p.font.name = "Arial"
    p.font.size = Pt(36)
    p.font.bold = True
    p.font.color.rgb = TEXT_WHITE
    p.space_after = Pt(6)
    
    p2 = tf.add_paragraph()
    p2.text = "E2E Quantitative Performance Scorecards, Tail-Risk Modeling, and Ingestion Engine"
    p2.font.name = "Arial"
    p2.font.size = Pt(14)
    p2.font.color.rgb = ACCENT_INDIGO
    
    # Metadata Box
    meta_box = slide1.shapes.add_textbox(Inches(0.5), Inches(4.5), Inches(9.0), Inches(0.8))
    tf_m = meta_box.text_frame
    p_m = tf_m.paragraphs[0]
    p_m.text = f"Presenter: Antigravity AI Pair Programmer  |  Date: {datetime.now().strftime('%B %d, %Y')}\nFrameworks: Python, SQLite, Plotly, Streamlit  |  Version: 1.0 (Final Release)"
    p_m.font.name = "Arial"
    p_m.font.size = Pt(10)
    p_m.font.color.rgb = TEXT_GRAY

    # ── SLIDE 2: Problem & Objective ──────────────────────────────────────────
    slide2 = prs.slides.add_slide(slide_layout)
    add_slide_background(slide2, BG_COLOR)
    add_slide_header(slide2, "Problem & Objective")
    
    points2 = [
        "• Mutual fund analytics often lack clean historical price alignment, leading to return calculation bias over holiday periods.",
        "• Standard retail dashboards do not incorporate tail-risk measures (VaR/CVaR) or interactive simulation engines.",
        "• Objectives of the Capstone Project:",
        "  - Build a fully automated E2E weekday ETL ingestion pipeline for AMFI mutual funds.",
        "  - Design a star schema SQL database storing fund attributes, NAV histories, and client transactions.",
        "  - Implement performance scorecards (Sharpe, Sortino, CAGR, Jensen's Alpha, Beta).",
        "  - Conduct cohort retention audits and model dynamic portfolio optimizations."
    ]
    add_bullet_points(slide2, points2, Inches(0.5), Inches(1.3), Inches(9.0), Inches(3.8))

    # ── SLIDE 3: Data Sources ──────────────────────────────────────────────────
    slide3 = prs.slides.add_slide(slide_layout)
    add_slide_background(slide3, BG_COLOR)
    add_slide_header(slide3, "Data Sources & Dimensions")
    
    points3 = [
        "• Ingests 10 primary CSV datasets representing mid-2022 through mid-2026 records:",
        "  - Fund Master: 40 unique schemes, classifications, and fund managers.",
        "  - NAV History / API: Daily NAVs from mfapi.in, reindexed and filled (64,354 rows).",
        "  - Scheme Performance: Return percentages and Morningstar ratings.",
        "  - Portfolio Holdings: 322 stock allocations, symbols, weights, and sectors.",
        "  - Investor Transactions: 32,778 transaction records detailing state, age, and gender.",
        "  - Auxiliary Tables: AUM growth, monthly SIP inflows, category flows, and folio counts.",
        "  - Index Benchmarks: Daily index close values for Nifty 50 and Nifty 100 (8,050 rows)."
    ]
    add_bullet_points(slide3, points3, Inches(0.5), Inches(1.3), Inches(9.0), Inches(3.8))

    # ── SLIDE 4: Architecture ──────────────────────────────────────────────────
    slide4 = prs.slides.add_slide(slide_layout)
    add_slide_background(slide4, BG_COLOR)
    add_slide_header(slide4, "ETL Pipeline & Schema Design")
    
    points4 = [
        "• Master Pipeline Ingestion Flow: Python scripts extract CSVs -> clean data -> load SQLite.",
        "• Holiday Forward-Filling (Critical Rule):",
        "  - Reindexes NAV dates to a full calendar range, forward-filling weekends and holidays.",
        "  - Eliminates standard deviation distortion when calculating daily percentage returns.",
        "• Annualization Metric Rules:",
        "  - Returns, variances, and Sharpe ratios are annualized utilizing a 252-day business year.",
        "• Star Schema Layout: dim_fund (AMFI PK) and dim_date (date_id PK) act as unified dimensions.",
        "  - Linked to fact tables: fact_nav, fact_transactions, fact_performance, and fact_aum."
    ]
    add_bullet_points(slide4, points4, Inches(0.5), Inches(1.3), Inches(9.0), Inches(3.8))

    # ── SLIDE 5: EDA Highlights (1) ────────────────────────────────────────────
    slide5 = prs.slides.add_slide(slide_layout)
    add_slide_background(slide5, BG_COLOR)
    add_slide_header(slide5, "EDA Highlights: Macro Industry Growth")
    
    points5 = [
        "• Steady NAV & AUM Growth: Long-term trends show steady performance, led by large-cap funds.",
        "• 2023 Bull Run: Sustained positive returns across all equity categories as valuations expanded.",
        "• Monthly SIP Inflows: Monthly retail contributions show consistent upward momentum,",
        "  demonstrating retail dollar-cost averaging discipline despite short-term market drops.",
        "• Folio Account Growth: Total mutual fund account count in India grew steadily,",
        "  confirming growing financial literacy and migration of savings into public equity markets.",
        "• Sector Allocations: Average equity fund allocations are dominated by Financial Services,",
        "  Information Technology, Energy, and Consumer Staples."
    ]
    add_bullet_points(slide5, points5, Inches(0.5), Inches(1.3), Inches(9.0), Inches(3.8))

    # ── SLIDE 6: EDA Highlights (2) ────────────────────────────────────────────
    slide6 = prs.slides.add_slide(slide_layout)
    add_slide_background(slide6, BG_COLOR)
    add_slide_header(slide6, "EDA Highlights: Investor Demographics")
    
    points6 = [
        "• Age Bracket Concentrations: Over 65% of the investor transaction base lies in the",
        "  26-35 and 36-45 age groups, representing young to mid-career professionals.",
        "• SIP Size by Age: Boxplot analysis shows older age brackets (46-55, 56+) maintain a wider",
        "  dispersion and higher median transaction size, reflecting accumulated wealth.",
        "• Geographic Contributions: Top investor counts originate from Maharashtra and Gujarat.",
        "• City Tier Contribution Split (T30 vs B30):",
        "  - Top 30 (T30) cities represent the majority of asset volume.",
        "  - Beyond 30 (B30) cities show rapid, compounding folio registration growth,",
        "    highlighting the geographical expansion of mutual fund penetration in India."
    ]
    add_bullet_points(slide6, points6, Inches(0.5), Inches(1.3), Inches(9.0), Inches(3.8))

    # ── SLIDE 7: Performance Metrics (1) ───────────────────────────────────────
    slide7 = prs.slides.add_slide(slide_layout)
    add_slide_background(slide7, BG_COLOR)
    add_slide_header(slide7, "Performance scorecards & leaderboards")
    
    points7 = [
        "• Scorecard Formulation: All 40 schemes are evaluated over a 3-year performance window.",
        "• Risk-Adjusted Ratios:",
        "  - Sharpe Ratio: Compares excess return to total standard deviation (risk-free rate = 6.5%).",
        "  - Sortino Ratio: Adjusts return for downside deviation, ignoring upside volatility.",
        "• Regression Coefficients (Jensen's Alpha & Beta):",
        "  - Regressed daily log returns of funds against Nifty 100 index daily returns.",
        "  - Determines systematic risk exposure (Beta) and excess manager alpha.",
        "• Weighted Composite Score (out of 100):",
        "  - Sharpe (30%), Sortino (20%), 3-Year CAGR (30%), and Max Drawdown (20%)."
    ]
    add_bullet_points(slide7, points7, Inches(0.5), Inches(1.3), Inches(9.0), Inches(3.8))

    # ── SLIDE 8: Performance Metrics (2) ───────────────────────────────────────
    slide8 = prs.slides.add_slide(slide_layout)
    add_slide_background(slide8, BG_COLOR)
    add_slide_header(slide8, "Top Performing Funds Leaderboard")
    
    points8 = [
        "• Top 5 Funds by Risk-Adjusted Sharpe Ratio:",
        "  1. HDFC Top 100 Direct - Growth (AMFI: 125497): Leading composite score & return profile.",
        "  2. SBI Bluechip Fund - Direct - Growth (AMFI: 119551): Stable Sharpe, low Beta.",
        "  3. ICICI Prudential Bluechip Fund - Direct - Growth (AMFI: 120503): Solid outperformance.",
        "  4. Nippon India Large Cap Fund - Direct - Growth (AMFI: 118632): Consistent alpha.",
        "  5. Axis Bluechip Fund - Direct - Growth (AMFI: 119092): Strong technology bias.",
        "• Alpha / Beta Insights: Top active large-cap funds successfully generated positive annual alpha",
        "  while maintaining Beta coefficients close to 0.85-0.95 relative to the Nifty 100 index.",
        "• Cumulative Performance: Best funds outperformed the standard Nifty 50 by over 4.5% annualized."
    ]
    add_bullet_points(slide8, points8, Inches(0.5), Inches(1.3), Inches(9.0), Inches(3.8))

    # ── SLIDE 9: Dashboard Screenshots (1) ─────────────────────────────────────
    slide9 = prs.slides.add_slide(slide_layout)
    add_slide_background(slide9, BG_COLOR)
    add_slide_header(slide9, "Dashboard Design & Core Workspaces")
    
    points9 = [
        "• Streamlit UI Layout: Structured as a custom cyber-financial terminal.",
        "• Slicer and Filter Controls: Multi-select lists, sliders, and date inputs on every page.",
        "• Dashboard Workspaces (Pages 1 - 3):",
        "  - Page 1: Fund Scorecard & Benchmark - Interactive scoreboard leaderboards,",
        "    benchmark tracking comparisons, and dynamic tracking error metrics.",
        "  - Page 2: NAV Analysis & Correlation - Timelines of daily NAVs, return distribution histograms,",
        "    and OLS linear return correlation matrices.",
        "  - Page 3: Industry & AUM Growth - Macro trends in total folios and monthly inflows."
    ]
    add_bullet_points(slide9, points9, Inches(0.5), Inches(1.3), Inches(9.0), Inches(3.8))

    # ── SLIDE 10: Dashboard Screenshots (2) ────────────────────────────────────
    slide10 = prs.slides.add_slide(slide_layout)
    add_slide_background(slide10, BG_COLOR)
    add_slide_header(slide10, "Dashboard: Simulation & Risk Workspace")
    
    points10 = [
        "• Dashboard Workspaces (Pages 4 - 6):",
        "  - Page 4: Investor Demographics - Aggregated charts of age, gender, and state attributes.",
        "  - Page 5: Advanced Simulation & Optimization - Runs Monte Carlo simulations using",
        "    Geometric Brownian Motion (GBM) and computes Markowitz Efficient Frontier weights.",
        "  - Page 6: Advanced Risk & Cohort Analytics - Tail-risk VaR/CVaR tables, rolling Sharpe plots,",
        "    investor cohorts, and Sector HHI concentration group comparisons.",
        "• Premium Visual Aesthetics: Radial gradient backdrops, neon borders, and tabular layouts",
        "  without unnecessary icons or standard widgets to maintain a premium look."
    ]
    add_bullet_points(slide10, points10, Inches(0.5), Inches(1.3), Inches(9.0), Inches(3.8))

    # ── SLIDE 11: Key Findings ────────────────────────────────────────────────
    slide11 = prs.slides.add_slide(slide_layout)
    add_slide_background(slide11, BG_COLOR)
    add_slide_header(slide11, "Key Findings & Recommendations")
    
    points11 = [
        "• Tail Risk parameters: Small-cap equity schemes show daily 95% VaR losses up to -2.63%,",
        "  requiring portfolio managers to size holdings dynamically. Liquid funds maintain 0% VaR.",
        "• SIP Continuity Warning: Analysis flagged 97.80% of long-term investors (1,332 out of 1,362)",
        "  as 'at-risk' due to transaction gaps exceeding 35 days (missed payments).",
        "• Sector HHI Concentration: Axis Bluechip exhibits the highest sector concentration (HHI: 2967.69),",
        "  while UTI Mid Cap shows the highest diversification (HHI: 1240.20).",
        "• Strategic Actionable Recommendations:",
        "  - Implement automatic UPI mandate renewal alerts 28 days after the last SIP date.",
        "  - Leverage Markowitz Frontier weights to provide personalized client recommendations.",
        "  - standardise holiday ffill() across all analytics teams to prevent index return distortions."
    ]
    add_bullet_points(slide11, points11, Inches(0.5), Inches(1.3), Inches(9.0), Inches(3.8), font_size=13.5)

    # ── SLIDE 12: Thank You ────────────────────────────────────────────────────
    slide12 = prs.slides.add_slide(slide_layout)
    add_slide_background(slide12, BG_COLOR)
    
    title_box12 = slide12.shapes.add_textbox(Inches(0.5), Inches(1.5), Inches(9.0), Inches(1.5))
    tf12 = title_box12.text_frame
    p12 = tf12.paragraphs[0]
    p12.text = "THANK YOU"
    p12.font.name = "Arial"
    p12.font.size = Pt(44)
    p12.font.bold = True
    p12.font.color.rgb = ACCENT_INDIGO
    p12.alignment = PP_ALIGN.CENTER
    
    p12_sub = tf12.add_paragraph()
    p12_sub.text = "Bluestock Mutual Fund Analytics Terminal — Capstone Project Complete"
    p12_sub.font.name = "Arial"
    p12_sub.font.size = Pt(16)
    p12_sub.font.color.rgb = TEXT_WHITE
    p12_sub.alignment = PP_ALIGN.CENTER
    p12_sub.space_before = Pt(10)
    
    meta12 = slide12.shapes.add_textbox(Inches(0.5), Inches(3.5), Inches(9.0), Inches(1.0))
    tf_m12 = meta12.text_frame
    p_m12 = tf_m12.paragraphs[0]
    p_m12.text = "GitHub Repository: https://github.com/samyukthamenon28/bluestock_mf_capstone\nExecutable Tag: v1.0  |  Dashboard Port: http://localhost:8501"
    p_m12.font.name = "Arial"
    p_m12.font.size = Pt(11)
    p_m12.font.color.rgb = TEXT_GRAY
    p_m12.alignment = PP_ALIGN.CENTER
    
    # Save Presentation
    prs.save(PPTX_OUT)
    print("PowerPoint presentation build complete!")


if __name__ == "__main__":
    build_presentation()

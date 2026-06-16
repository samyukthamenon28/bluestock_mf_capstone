"""
generate_pptx_presentation.py — Bluestock MF Capstone: 12-Slide PowerPoint Builder (python-pptx)
Compiles a 12-slide presentation with advanced text-run parsing. Key terms surrounded
by double asterisks (**) are formatted as bold and colored in Indigo accent.
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
PPTX_OUT = ROOT / "reports" / "Bluestock_Presentation_Final.pptx"

# Ensure reports directory exists
PPTX_OUT.parent.mkdir(parents=True, exist_ok=True)

# ── Slide Color Constants ──────────────────────────────────────────────────────
BG_COLOR = RGBColor(15, 23, 42)        # Dark Slate / Navy (0f172a)
TEXT_WHITE = RGBColor(255, 255, 255)   # White
TEXT_GRAY = RGBColor(148, 163, 184)    # Cool Gray (94a6b8)
ACCENT_INDIGO = RGBColor(129, 140, 248) # Neon Indigo/Lavender (818cf8)


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


def add_bullet_points(slide, points, left, top, width, height, font_size=14):
    """Add a bullet point text frame on the slide with bold run parsing."""
    txBox = slide.shapes.add_textbox(left, top, width, height)
    tf = txBox.text_frame
    tf.word_wrap = True
    
    for idx, pt in enumerate(points):
        if idx == 0:
            p = tf.paragraphs[0]
        else:
            p = tf.add_paragraph()
            
        p.space_after = Pt(6)
        
        # Determine bullet level
        level = 0
        text_content = pt
        if pt.startswith("• "):
            text_content = pt[2:]
            level = 0
        elif pt.startswith("  - "):
            text_content = pt[4:]
            level = 1
            
        p.level = level
        
        # Parse bold tags **
        parts = text_content.split("**")
        # Every odd index in parts represents bold text
        for part_idx, part in enumerate(parts):
            run = p.add_run()
            run.text = part
            run.font.name = "Arial"
            run.font.size = Pt(font_size)
            if part_idx % 2 == 1:
                run.font.bold = True
                run.font.color.rgb = ACCENT_INDIGO
            else:
                run.font.bold = False
                run.font.color.rgb = TEXT_WHITE
                
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
        "• **Holiday Price Distortion**: Missing holiday NAV prices can skew standard deviation and return calculations if holiday periods are not handled.",
        "• **Analytics Gap**: Standard retail platforms do not calculate tail-risk parameters (VaR/CVaR) or support dynamic asset optimization model simulations.",
        "• **Capstone Project Objectives**:",
        "  - **ETL Ingestion Engine**: Build a fully automated E2E pipeline fetching live NAV from mfapi.in and loading SQLite database tables.",
        "  - **Relational Schema**: Design a SQLite star schema layout to cleanly query NAV histories and investor demographics.",
        "  - **Performance Scorecards**: Compute CAGRs, Sharpe, Sortino, Jensen's Alpha, and Beta parameters.",
        "  - **Advanced Risk Dashboards**: Integrate investor cohorts, continuity risk, and sector allocations into interactive workspaces."
    ]
    add_bullet_points(slide2, points2, Inches(0.5), Inches(1.3), Inches(9.0), Inches(3.8))

    # ── SLIDE 3: Data Sources ──────────────────────────────────────────────────
    slide3 = prs.slides.add_slide(slide_layout)
    add_slide_background(slide3, BG_COLOR)
    add_slide_header(slide3, "Data Sources & Dimensions")
    
    points3 = [
        "• **Ingested Datasets**: The relational database processes 10 raw CSV datasets representing mid-2022 to mid-2026:",
        "  - **Fund Registration**: Fund Master (40 schemes) and Scheme Performance lists.",
        "  - **Daily Valuations**: NAV History (64,354 rows) and daily index prices for Nifty 50 and Nifty 100 (8,050 rows).",
        "  - **Asset Allocation**: Portfolio Holdings weights detailing 322 stock allocations.",
        "  - **Investor Attributes**: Investor Transactions (32,778 rows) containing demographic profiles.",
        "  - **Industry Aggregates**: AMC AUM, monthly SIP inflows, category flows, and folio counts.",
        "• **Star Schema Dimensions**:",
        "  - **dim_fund** (AMFI code primary key) and **dim_date** (date_id primary key) act as dimensions.",
        "  - **fact_nav**, **fact_transactions**, **fact_performance**, and **fact_aum** act as facts."
    ]
    add_bullet_points(slide3, points3, Inches(0.5), Inches(1.3), Inches(9.0), Inches(3.8))

    # ── SLIDE 4: Architecture ──────────────────────────────────────────────────
    slide4 = prs.slides.add_slide(slide_layout)
    add_slide_background(slide4, BG_COLOR)
    add_slide_header(slide4, "ETL Pipeline & Ingestion Design")
    
    points4 = [
        "• **Extraction Component**: Standardized requests query mfapi.in API with exponential backoff retries to handle rate limits.",
        "• **Holiday Forward-Filling Rule**:",
        "  - Timeline is reindexed to a full calendar. Missing weekend and holiday NAVs are forward-filled.",
        "  - Prevents standard deviation damping. Daily returns are calculated strictly on business days (Mon-Fri).",
        "• **Annualization Standards**:",
        "  - Ratios, variances, and compounding CAGRs are annualized utilizing a **252-day business year**.",
        "• **SQL Loading**: Ingestion is processed via SQLAlchemy engine, enforcing primary/foreign key relations.",
        "  - Database indices optimize queries on dates, AMFI codes, and transaction references."
    ]
    add_bullet_points(slide4, points4, Inches(0.5), Inches(1.3), Inches(9.0), Inches(3.8))

    # ── SLIDE 5: EDA Highlights (1) ────────────────────────────────────────────
    slide5 = prs.slides.add_slide(slide_layout)
    add_slide_background(slide5, BG_COLOR)
    add_slide_header(slide5, "EDA Highlights: Macro Industry Growth")
    
    points5 = [
        "• **NAV and AUM Growth**: Valuation trends show consistent performance, with large-cap funds leading in assets.",
        "• **2023 Bull Run**: Sustained market rally of 2023 is clearly visible across all equity sub-categories.",
        "• **Monthly SIP Inflows**: Monthly contributions show strong upward momentum,",
        "  proving retail systematic investment discipline continues regardless of short-term drops.",
        "• **Folio Registrations**: Total folio accounts in India grew steadily, illustrating capital flow migration from savings accounts to mutual funds.",
        "• **Sector Exposures**: Financial Services, Technology, Energy, and Consumer Staples represent the largest allocations across equity holdings."
    ]
    add_bullet_points(slide5, points5, Inches(0.5), Inches(1.3), Inches(9.0), Inches(3.8))

    # ── SLIDE 6: EDA Highlights (2) ────────────────────────────────────────────
    slide6 = prs.slides.add_slide(slide_layout)
    add_slide_background(slide6, BG_COLOR)
    add_slide_header(slide6, "EDA Highlights: Investor Demographics")
    
    points6 = [
        "• **Age Concentrations**: Over 65% of the transaction volume is driven by the **26-35** and **36-45** age brackets,",
        "  confirming mutual fund popularity among young professionals.",
        "• **Transaction Size by Age**: Boxplot analysis shows older brackets (46-55, 56+) maintain a wider spread",
        "  and higher median transaction size, reflecting accumulated wealth.",
        "• **Geographical Volume**: The largest contribution volumes originate from Maharashtra and Gujarat.",
        "• **City Tier Contribution Split (T30 vs B30)**:",
        "  - **Top 30 (T30) Cities** represent the majority of absolute asset volume.",
        "  - **Beyond 30 (B30) Cities** show rapid, compounding growth in new account registrations,",
        "    highlighting successful geographical market expansion."
    ]
    add_bullet_points(slide6, points6, Inches(0.5), Inches(1.3), Inches(9.0), Inches(3.8))

    # ── SLIDE 7: Performance Metrics (1) ───────────────────────────────────────
    slide7 = prs.slides.add_slide(slide_layout)
    add_slide_background(slide7, BG_COLOR)
    add_slide_header(slide7, "Performance scorecards & leaderboards")
    
    points7 = [
        "• **Scorecard Metrics**: Performance is evaluated over a 3-year history utilizing daily returns.",
        "• **Risk-Adjusted Ratios**:",
        "  - **Sharpe Ratio**: Measures excess return per unit of volatility (risk-free rate = 6.5%).",
        "  - **Sortino Ratio**: Adjusts return for downside deviation only, ignoring upside volatility.",
        "• **Regression Coefficients (Alpha & Beta)**:",
        "  - Calculated via Ordinary Least Squares (OLS) regression against the Nifty 100 benchmark index.",
        "  - Estimates systematic risk (Beta) and excess manager returns (Alpha).",
        "• **Weighted Composite Score**:",
        "  - Sharpe (30%), Sortino (20%), 3-Year CAGR (30%), and Max Drawdown (20%)."
    ]
    add_bullet_points(slide7, points7, Inches(0.5), Inches(1.3), Inches(9.0), Inches(3.8))

    # ── SLIDE 8: Performance Metrics (2) ───────────────────────────────────────
    slide8 = prs.slides.add_slide(slide_layout)
    add_slide_background(slide8, BG_COLOR)
    add_slide_header(slide8, "Top Performing Funds Leaderboard")
    
    points8 = [
        "• **Top Large Cap Schemes (Sorted by Composite Score)**:",
        "  - **HDFC Top 100 Direct - Growth (AMFI: 125497)**: Highest composite score, driven by stable Sharpe and Sortino ratios.",
        "  - **SBI Bluechip Fund - Direct - Growth (AMFI: 119551)**: Lowest Beta (0.87), providing steady defensive performance.",
        "  - **ICICI Prudential Bluechip - Direct - Growth (AMFI: 120503)**: Consistent outperformance.",
        "  - **Nippon India Large Cap - Direct - Growth (AMFI: 118632)**: Strong alpha creation.",
        "  - **Axis Bluechip Fund - Direct - Growth (AMFI: 119092)**: High technology allocation.",
        "• **Benchmark Outperformance**: Top schemes generated positive annual alpha (1.5% to 3.2%) and outperformed the Nifty 50 and Nifty 100 indices over the 3-year window."
    ]
    add_bullet_points(slide8, points8, Inches(0.5), Inches(1.3), Inches(9.0), Inches(3.8))

    # ── SLIDE 9: Dashboard Screenshots (1) ─────────────────────────────────────
    slide9 = prs.slides.add_slide(slide_layout)
    add_slide_background(slide9, BG_COLOR)
    add_slide_header(slide9, "Dashboard Design & Core Workspaces")
    
    points9 = [
        "• **Interactive Dashboard**: Built using Streamlit, styled as a custom cyber-dark financial terminal.",
        "• **Slicer & Filter Controls**: Features Category, Fund House, and Date widgets on every page.",
        "• **Dashboard Workspaces (Pages 1 - 3)**:",
        "  - **Page 1: Fund Scorecard & Benchmark** - Displays composite scorecard leaderboards, benchmark comparison trends, and tracking error metrics.",
        "  - **Page 2: NAV Analysis & Correlation** - Compares historical NAV trends, return distribution histograms, and OLS linear return correlation matrices.",
        "  - **Page 3: Industry & AUM Growth** - Visualizes total folio growth, AMC market share, and monthly industry inflows."
    ]
    add_bullet_points(slide9, points9, Inches(0.5), Inches(1.3), Inches(9.0), Inches(3.8))

    # ── SLIDE 10: Dashboard Screenshots (2) ────────────────────────────────────
    slide10 = prs.slides.add_slide(slide_layout)
    add_slide_background(slide10, BG_COLOR)
    add_slide_header(slide10, "Dashboard: Simulation & Risk Workspace")
    
    points10 = [
        "• **Dashboard Workspaces (Pages 4 - 6)**:",
        "  - **Page 4: Investor Demographics** - Tracks transaction volumes by age, gender, state, and city tier.",
        "  - **Page 5: Advanced Simulation & Optimization** - Runs 5-year Monte Carlo growth projections using Geometric Brownian Motion (GBM) and generates the Markowitz Efficient Frontier to compute optimal portfolio weights.",
        "  - **Page 6: Advanced Risk & Cohort Analytics** - Integrates tail-risk metrics (VaR & CVaR), rolling Sharpe ratio timelines, yearly cohort tables, and Sector HHI concentration bars.",
        "• **Premium Visual Theme**: Custom dark theme with neon borders, designed without unnecessary emojis to maintain a professional look."
    ]
    add_bullet_points(slide10, points10, Inches(0.5), Inches(1.3), Inches(9.0), Inches(3.8))

    # ── SLIDE 11: Key Findings ────────────────────────────────────────────────
    slide11 = prs.slides.add_slide(slide_layout)
    add_slide_background(slide11, BG_COLOR)
    add_slide_header(slide11, "Key Findings & Recommendations")
    
    points11 = [
        "• **Value at Risk (95% Daily VaR)**: Small-cap schemes show daily VaR loss risk of **-2.63%** (CVaR of **-3.68%**). Liquid funds demonstrate **0.00%** daily VaR.",
        "• **SIP Continuity Risks**: Out of 1,362 eligible long-term investors (6+ transactions), over **97.80% (1,332)** are flagged as 'at-risk' due to transaction gaps exceeding 35 days.",
        "• **HHI Sector Concentration**: Axis Bluechip is the most concentrated (HHI: 2967.69), while UTI Mid Cap is the most diversified (HHI: 1240.20).",
        "• **Strategic Recommendations**:",
        "  - **UPI Retention Alerts**: Implement automated notification systems 28 days after an investor's last SIP transaction to prevent missed payments.",
        "  - **Standardize Holiday Handling**: Standardize holiday ffill() across all analytics teams to prevent index return distortions."
    ]
    add_bullet_points(slide11, points11, Inches(0.5), Inches(1.3), Inches(9.0), Inches(3.8), font_size=13)

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

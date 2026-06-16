"""
create_docx.py — Programmatically generate a valid DOCX file for the Demo Video guide
using only Python's standard zipfile library (no python-docx dependency).
"""

import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT_PATH = ROOT / "Samyuktha_MF_Capstone_Submission" / "Demo Video" / "Demo_Video_Guide.docx"

CONTENT_TYPES_XML = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
</Types>
"""

RELS_XML = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
</Relationships>
"""

DOCUMENT_XML = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:body>
    <w:p>
      <w:pPr>
        <w:pStyle w:val="Heading1"/>
      </w:pPr>
      <w:r>
        <w:rPr>
          <w:b/>
          <w:sz w:val="28"/>
        </w:rPr>
        <w:t>BLUESTOCK MUTUAL FUND TERMINAL - DEMO VIDEO GUIDE</w:t>
      </w:r>
    </w:p>
    <w:p/>
    <w:p>
      <w:r>
        <w:t>Reviewers can launch the Streamlit quantitative financial terminal locally to test the features and interact with all workspaces. Please follow these setup steps:</w:t>
      </w:r>
    </w:p>
    <w:p/>
    <w:p>
      <w:r>
        <w:rPr><w:b/></w:rPr>
        <w:t>Step 1: Install Package Dependencies</w:t>
      </w:r>
    </w:p>
    <w:p>
      <w:r>
        <w:t>Open your terminal and run: pip install -r requirements.txt</w:t>
      </w:r>
    </w:p>
    <w:p/>
    <w:p>
      <w:r>
        <w:rPr><w:b/></w:rPr>
        <w:t>Step 2: Run Ingestion &amp; Scorecard Analytics Pipeline</w:t>
      </w:r>
    </w:p>
    <w:p>
      <w:r>
        <w:t>Compile all database tables, scores, and PDF reports by running: python scripts/run_pipeline.py</w:t>
      </w:r>
    </w:p>
    <w:p/>
    <w:p>
      <w:r>
        <w:rPr><w:b/></w:rPr>
        <w:t>Step 3: Launch Streamlit Dashboard App</w:t>
      </w:r>
    </w:p>
    <w:p>
      <w:r>
        <w:t>Execute: streamlit run dashboard/app.py</w:t>
      </w:r>
    </w:p>
    <w:p>
      <w:r>
        <w:t>This will host the dashboard at http://localhost:8501</w:t>
      </w:r>
    </w:p>
    <w:p/>
    <w:p>
      <w:r>
        <w:rPr><w:b/></w:rPr>
        <w:t>Alternative (CLI Recommender):</w:t>
      </w:r>
    </w:p>
    <w:p>
      <w:r>
        <w:t>You can also query the OLS-based Sharpe recommender from the terminal: python recommender.py --risk Moderate</w:t>
      </w:r>
    </w:p>
  </w:body>
</w:document>
"""


def main():
    print(f"Creating docx file at: {OUT_PATH}")
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    
    with zipfile.ZipFile(OUT_PATH, "w", zipfile.ZIP_DEFLATED) as docx:
        docx.writestr("[Content_Types].xml", CONTENT_TYPES_XML)
        docx.writestr("_rels/.rels", RELS_XML)
        docx.writestr("word/document.xml", DOCUMENT_XML)
        
    print("DOCX file compiled successfully!")


if __name__ == "__main__":
    main()

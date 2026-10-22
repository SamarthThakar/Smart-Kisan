import os
import sys
import subprocess

# Ensure scripts dir is on sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from doc_styles import get_css
from doc_content_part1 import get_cover_html, get_section1_html, get_section2_html
from doc_content_part2 import get_section3_html, get_section4_html
from doc_content_part3 import get_section5_html, get_section6_html
from doc_content_part4 import get_section7_html, get_section8_html, get_section9_html, get_section10_html

def build_html():
    css = get_css()
    cover = get_cover_html()
    s1 = get_section1_html()
    s2 = get_section2_html()
    s3 = get_section3_html()
    s4 = get_section4_html()
    s5 = get_section5_html()
    s6 = get_section6_html()
    s7 = get_section7_html()
    s8 = get_section8_html()
    s9 = get_section9_html()
    s10 = get_section10_html()
    
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Smart Kisan - Complete Technical Project Documentation</title>
<style>
{css}
</style>
</head>
<body>
{cover}
<div class="content-wrap">
{s1}
{s2}
{s3}
{s4}
{s5}
{s6}
{s7}
{s8}
{s9}
{s10}
</div>
</body>
</html>
"""
    return html

def main():
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    docs_dir = os.path.join(root_dir, "docs")
    os.makedirs(docs_dir, exist_ok=True)
    
    html_path = os.path.join(docs_dir, "Smart_Kisan_Complete_Project_Documentation.html")
    pdf_path = os.path.join(docs_dir, "Smart_Kisan_Complete_Project_Documentation.pdf")
    
    html_content = build_html()
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"[OK] Wrote HTML documentation: {html_path} ({len(html_content):,} bytes)")
    
    chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
    browser_exe = chrome_path if os.path.exists(chrome_path) else edge_path
    
    if not os.path.exists(browser_exe):
        print("[ERROR] Neither Chrome nor Edge executable found!")
        return 1
        
    print(f"[*] Compiling PDF using: {browser_exe}")
    file_uri = f"file:///{html_path.replace(os.sep, '/')}"
    cmd = [
        browser_exe,
        "--headless=new",
        "--disable-gpu",
        "--no-pdf-header-footer",
        "--run-all-compositor-stages-before-draw",
        f"--print-to-pdf={pdf_path}",
        file_uri
    ]
    
    res = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
    if os.path.exists(pdf_path):
        size_kb = os.path.getsize(pdf_path) / 1024
        print(f"[SUCCESS] PDF generated successfully: {pdf_path} ({size_kb:.1f} KB)")
        return 0
    else:
        print("[ERROR] PDF generation failed!")
        print("Stdout:", res.stdout)
        print("Stderr:", res.stderr)
        return 1

if __name__ == "__main__":
    sys.exit(main())

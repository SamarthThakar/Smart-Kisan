import os
import sys
import subprocess

def get_css():
    return """
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Fira+Code:wght@400;500;600&display=swap');
    
    :root {
        --primary: #15803d;
        --primary-dark: #14532d;
        --primary-light: #22c55e;
        --primary-subtle: #f0fdf4;
        --secondary: #d97706;
        --secondary-light: #fef3c7;
        --accent: #2563eb;
        --accent-light: #eff6ff;
        --danger: #dc2626;
        --danger-light: #fef2f2;
        --neutral-900: #0f172a;
        --neutral-800: #1e293b;
        --neutral-700: #334155;
        --neutral-600: #475569;
        --neutral-500: #64748b;
        --neutral-300: #cbd5e1;
        --neutral-200: #e2e8f0;
        --neutral-100: #f1f5f9;
        --neutral-50: #f8fafc;
        --white: #ffffff;
    }
    
    * {
        box-sizing: border-box;
        margin: 0;
        padding: 0;
    }
    
    @page {
        size: A4 portrait;
        margin: 14mm 14mm 16mm 14mm;
        @bottom-right {
            content: counter(page);
            font-family: 'Plus Jakarta Sans', sans-serif;
            font-size: 8pt;
            color: var(--neutral-500);
        }
    }
    
    body {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        color: var(--neutral-800);
        background: #ffffff;
        font-size: 9.5pt;
        line-height: 1.55;
        -webkit-print-color-adjust: exact;
        print-color-adjust: exact;
    }
    
    .page-break {
        page-break-before: always;
        break-before: page;
    }
    
    .avoid-break {
        page-break-inside: avoid;
        break-inside: avoid;
    }
    
    /* Cover Page */
    .cover-container {
        height: 100vh;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        background: linear-gradient(145deg, #0f391e 0%, #14532d 40%, #166534 80%, #1e3a8a 100%);
        color: #ffffff;
        padding: 60px 50px;
        border-radius: 12px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.15);
        margin-bottom: 20px;
    }
    
    .cover-badge {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.3);
        padding: 6px 16px;
        border-radius: 30px;
        font-size: 9pt;
        font-weight: 600;
        letter-spacing: 0.8px;
        text-transform: uppercase;
        width: fit-content;
    }
    
    .cover-title-group h1 {
        font-size: 42pt;
        font-weight: 800;
        line-height: 1.1;
        letter-spacing: -1px;
        margin-top: 25px;
        margin-bottom: 15px;
    }
    
    .cover-title-group h1 span {
        color: #86efac;
        background: linear-gradient(90deg, #86efac, #fde047);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .cover-tagline {
        font-size: 15pt;
        font-weight: 400;
        opacity: 0.92;
        max-width: 650px;
        line-height: 1.45;
        margin-bottom: 30px;
    }
    
    .cover-features-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 12px;
        margin: 30px 0;
    }
    
    .cover-feature-pill {
        background: rgba(255, 255, 255, 0.12);
        border: 1px solid rgba(255, 255, 255, 0.2);
        padding: 10px 14px;
        border-radius: 8px;
        font-size: 8.5pt;
        font-weight: 500;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    
    .cover-meta {
        border-top: 1px solid rgba(255, 255, 255, 0.25);
        padding-top: 25px;
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 20px;
    }
    
    .cover-meta-item .label {
        font-size: 7.5pt;
        text-transform: uppercase;
        letter-spacing: 1px;
        opacity: 0.7;
    }
    
    .cover-meta-item .val {
        font-size: 10.5pt;
        font-weight: 700;
        margin-top: 4px;
    }
    
    /* Layout and Content */
    .content-wrap {
        padding: 10px 5px;
    }
    
    .header-bar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-bottom: 2px solid var(--neutral-200);
        padding-bottom: 10px;
        margin-bottom: 22px;
    }
    
    .header-bar .doc-tag {
        font-size: 8pt;
        font-weight: 700;
        text-transform: uppercase;
        color: var(--primary);
        letter-spacing: 1px;
    }
    
    .header-bar .doc-version {
        font-size: 8pt;
        color: var(--neutral-500);
    }
    
    h2.section-heading {
        font-size: 16pt;
        font-weight: 800;
        color: var(--primary-dark);
        border-bottom: 2px solid var(--primary-light);
        padding-bottom: 6px;
        margin-top: 26px;
        margin-bottom: 14px;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    
    h2.section-heading .sec-num {
        background: var(--primary-dark);
        color: #ffffff;
        font-size: 10pt;
        font-weight: 800;
        width: 26px;
        height: 26px;
        border-radius: 6px;
        display: inline-flex;
        align-items: center;
        justify-content: center;
    }
    
    h3 {
        font-size: 11.5pt;
        font-weight: 700;
        color: var(--neutral-900);
        margin-top: 18px;
        margin-bottom: 8px;
    }
    
    h4 {
        font-size: 9.5pt;
        font-weight: 700;
        color: var(--neutral-700);
        margin-top: 12px;
        margin-bottom: 6px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    p {
        margin-bottom: 10px;
        color: var(--neutral-700);
    }
    
    ul, ol {
        margin-left: 20px;
        margin-bottom: 12px;
    }
    
    li {
        margin-bottom: 4px;
        color: var(--neutral-700);
    }
    
    strong {
        color: var(--neutral-900);
        font-weight: 600;
    }
    
    /* Code and Terminal Blocks */
    code {
        font-family: 'Fira Code', monospace;
        font-size: 8pt;
        background: var(--neutral-100);
        color: var(--primary-dark);
        padding: 2px 5px;
        border-radius: 4px;
        border: 1px solid var(--neutral-200);
    }
    
    pre {
        background: #0f172a;
        color: #e2e8f0;
        font-family: 'Fira Code', monospace;
        font-size: 7.8pt;
        line-height: 1.5;
        padding: 14px 16px;
        border-radius: 8px;
        overflow-x: auto;
        margin: 10px 0 14px 0;
        border: 1px solid #1e293b;
    }
    
    .pre-tag {
        display: inline-block;
        background: #334155;
        color: #cbd5e1;
        font-family: 'Fira Code', monospace;
        font-size: 7pt;
        padding: 2px 8px;
        border-radius: 4px 4px 0 0;
        margin-bottom: -1px;
    }
    
    /* Tables */
    table {
        width: 100%;
        border-collapse: collapse;
        margin: 12px 0 16px 0;
        font-size: 8.5pt;
    }
    
    th {
        background: var(--primary-dark);
        color: #ffffff;
        text-align: left;
        padding: 8px 10px;
        font-weight: 600;
        font-size: 8pt;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    td {
        padding: 7px 10px;
        border-bottom: 1px solid var(--neutral-200);
        vertical-align: top;
    }
    
    tr:nth-child(even) td {
        background: var(--neutral-50);
    }
    
    /* Cards and Grids */
    .grid-2 {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 12px;
        margin: 10px 0 14px 0;
    }
    
    .grid-3 {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 10px;
        margin: 10px 0 14px 0;
    }
    
    .card {
        background: #ffffff;
        border: 1px solid var(--neutral-200);
        border-radius: 8px;
        padding: 14px 16px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.03);
    }
    
    .card.highlight {
        border-left: 4px solid var(--primary);
        background: var(--primary-subtle);
    }
    
    .card.alert {
        border-left: 4px solid var(--secondary);
        background: var(--secondary-light);
    }
    
    .card.info {
        border-left: 4px solid var(--accent);
        background: var(--accent-light);
    }
    
    .stat-box {
        text-align: center;
        padding: 12px;
        background: var(--neutral-50);
        border: 1px solid var(--neutral-200);
        border-radius: 8px;
    }
    
    .stat-number {
        font-size: 20pt;
        font-weight: 800;
        color: var(--primary);
        line-height: 1;
    }
    
    .stat-label {
        font-size: 7.5pt;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        color: var(--neutral-600);
        margin-top: 4px;
    }
    
    /* Badges */
    .badge {
        display: inline-block;
        font-size: 7pt;
        font-weight: 700;
        padding: 2px 7px;
        border-radius: 12px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .badge-green { background: #dcfce7; color: #15803d; }
    .badge-blue { background: #dbeafe; color: #1d4ed8; }
    .badge-amber { background: #fef3c7; color: #b45309; }
    .badge-red { background: #fee2e2; color: #b91c1c; }
    
    /* Endpoints */
    .api-endpoint {
        background: var(--neutral-900);
        color: #ffffff;
        padding: 8px 12px;
        border-radius: 6px;
        font-family: 'Fira Code', monospace;
        font-size: 8pt;
        display: flex;
        align-items: center;
        gap: 10px;
        margin: 6px 0;
    }
    
    .method-badge {
        padding: 2px 7px;
        border-radius: 4px;
        font-size: 7pt;
        font-weight: 800;
    }
    .method-get { background: #16a34a; color: white; }
    .method-post { background: #2563eb; color: white; }
    .method-put { background: #d97706; color: white; }
    .method-delete { background: #dc2626; color: white; }
    
    .endpoint-path {
        color: #7dd3fc;
        font-weight: 600;
        flex: 1;
    }
    
    .endpoint-desc {
        color: #94a3b8;
        font-size: 7.5pt;
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    /* Footer */
    .doc-footer {
        margin-top: 30px;
        border-top: 1px solid var(--neutral-200);
        padding-top: 15px;
        text-align: center;
        font-size: 8pt;
        color: var(--neutral-500);
    }
    """

def get_cover_html():
    return """
    <div class="cover-container">
        <div>
            <div class="cover-badge">🌱 Comprehensive Technical Architecture & Project Guide</div>
            <div class="cover-title-group">
                <h1>Smart<span>Kisan</span></h1>
                <div class="cover-tagline">
                    An AI-Powered Agricultural Advisory Platform for Indian Farmers — Combining Deep Learning Computer Vision, Agronomic Recommendation Engines, Real-Time Mandi Intelligence, and Multilingual Generative AI.
                </div>
            </div>
            
            <div class="cover-features-grid">
                <div class="cover-feature-pill">🍃 EfficientNetB3 Disease Detection</div>
                <div class="cover-feature-pill">🌱 Random Forest Crop Recommendation</div>
                <div class="cover-feature-pill">☀️ Open-Meteo Weather Advisory</div>
                <div class="cover-feature-pill">📊 APMC Mandi Price Intelligence</div>
                <div class="cover-feature-pill">🏛️ National Schemes Directory</div>
                <div class="cover-feature-pill">🤖 Gemini 1.5 Flash Multilingual RAG</div>
            </div>
        </div>
        
        <div class="cover-meta">
            <div class="cover-meta-item">
                <div class="label">Backend Architecture</div>
                <div class="val">FastAPI + Python 3.13</div>
            </div>
            <div class="cover-meta-item">
                <div class="label">Frontend Stack</div>
                <div class="val">React 19 + Vite</div>
            </div>
            <div class="cover-meta-item">
                <div class="label">Database Layer</div>
                <div class="val">SQLAlchemy + SQLite / PostgreSQL</div>
            </div>
            <div class="cover-meta-item">
                <div class="label">Languages Supported</div>
                <div class="val">English, Hindi, Marathi</div>
            </div>
        </div>
    </div>
    """

def get_section1_html():
    return """
    <div class="page-break"></div>
    <div class="header-bar">
        <span class="doc-tag">Smart Kisan Project Guide</span>
        <span class="doc-version">Section 1 &bull; Overview & Mission</span>
    </div>

    <h2 class="section-heading"><span class="sec-num">1</span> Project Overview & Core Mission</h2>
    
    <p><strong>Smart Kisan</strong> ("Smart Farmer") is an end-to-end, full-stack, artificial intelligence-powered agricultural advisory platform created specifically to address the structural technology divide in Indian agriculture. Over 140 million farming households in India face recurring agricultural and economic vulnerabilities due to five fundamental challenges:</p>

    <div class="grid-2">
        <div class="card alert">
            <h4>1. Asymmetric Crop Health Information</h4>
            <p>Farmers often fail to diagnose fungal and bacterial leaf diseases until irreversible damage occurs. Agricultural extension officers (Krishi Vigyan Kendras) are understaffed and geographically distant from remote villages.</p>
        </div>
        <div class="card alert">
            <h4>2. Suboptimal Crop Selection</h4>
            <p>Sowing choices are frequently based on tradition or speculative market hype rather than objective soil chemistry (Nitrogen, Phosphorus, Potassium, pH) and seasonal meteorological forecasts.</p>
        </div>
        <div class="card alert">
            <h4>3. Market Mandi Price Exploitation</h4>
            <p>Middlemen (arhtiyas) leverage price opacity in regional Agricultural Produce Market Committees (APMCs) to purchase farmer harvests well below prevailing modal market rates.</p>
        </div>
        <div class="card alert">
            <h4>4. Underutilization of Government Welfare</h4>
            <p>Billions of rupees allocated under PM-KISAN, PMFBY (Crop Insurance), and Kisan Credit Card (KCC) remain unclaimed because eligibility rules are buried in complex government portals.</p>
        </div>
    </div>

    <div class="card highlight">
        <h4>The Smart Kisan Solution</h4>
        <p>Smart Kisan consolidates six distinct agricultural domains into a single, high-performance, mobile-first web ecosystem accessible across desktop, tablet, and smartphone browsers in the farmer's native tongue (English, Hindi, and Marathi):</p>
        <ul style="margin-bottom:0;">
            <li><strong>Instant Leaf Disease Diagnosis:</strong> Point-and-shoot computer vision diagnostics delivering actionable chemical treatments, preventative measures, and KVK contact recommendations within seconds.</li>
            <li><strong>Agronomic Crop Advisor:</strong> Scientific crop recommendations matching exact soil nutrient parameters (NPK, pH) and micro-climate inputs with regional soil presets.</li>
            <li><strong>Real-time Mandi Intelligence:</strong> Transparent pricing across major Indian markets with automatic "Best Mandi" profit optimization highlights.</li>
            <li><strong>Precision Meteorological Alerts:</strong> 7-day hyperlocal forecast paired with rule-based operational advisories (foliar spray timing, rain shelter alerts).</li>
            <li><strong>National Welfare Directory:</strong> Searchable repository of subsidies, loans, and insurance schemes with direct application pathways.</li>
            <li><strong>Conversational Krishi Mitra AI:</strong> 24/7 multilingual agronomic intelligence grounded in ICAR research through Retrieval-Augmented Generation (RAG).</li>
        </ul>
    </div>

    <div class="grid-3" style="margin-top:15px;">
        <div class="stat-box">
            <div class="stat-number">7</div>
            <div class="stat-label">Production Modules</div>
        </div>
        <div class="stat-box">
            <div class="stat-number">38+</div>
            <div class="stat-label">Crop Disease Classes</div>
        </div>
        <div class="stat-box">
            <div class="stat-number">22</div>
            <div class="stat-label">Analyzed Crop Varieties</div>
        </div>
    </div>
    """

def get_section2_html():
    return """
    <div class="page-break"></div>
    <div class="header-bar">
        <span class="doc-tag">Smart Kisan Project Guide</span>
        <span class="doc-version">Section 2 &bull; Architecture & Data Flow</span>
    </div>

    <h2 class="section-heading"><span class="sec-num">2</span> System Architecture & Data Flow</h2>
    
    <p>Smart Kisan adheres to a modern, decoupled 3-tier web architecture engineered for speed, resilience, and offline accessibility:</p>

    <div class="pre-tag">System Architecture Diagram</div>
    <pre>
===================================================================================
                       SMART KISAN SYSTEM ARCHITECTURE
===================================================================================

  [ CLIENT TIER : Web & Mobile Browser (localhost:5173) ]
  React 19 + Vite + React Router v7 + Vanilla CSS Design System + i18next
  +-------------------+ +--------------------+ +---------------------+
  | Home & Weather    | | Leaf Disease Doctor| | Crop Advisor        |
  +-------------------+ +--------------------+ +---------------------+
  | Mandi Prices      | | Government Schemes | | Krishi Mitra AI Chat|
  +-------------------+ +--------------------+ +---------------------+
  State Layer: AuthContext (JWT + Guest Mode) | api.js (Axios Client + Bearer Auth)
                          |
                          | HTTP REST (JSON / Multipart Form-Data)
                          v
  [ APPLICATION TIER : FastAPI on Uvicorn ASGI (localhost:8000) ]
  Middleware Layer: CORS Whitelist | SlowAPI Rate Limiter | JWT Bearer Validator
  +-------------------------------------------------------------------------------+
  | Routers: /auth  /predict  /recommend  /weather  /market  /schemes  /chat     |
  +-------------------------------------------------------------------------------+
  | ML Inference Layer:                                                           |
  |  - EfficientNetB3 (TensorFlow Keras) -> Leaf Disease Classification           |
  |  - Random Forest (Scikit-Learn)      -> Soil & Climate Crop Recommendation    |
  |  - Gemini 1.5 Flash + ChromaDB       -> Multilingual Retrieval-Augmented Gen  |
  |  - Rule Engine (weather_rules.py)    -> Farming Advisory Alert Synthesis      |
  +-------------------------------------------------------------------------------+
  | Data Access Layer: SQLAlchemy 2.0 ORM + Pydantic v2 Schema Validation         |
  +-------------------------------------------------------------------------------+
                          |
                          | SQL / File System / Vector Index / External REST
                          v
  [ PERSISTENCE & EXTERNAL SERVICES TIER ]
  +-----------------------+ +-----------------------+ +---------------------------+
  | SQLite (smart_kisan.db)| | Leaf Uploads Storage  | | ChromaDB Vector Store     |
  | or PostgreSQL (Prod)  | | (/uploads directory)  | | (/models/chroma_db)       |
  +-----------------------+ +-----------------------+ +---------------------------+
  | Open-Meteo API        | | data.gov.in API       | | Google Gemini API         |
  | (Zero-Key Weather)    | | (APMC Mandi Rates)    | | (Generative AI Engine)    |
  +-----------------------+ +-----------------------+ +---------------------------+
===================================================================================
    </pre>

    <h3>Request Lifecycle & Execution Flow</h3>
    <ol>
        <li><strong>Client Dispatch:</strong> The user interacts with the UI. The frontend service module (<code>frontend/src/services/api.js</code>) intercepts the request and automatically attaches the JWT bearer token from <code>localStorage</code> if present.</li>
        <li><strong>Reverse Proxy / CORS:</strong> In development, the Vite server proxies API calls from port 5173 to port 8000. In production, FastAPI's CORS middleware ensures only authorized domains can access backend endpoints.</li>
        <li><strong>Security & Rate Limiting:</strong> SlowAPI inspects the client IP address. High-compute endpoints (such as image disease prediction) are capped at 10 requests per minute to prevent resource exhaustion.</li>
        <li><strong>Authentication Resolution:</strong> <code>get_current_user</code> verifies token signatures using HS256. If no token is provided, requests still succeed gracefully via the built-in <em>Guest Mode</em> fallback.</li>
        <li><strong>Business Logic & Inference:</strong> The router triggers the corresponding service. ML models are loaded lazily into memory on the first request to eliminate cold-start server lag.</li>
        <li><strong>Database Transaction:</strong> Queries, caches, and records are committed via SQLAlchemy sessions and returned through Pydantic response models.</li>
    </ol>
    """

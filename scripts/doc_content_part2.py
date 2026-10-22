def get_section3_html():
    return """
    <div class="page-break"></div>
    <div class="header-bar">
        <span class="doc-tag">Smart Kisan Project Guide</span>
        <span class="doc-version">Section 3 &bull; Technology Stack</span>
    </div>

    <h2 class="section-heading"><span class="sec-num">3</span> Technology Stack & Architectural Rationale</h2>
    
    <p>Every tool and library in Smart Kisan was selected specifically for high throughput, minimal developer friction, low hosting cost, and resilience under erratic rural internet connectivity.</p>

    <h3>1. Backend Engineering (Python Ecosystem)</h3>
    <table>
        <tr>
            <th style="width:22%;">Package / Tool</th>
            <th style="width:12%;">Version</th>
            <th>Role & Architectural Rationale</th>
        </tr>
        <tr>
            <td><code>fastapi</code></td>
            <td>0.115.0</td>
            <td>High-performance asynchronous web framework based on Starlette and Pydantic. Auto-generates OpenAPI / Swagger schemas, enforces strict type validation, and supports async I/O.</td>
        </tr>
        <tr>
            <td><code>uvicorn[standard]</code></td>
            <td>0.30.6</td>
            <td>Lightning-fast ASGI web server implementation using uvloop and httptools. Powers development hot-reloading (<code>--reload</code>).</td>
        </tr>
        <tr>
            <td><code>sqlalchemy</code></td>
            <td>2.0.35</td>
            <td>Production-grade Object Relational Mapper (ORM). Decouples database models from the underlying SQL dialect, enabling seamless migration from SQLite to PostgreSQL.</td>
        </tr>
        <tr>
            <td><code>pydantic</code></td>
            <td>2.9.2</td>
            <td>Data modeling and parsing library. Ensures incoming HTTP JSON payloads conform strictly to domain expectations before reaching router logic.</td>
        </tr>
        <tr>
            <td><code>python-jose</code></td>
            <td>3.3.0</td>
            <td>Cryptographic library for JSON Web Tokens (JWT). Signs and verifies user identity tokens using SHA-256 HMAC (HS256) with 24-hour expiration windows.</td>
        </tr>
        <tr>
            <td><code>passlib[bcrypt]</code></td>
            <td>1.7.4</td>
            <td>Industry standard password hashing with automatic salt generation and timing-attack resistant verification.</td>
        </tr>
        <tr>
            <td><code>tensorflow</code></td>
            <td>2.17.0</td>
            <td>Executes the pre-trained EfficientNetB3 deep learning convolutional neural network for plant disease inference.</td>
        </tr>
        <tr>
            <td><code>scikit-learn</code></td>
            <td>1.5.2</td>
            <td>Executes the Random Forest classifier for crop recommendation and handles feature normalization with <code>StandardScaler</code>.</td>
        </tr>
        <tr>
            <td><code>google-generativeai</code></td>
            <td>0.8.2</td>
            <td>Official SDK for Google Gemini 1.5 Flash. Delivers sub-second generative responses with high multilingual translation fidelity.</td>
        </tr>
        <tr>
            <td><code>chromadb</code></td>
            <td>0.5.7</td>
            <td>High-performance vector database. Computes cosine similarity across indexed agronomic documents to provide grounded context for RAG.</td>
        </tr>
        <tr>
            <td><code>slowapi</code></td>
            <td>0.1.9</td>
            <td>IP-based rate limiting middleware. Guards against denial-of-service attempts and malicious bot scraping on heavy ML endpoints.</td>
        </tr>
        <tr>
            <td><code>httpx</code></td>
            <td>0.27.2</td>
            <td>Asynchronous HTTP client for non-blocking outbound requests to Open-Meteo and data.gov.in APIs.</td>
        </tr>
    </table>

    <h3>2. Frontend Engineering (JavaScript Ecosystem)</h3>
    <table>
        <tr>
            <th style="width:22%;">Package / Tool</th>
            <th style="width:12%;">Version</th>
            <th>Role & Architectural Rationale</th>
        </tr>
        <tr>
            <td><code>react</code></td>
            <td>19.2.8</td>
            <td>Declarative component-based UI framework leveraging concurrent rendering and modern hook patterns (<code>useState</code>, <code>useEffect</code>, <code>useContext</code>).</td>
        </tr>
        <tr>
            <td><code>vite</code></td>
            <td>8.3.0</td>
            <td>Next-generation frontend tooling providing sub-100ms Hot Module Replacement (HMR) and optimized Rollup asset bundling.</td>
        </tr>
        <tr>
            <td><code>react-router-dom</code></td>
            <td>7.18.4</td>
            <td>Client-side routing managing URL transitions across all 7 feature modules without full browser reloads.</td>
        </tr>
        <tr>
            <td><code>index.css</code></td>
            <td>Custom</td>
            <td>Comprehensive 58KB Vanilla CSS Design System. Avoids bulky runtime CSS-in-JS dependencies while enforcing harmonious green-amber design tokens.</td>
        </tr>
        <tr>
            <td><code>i18next</code></td>
            <td>26.4.2</td>
            <td>Complete internationalization engine holding 200+ localized agricultural phrases in English, Hindi, and Marathi with zero remote fetch latency.</td>
        </tr>
        <tr>
            <td><code>recharts</code></td>
            <td>3.10.1</td>
            <td>SVG charting library. Renders responsive bar graphs comparing commodity prices across Indian APMC mandis.</td>
        </tr>
        <tr>
            <td><code>lucide-react</code></td>
            <td>1.52.0</td>
            <td>Crisp SVG iconography enhancing visual navigation for semi-literate rural users.</td>
        </tr>
    </table>
    """

def get_section4_html():
    return """
    <div class="page-break"></div>
    <div class="header-bar">
        <span class="doc-tag">Smart Kisan Project Guide</span>
        <span class="doc-version">Section 4 &bull; File Inventory</span>
    </div>

    <h2 class="section-heading"><span class="sec-num">4</span> Project Directory & File Structure</h2>
    
    <p>The repository follows a clean separation between backend service APIs, frontend client pages, machine learning assets, and database seeds:</p>

    <div class="pre-tag">Project Repository Layout</div>
    <pre>
Smart-Kisan/
├── .env.example                     # Environment template defining DB, SECRET_KEY, API keys
├── README.md                        # Developer onboarding and system launch manual
├── smart_kisan.db                   # Root SQLite database holding persistent records
│
├── backend/                         # FastAPI Application Package
│   ├── requirements.txt             # Manifest of 22 Python dependencies
│   └── app/
│       ├── main.py                  # Server entry point: middleware, routers, lifespans
│       ├── config.py                # Pydantic Settings reading .env configurations
│       ├── database.py              # Engine creation, declarative base, get_db() generator
│       ├── models/
│       │   └── __init__.py           # Declarative SQLAlchemy models (Users, Diseases, Crops, etc.)
│       ├── schemas/
│       │   └── auth.py               # Pydantic schemas validating registration & login
│       ├── core/
│       │   └── security.py           # Bcrypt hashing utilities, JWT encoder/decoder, auth dependency
│       ├── routers/                  # Modular REST route controllers
│       │   ├── auth.py               # /api/v1/auth (register, login, me, profile updates)
│       │   ├── disease.py            # /api/v1/predict/disease (image upload & diagnosis)
│       │   ├── crop.py               # /api/v1/recommend/crop (NPK agronomic recommendations)
│       │   ├── weather.py            # /api/v1/weather (Open-Meteo fetch & advisory engine)
│       │   ├── market.py             # /api/v1/market (APMC mandi pricing & historical trends)
│       │   ├── schemes.py            # /api/v1/schemes (search & filter central/state schemes)
│       │   ├── chat.py               # /api/v1/chat (multilingual Gemini RAG interaction)
│       │   └── history.py            # /api/v1/history (unified farmer diagnostic history)
│       ├── ml/                       # Machine Learning inference engines
│       │   ├── disease_model.py       # EfficientNetB3 loader, image preprocessor, predictor
│       │   ├── crop_model.py          # Random Forest joblib loader, scaler, prediction logic
│       │   └── rag_engine.py          # ChromaDB vector indexer & Gemini client integration
│       └── utils/
│           └── weather_rules.py       # Agronomic heuristic engine generating weather advisories
│
├── frontend/                        # React 19 Client Application
│   ├── package.json                 # Node dependencies and build scripts
│   ├── vite.config.js               # Dev server configuration with backend /api proxy
│   └── src/
│       ├── App.jsx                   # Root layout, routing routes, Splash and Auth wrapper
│       ├── i18n.js                   # 200+ translation keys for English, Hindi, Marathi
│       ├── index.css                 # 58KB Vanilla CSS design system with custom properties
│       ├── context/
│       │   └── AuthContext.jsx       # Global authentication state, JWT storage, Guest Mode
│       ├── services/
│       │   └── api.js                # Axios client with automatic Bearer token interceptor
│       ├── components/
│       │   ├── Sidebar.jsx            # Desktop responsive sidebar navigation
│       │   ├── TopHeader.jsx          # Header with breadcrumb trail, mobile toggle, language
│       │   ├── BottomNav.jsx          # Mobile 5-tab fixed navigation dock
│       │   └── SplashScreen.jsx       # 1.9-second animated branding introduction
│       └── pages/                    # Core view components
│           ├── Home.jsx               # Dashboard summary, quick actions, weather overview
│           ├── DiseaseDetector.jsx    # Leaf image uploader, camera capture, diagnosis report
│           ├── CropAdvisor.jsx        # Soil NPK form, regional presets, crop ranking view
│           ├── MarketPrices.jsx       # Commodity selection, APMC table, Recharts chart
│           ├── Schemes.jsx            # Government scheme cards, category filters, search
│           ├── Chat.jsx               # Conversational AI dialogue interface with audio/chips
│           └── Profile.jsx            # Farm data, language settings, consolidated logs
│
├── database/
│   └── seed_schemes.py               # Seeds 10+ official farmer welfare schemes
├── models/                           # Binary weights (EfficientNet, Random Forest, ChromaDB)
├── uploads/                          # Persistent storage for uploaded leaf diagnosis photos
└── docs/                             # Project manuals, architectural diagrams, PDF documentation
    </pre>
    """

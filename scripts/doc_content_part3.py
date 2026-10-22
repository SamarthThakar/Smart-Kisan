def get_section5_html():
    return """
    <div class="page-break"></div>
    <div class="header-bar">
        <span class="doc-tag">Smart Kisan Project Guide</span>
        <span class="doc-version">Section 5 &bull; Feature Deep-Dive</span>
    </div>

    <h2 class="section-heading"><span class="sec-num">5</span> In-Depth Feature Breakdown</h2>
    
    <p>Smart Kisan is built around 7 core modules, each engineered with strict validation, real-time feedback, and offline fallback capability:</p>

    <h3>1. Leaf Disease Doctor (<code>/disease</code>)</h3>
    <div class="card">
        <p>Allows farmers to upload or snap a photo of an infected leaf. The platform executes an AI visual diagnostic and returns a tailored disease report.</p>
        <ul>
            <li><strong>Input:</strong> Image file (JPEG, PNG, WebP) up to 10MB via file picker or webcam.</li>
            <li><strong>File Validation:</strong> Validates MIME headers and inspects raw magic bytes (<code>\\xFF\\xD8\\xFF</code> for JPEG, <code>\\x89PNG</code> for PNG, <code>RIFF</code> for WebP) to prevent malicious executable injection.</li>
            <li><strong>Inference Engine:</strong> Resizes image to 224x224 RGB, applies ImageNet normalization, and runs EfficientNetB3 inference across 38+ plant pathology classes.</li>
            <li><strong>Output:</strong> Top-3 predicted diseases with confidence scores, severity rating (None, Medium, High), chemical treatments, cultural preventative actions, and a Krishi Vigyan Kendra (KVK) advisory notice.</li>
            <li><strong>Built-in Samples:</strong> Includes instant 1-click test leaves (Tomato Early Blight, Healthy Potato, Corn Rust) for seamless demonstrations.</li>
        </ul>
    </div>

    <h3>2. Crop Advisor (<code>/crop</code>)</h3>
    <div class="card">
        <p>Predicts the top 5 most profitable and biologically suitable crops based on soil chemistry and regional weather parameters.</p>
        <ul>
            <li><strong>Inputs:</strong> Nitrogen (0-200 kg/ha), Phosphorus (0-200 kg/ha), Potassium (0-200 kg/ha), pH (0-14), Temperature (&deg;C), Humidity (%), and Annual Rainfall (mm).</li>
            <li><strong>Regional Soil Presets:</strong> Quick-fill buttons for <em>Black Cotton Soil</em> (High K, medium N/P), <em>Alluvial Soil</em> (Balanced NPK), and <em>Red Laterite</em> (Acidic, low N/P).</li>
            <li><strong>Inference Engine:</strong> Standardizes input features via <code>StandardScaler</code> and evaluates them using a Random Forest Classifier trained on ICAR multi-crop benchmarks.</li>
            <li><strong>Output:</strong> Ranked list of 5 crops with suitability percentages, water requirements (Low/Medium/High), optimal growing season (Kharif, Rabi, Zaid), and current market demand.</li>
        </ul>
    </div>

    <h3>3. Weather Advisory & Alert Engine (<code>/</code>)</h3>
    <div class="card">
        <p>Integrates precision meteorological data with agronomic heuristic rules to safeguard crops against adverse weather events.</p>
        <ul>
            <li><strong>Data Provider:</strong> Open-Meteo REST API. Completely free, high-uptime, requiring zero API keys.</li>
            <li><strong>Parameters:</strong> 7-day temperature range (min/max), relative humidity, precipitation probability, wind speed, and reference evapotranspiration (ET<sub>0</sub>).</li>
            <li><strong>Agronomic Rule Engine (<code>weather_rules.py</code>):</strong>
                <ul>
                    <li><em>Foliar Spray Advisory:</em> Flags high winds (&gt;15 km/h) or impending rain (&gt;40%) to warn against wasted pesticide application.</li>
                    <li><em>Crop Inundation Warning:</em> Alerts farmers when rainfall exceeds 50mm within 24 hours.</li>
                    <li><em>Frost Protection Alert:</em> Warns northern farmers when night temperatures dip below 4&deg;C.</li>
                </ul>
            </li>
            <li><strong>Intelligent Cache:</strong> Caches weather responses in the database for 6 hours per coordinate pair to eliminate redundant network traffic.</li>
        </ul>
    </div>

    <h3>4. Live Mandi Market Prices (<code>/market</code>)</h3>
    <div class="card">
        <p>Empowers farmers to negotiate fair prices by providing real-time commodity pricing across Agricultural Produce Market Committees (APMCs).</p>
        <ul>
            <li><strong>Data Source:</strong> data.gov.in official Open Government Data (OGD) platform with automated fallback to realistic price simulations.</li>
            <li><strong>Commodity Scope:</strong> 23 primary Indian crops including Rice, Wheat, Cotton, Soybean, Onion, Tomato, Mustard, and Turmeric.</li>
            <li><strong>Market Intelligence:</strong>
                <ul>
                    <li>Displays Minimum, Maximum, and Modal (prevailing) prices per quintal (100 kg).</li>
                    <li><strong>"Best Mandi" Badge:</strong> Highlights the local market offering the highest modal payout.</li>
                    <li><strong>Recharts Interactive Graph:</strong> Renders visual price comparisons across state mandis.</li>
                </ul>
            </li>
        </ul>
    </div>

    <h3>5. Government Welfare Schemes Directory (<code>/schemes</code>)</h3>
    <div class="card">
        <p>Centralizes welfare programs, subsidies, and credit schemes from the Ministry of Agriculture and Farmers Welfare.</p>
        <ul>
            <li><strong>Cataloged Schemes:</strong> PM-KISAN (&pound;6,000 direct income support), PMFBY (Pradhan Mantri Fasal Bima Yojana - crop insurance), KCC (Kisan Credit Card at 4% subsidized interest), e-NAM (National Agriculture Market), and AIF (Agriculture Infrastructure Fund).</li>
            <li><strong>Filtering Dimensions:</strong> Scheme type (Subsidy, Insurance, Credit, Organic), state applicability, and target farmer category (Marginal, Small, Medium).</li>
            <li><strong>Direct Action:</strong> Full eligibility breakdowns, documentation requirements, and direct external links to official government application portals.</li>
        </ul>
    </div>

    <h3>6. Krishi Mitra Multilingual AI Specialist (<code>/chat</code>)</h3>
    <div class="card">
        <p>A 24/7 agricultural domain chatbot powered by Google Gemini 1.5 Flash grounded with ChromaDB vector search.</p>
        <ul>
            <li><strong>Multilingual Engine:</strong> Native conversational understanding and generation in <strong>English</strong>, <strong>हिंदी (Hindi)</strong>, and <strong>मराठी (Marathi)</strong>.</li>
            <li><strong>RAG Grounding:</strong> Vector database contains verified agronomic advisories. Restricts the model from inventing unverified chemical dosages or false pricing.</li>
            <li><strong>Conversation Memory:</strong> Retains dialogue history for multi-turn conversational follow-ups.</li>
        </ul>
    </div>

    <h3>7. Farmer Profile & Consolidated History (<code>/profile</code>)</h3>
    <div class="card">
        <p>A centralized dashboard for personal farm metrics, past diagnostic reports, and application-wide preferences.</p>
        <ul>
            <li><strong>Farm Demographics:</strong> Landholding acreage, primary cultivated crops, state/district, and soil classification.</li>
            <li><strong>Audit Logs:</strong> Unified chronological timeline of previous leaf disease scans (with preview thumbnails) and crop recommendation runs.</li>
            <li><strong>Instant Localization:</strong> Allows switching the active UI language across all pages with a single click.</li>
        </ul>
    </div>
    """

def get_section6_html():
    return """
    <div class="page-break"></div>
    <div class="header-bar">
        <span class="doc-tag">Smart Kisan Project Guide</span>
        <span class="doc-version">Section 6 &bull; REST API Reference</span>
    </div>

    <h2 class="section-heading"><span class="sec-num">6</span> Complete REST API Reference</h2>
    
    <p>All endpoints are prefixed with <code>/api/v1</code>. Interactive documentation is accessible at <code>http://127.0.0.1:8000/docs</code>.</p>

    <h3>Authentication Endpoints (<code>/auth</code>)</h3>
    <div class="api-endpoint">
        <span class="method-badge method-post">POST</span>
        <span class="endpoint-path">/auth/register</span>
        <span class="endpoint-desc">Registers a farmer account with phone, full name, language, and password.</span>
    </div>
    <div class="api-endpoint">
        <span class="method-badge method-post">POST</span>
        <span class="endpoint-path">/auth/login</span>
        <span class="endpoint-desc">Authenticates phone & password. Returns JWT access token (HS256).</span>
    </div>
    <div class="api-endpoint">
        <span class="method-badge method-get">GET</span>
        <span class="endpoint-path">/auth/me</span>
        <span class="endpoint-desc">Fetches current profile. Requires <code>Authorization: Bearer &lt;token&gt;</code>.</span>
    </div>
    <div class="api-endpoint">
        <span class="method-badge method-put">POST</span>
        <span class="endpoint-path">/auth/profile</span>
        <span class="endpoint-desc">Updates farm details (land size, crops, state, coordinates).</span>
    </div>

    <h3>Plant Pathology Diagnostics (<code>/predict</code>)</h3>
    <div class="api-endpoint">
        <span class="method-badge method-post">POST</span>
        <span class="endpoint-path">/predict/disease</span>
        <span class="endpoint-desc">Accepts multipart leaf image. Returns top-3 diagnoses, treatments, severity. (Rate: 10/min)</span>
    </div>
    <div class="api-endpoint">
        <span class="method-badge method-get">GET</span>
        <span class="endpoint-path">/predict/disease/history</span>
        <span class="endpoint-desc">Returns paginated diagnostic history for the authenticated farmer.</span>
    </div>

    <h3>Agronomic Crop Recommendations (<code>/recommend</code>)</h3>
    <div class="api-endpoint">
        <span class="method-badge method-post">POST</span>
        <span class="endpoint-path">/recommend/crop</span>
        <span class="endpoint-desc">JSON payload: {N, P, K, pH, temperature, humidity, rainfall}. Returns top 5 crops.</span>
    </div>

    <h3>Weather & Advisory (<code>/weather</code>)</h3>
    <div class="api-endpoint">
        <span class="method-badge method-get">GET</span>
        <span class="endpoint-path">/weather?lat=18.52&lon=73.85</span>
        <span class="endpoint-desc">Fetches 7-day forecast & farming alerts. Cached 6 hrs per coordinate.</span>
    </div>

    <h3>Mandi Market Rates (<code>/market</code>)</h3>
    <div class="api-endpoint">
        <span class="method-badge method-get">GET</span>
        <span class="endpoint-path">/market/commodities</span>
        <span class="endpoint-desc">Returns list of all 23 trackable agricultural commodities.</span>
    </div>
    <div class="api-endpoint">
        <span class="method-badge method-get">GET</span>
        <span class="endpoint-path">/market/prices?commodity=Wheat&state=Punjab</span>
        <span class="endpoint-desc">Fetches modal/min/max rates across APMCs with Best Mandi tag.</span>
    </div>

    <h3>Welfare Schemes (<code>/schemes</code>)</h3>
    <div class="api-endpoint">
        <span class="method-badge method-get">GET</span>
        <span class="endpoint-path">/schemes?scheme_type=subsidy&q=kisan</span>
        <span class="endpoint-desc">Searches and filters government welfare schemes.</span>
    </div>
    <div class="api-endpoint">
        <span class="method-badge method-get">GET</span>
        <span class="endpoint-path">/schemes/types</span>
        <span class="endpoint-desc">Returns categorized scheme types with emoji icons and descriptions.</span>
    </div>

    <h3>Conversational AI (<code>/chat</code>)</h3>
    <div class="api-endpoint">
        <span class="method-badge method-post">POST</span>
        <span class="endpoint-path">/chat</span>
        <span class="endpoint-desc">Payload: {message, session_id, language}. Returns RAG-grounded response.</span>
    </div>
    <div class="api-endpoint">
        <span class="method-badge method-get">GET</span>
        <span class="endpoint-path">/chat/history</span>
        <span class="endpoint-desc">Returns message history for active conversation session.</span>
    </div>

    <h3>System & History (<code>/history</code>, <code>/health</code>)</h3>
    <div class="api-endpoint">
        <span class="method-badge method-get">GET</span>
        <span class="endpoint-path">/history?type=all</span>
        <span class="endpoint-desc">Consolidated timeline of disease scans and crop recommendations.</span>
    </div>
    <div class="api-endpoint">
        <span class="method-badge method-get">GET</span>
        <span class="endpoint-path">/api/v1/health</span>
        <span class="endpoint-desc">System health check: API version, database connectivity, model status.</span>
    </div>
    """

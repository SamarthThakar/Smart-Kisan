def get_section7_html():
    return """
    <div class="page-break"></div>
    <div class="header-bar">
        <span class="doc-tag">Smart Kisan Project Guide</span>
        <span class="doc-version">Section 7 &bull; Database Schema</span>
    </div>

    <h2 class="section-heading"><span class="sec-num">7</span> Database Architecture & Data Models</h2>
    
    <p>Smart Kisan uses SQLAlchemy 2.0 ORM with 10 tables. The schema supports SQLite during local development and is fully compatible with PostgreSQL in production.</p>

    <h3>Primary Entities & Schema Definitions</h3>
    <table>
        <tr>
            <th style="width:24%;">Table Name</th>
            <th style="width:28%;">Primary & Foreign Keys</th>
            <th>Core Attributes & Data Types</th>
        </tr>
        <tr>
            <td><code>users</code></td>
            <td><code>id</code> (PK, UUID String)<br>Index on <code>phone</code></td>
            <td><code>phone</code> (VARCHAR 15, Unique), <code>password_hash</code> (VARCHAR 255), <code>full_name</code> (VARCHAR 100), <code>preferred_language</code> (VARCHAR 10), <code>is_active</code> (BOOLEAN), <code>created_at</code> (DATETIME), <code>last_login</code> (DATETIME)</td>
        </tr>
        <tr>
            <td><code>farmer_profiles</code></td>
            <td><code>id</code> (PK, UUID)<br><code>user_id</code> (FK &rarr; users.id)</td>
            <td><code>state</code> (VARCHAR 50), <code>district</code> (VARCHAR 50), <code>latitude</code> (FLOAT), <code>longitude</code> (FLOAT), <code>land_size_acres</code> (FLOAT), <code>primary_crops</code> (JSON array), <code>farmer_category</code> (VARCHAR 20), <code>soil_type</code> (VARCHAR 50)</td>
        </tr>
        <tr>
            <td><code>disease_predictions</code></td>
            <td><code>id</code> (PK, UUID)<br><code>user_id</code> (FK &rarr; users.id)</td>
            <td><code>image_path</code> (VARCHAR 500), <code>disease_name</code> (VARCHAR 150), <code>confidence</code> (FLOAT), <code>top3_results</code> (JSON array of predictions), <code>treatment_shown</code> (JSON array of action steps), <code>crop_type</code> (VARCHAR 100), <code>user_rating</code> (SMALLINT 1-5), <code>created_at</code> (DATETIME)</td>
        </tr>
        <tr>
            <td><code>crop_recommendations</code></td>
            <td><code>id</code> (PK, UUID)<br><code>user_id</code> (FK &rarr; users.id)</td>
            <td><code>input_params</code> (JSON: N, P, K, pH, temp, humidity, rainfall), <code>recommended_crops</code> (JSON array of top 5 ranked crops), <code>created_at</code> (DATETIME)</td>
        </tr>
        <tr>
            <td><code>weather_cache</code></td>
            <td><code>id</code> (PK, UUID)<br>Index on <code>lat_lon_key</code></td>
            <td><code>lat_lon_key</code> (VARCHAR 50: rounded lat/lon), <code>weather_data</code> (JSON: 7-day forecast), <code>farming_advice</code> (JSON: rules engine output), <code>expires_at</code> (DATETIME: 6h TTL)</td>
        </tr>
        <tr>
            <td><code>market_prices</code></td>
            <td><code>id</code> (PK, UUID)</td>
            <td><code>commodity</code> (VARCHAR 50), <code>market_name</code> (VARCHAR 100), <code>state</code> (VARCHAR 50), <code>min_price</code> (FLOAT), <code>max_price</code> (FLOAT), <code>modal_price</code> (FLOAT), <code>price_date</code> (DATE), <code>source</code> (VARCHAR 20)</td>
        </tr>
        <tr>
            <td><code>government_schemes</code></td>
            <td><code>id</code> (PK, UUID)</td>
            <td><code>scheme_name</code> (VARCHAR 150), <code>scheme_type</code> (VARCHAR 50), <code>description</code> (TEXT), <code>benefits</code> (JSON array), <code>eligibility_criteria</code> (JSON object), <code>applicable_states</code> (JSON array), <code>official_url</code> (VARCHAR 500)</td>
        </tr>
        <tr>
            <td><code>chat_history</code></td>
            <td><code>id</code> (PK, UUID)<br><code>user_id</code> (FK &rarr; users.id)</td>
            <td><code>session_id</code> (VARCHAR 50), <code>role</code> (VARCHAR 20: user/assistant), <code>content</code> (TEXT), <code>language</code> (VARCHAR 10), <code>sources_used</code> (JSON array of citations), <code>created_at</code> (DATETIME)</td>
        </tr>
        <tr>
            <td><code>notifications</code></td>
            <td><code>id</code> (PK, UUID)<br><code>user_id</code> (FK &rarr; users.id)</td>
            <td><code>type</code> (VARCHAR 50: weather/disease/scheme), <code>title</code> (VARCHAR 150), <code>message</code> (TEXT), <code>is_read</code> (BOOLEAN, default False), <code>created_at</code> (DATETIME)</td>
        </tr>
        <tr>
            <td><code>user_feedback</code></td>
            <td><code>id</code> (PK, UUID)<br><code>user_id</code> (FK &rarr; users.id)</td>
            <td><code>feature</code> (VARCHAR 50), <code>prediction_id</code> (VARCHAR 50), <code>rating</code> (SMALLINT 1-5), <code>comment</code> (TEXT), <code>created_at</code> (DATETIME)</td>
        </tr>
    </table>
    """

def get_section8_html():
    return """
    <div class="page-break"></div>
    <div class="header-bar">
        <span class="doc-tag">Smart Kisan Project Guide</span>
        <span class="doc-version">Section 8 &bull; Machine Learning Pipeline</span>
    </div>

    <h2 class="section-heading"><span class="sec-num">8</span> Machine Learning & AI Pipeline Deep Dive</h2>
    
    <p>The intelligence layer of Smart Kisan is split into three dedicated engines designed for fast inference and resilience under offline or uninstalled conditions:</p>

    <h3>1. Plant Pathology Vision: EfficientNetB3 (<code>disease_model.py</code>)</h3>
    <div class="card">
        <p>EfficientNetB3 scales depth, width, and resolution using a compound coefficient. It balances lightweight edge inference with high diagnostic accuracy on complex leaf textures.</p>
        <div class="pre-tag">Python Inference Pipeline</div>
        <pre>
# 1. Lazy Loading (Loads into RAM only upon the first diagnostic request)
model = tf.keras.models.load_model("models/disease_model.keras")

# 2. Image Preprocessing
image = Image.open(BytesIO(image_bytes)).convert("RGB").resize((224, 224))
img_array = np.array(image, dtype=np.float32)
img_array = tf.keras.applications.efficientnet.preprocess_input(img_array)
img_array = np.expand_dims(img_array, axis=0)  # Shape: [1, 224, 224, 3]

# 3. Softmax Classification across 38+ plant pathology classes
raw_probs = model.predict(img_array, verbose=0)[0]
top3_idx = np.argsort(raw_probs)[-3:][::-1]
predictions = [{"disease": class_names[i], "confidence": float(raw_probs[i])} for i in top3_idx]
        </pre>
        <p><strong>Fail-Safe Fallback:</strong> If TensorFlow binary weights are missing during local development, the system automatically falls back to high-fidelity mock diagnostic data (e.g. Tomato Late Blight at 87.3% confidence) to ensure the UI remains fully functional.</p>
    </div>

    <h3>2. Agronomic Crop Recommendation: Random Forest (<code>crop_model.py</code>)</h3>
    <div class="card">
        <p>Trained on the ICAR Multi-Crop dataset across 2,200 soil-climate observations covering 22 distinct crops. Uses 100 decision trees to avoid overfitting on single soil parameters.</p>
        <div class="pre-tag">Crop Predictor Pipeline</div>
        <pre>
# Feature vector order: [N, P, K, pH, temperature, humidity, rainfall]
raw_features = np.array([[n, p, k, ph, temp, humidity, rainfall]], dtype=np.float32)

# StandardScaler Normalization
scaled_features = scaler.transform(raw_features)

# Class Probability Estimation
probabilities = model.predict_proba(scaled_features)[0]
top5_indices = np.argsort(probabilities)[-5:][::-1]
recommendations = [
    {"crop": label_encoder.inverse_transform([idx])[0], "suitability": round(probabilities[idx] * 100, 1)}
    for idx in top5_indices
]
        </pre>
    </div>

    <h3>3. Conversational RAG Engine: Gemini 1.5 Flash + ChromaDB (<code>rag_engine.py</code>)</h3>
    <div class="card">
        <p>Combines sub-second LLM generation with domain-verified agricultural publications stored in a local ChromaDB vector collection:</p>
        <ul>
            <li><strong>Vector Storage:</strong> Indexed agricultural chunks from ICAR, extension bulletins, and government schemes using cosine similarity distance thresholds (<code>distance &lt; 0.7</code>).</li>
            <li><strong>System Prompt Constraints:</strong> Enforces domain isolation &mdash; declines medical, political, or off-topic questions; speaks in the farmer's dialect; explicitly recommends consulting local Krishi Vigyan Kendras for severe outbreaks.</li>
            <li><strong>Conversation Memory:</strong> Contextually threads the last 3 conversational turns to maintain dialogue coherence during follow-up questions.</li>
        </ul>
    </div>
    """

def get_section9_html():
    return """
    <div class="page-break"></div>
    <div class="header-bar">
        <span class="doc-tag">Smart Kisan Project Guide</span>
        <span class="doc-version">Section 9 &bull; Frontend & Design System</span>
    </div>

    <h2 class="section-heading"><span class="sec-num">9</span> Frontend Architecture & Design System</h2>

    <p>The frontend is built with React 19 and Vite. It avoids third-party CSS frameworks like Tailwind or Bootstrap in favor of a bespoke 58KB Vanilla CSS design system (<code>index.css</code>) optimized for smooth rendering on low-cost Android devices.</p>

    <div class="grid-2">
        <div class="card highlight">
            <h4>Harmonious Design Tokens</h4>
            <p>Built with agricultural tones: Deep Forest Green (<code>#14532d</code>), Leaf Emerald (<code>#22c55e</code>), Golden Harvest Amber (<code>#d97706</code>), and clean neutral grays for sunlight readability.</p>
        </div>
        <div class="card highlight">
            <h4>Adaptive Navigation</h4>
            <p>Desktop users get a permanent 7-item sidebar. Mobile devices switch to a fixed bottom 5-tab bar and a top bar with breadcrumb tracking.</p>
        </div>
    </div>

    <h3>Global Authentication & The "Guest Mode" Pattern</h3>
    <p>To prevent user friction in rural communities, Smart Kisan provides a <strong>Guest Mode</strong> managed by <code>AuthContext.jsx</code>:</p>
    <ul>
        <li>On load, the app checks <code>localStorage</code> for an existing JWT token.</li>
        <li>If present, it validates the token via <code>GET /api/v1/auth/me</code> and hydrates the farmer's profile.</li>
        <li>If absent, it automatically logs in a default guest user ("<em>Kisan Mitra (Demo)</em>"). Every feature remains accessible, ensuring zero onboarding friction for new visitors.</li>
    </ul>

    <h3>Internationalization (i18n.js)</h3>
    <p>All UI strings across all 7 views are stored directly in <code>frontend/src/i18n.js</code>. Farmers can toggle between English, Hindi, and Marathi in real time without refreshing the page or making network requests.</p>
    """

def get_section10_html():
    return """
    <div class="page-break"></div>
    <div class="header-bar">
        <span class="doc-tag">Smart Kisan Project Guide</span>
        <span class="doc-version">Section 10 &bull; Security & Setup</span>
    </div>

    <h2 class="section-heading"><span class="sec-num">10</span> Security, Reliability & Quality Assurance</h2>

    <div class="grid-2">
        <div class="card alert">
            <h4>Cryptographic Token Security</h4>
            <p>Authentication utilizes HS256 JWT tokens with a 24-hour expiration window. Passwords are salted and hashed using bcrypt via <code>passlib</code>.</p>
        </div>
        <div class="card alert">
            <h4>Magic-Byte Upload Validation</h4>
            <p>Prevents file extension spoofing by inspecting raw binary headers (JPEG, PNG, WebP) and enforcing a 10MB file size ceiling.</p>
        </div>
        <div class="card alert">
            <h4>IP-Based Rate Limiting</h4>
            <p>SlowAPI enforces 10 requests per minute on deep learning inference routes, preventing denial-of-service from malicious actors.</p>
        </div>
        <div class="card alert">
            <h4>Safe ORM Parameterization</h4>
            <p>SQLAlchemy 2.0 uses parameterized SQL queries, completely eliminating SQL injection risks across all endpoints.</p>
        </div>
    </div>

    <h2 class="section-heading"><span class="sec-num">11</span> Step-by-Step Developer Setup Guide</h2>

    <h3>1. Prerequisites</h3>
    <p>Ensure Python 3.11+ (tested on Python 3.13) and Node.js 18+ with npm are installed on your workstation.</p>

    <h3>2. Clone Repository & Setup Environment</h3>
    <div class="pre-tag">Bash / PowerShell</div>
    <pre>
git clone https://github.com/your-username/Smart-Kisan.git
cd Smart-Kisan

# Copy environment variables template
copy .env.example .env    # Windows
# cp .env.example .env    # Linux / macOS
    </pre>

    <h3>3. Launch Backend API</h3>
    <div class="pre-tag">Bash / PowerShell (Backend Terminal)</div>
    <pre>
cd backend
python -m venv venv
venv\\Scripts\\activate          # Windows (source venv/bin/activate on Linux/Mac)
pip install -r requirements.txt
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
    </pre>
    <p>The backend auto-seeds the database schema, seeds government welfare programs, and opens Swagger documentation at <code>http://127.0.0.1:8000/docs</code>.</p>

    <h3>4. Launch Frontend Web Application</h3>
    <div class="pre-tag">Bash / PowerShell (Frontend Terminal)</div>
    <pre>
cd frontend
npm install
npm run dev
    </pre>
    <p>Open <code>http://localhost:5173</code> in your browser to explore the running application.</p>

    <h2 class="section-heading"><span class="sec-num">12</span> Production Cloud Deployment Architecture</h2>
    <table>
        <tr>
            <th>Application Layer</th>
            <th>Recommended Host</th>
            <th>Configuration Details</th>
        </tr>
        <tr>
            <td>FastAPI Backend</td>
            <td>Render / AWS EC2 / Railway</td>
            <td>Start command: <code>uvicorn app.main:app --host 0.0.0.0 --port $PORT</code></td>
        </tr>
        <tr>
            <td>React Frontend</td>
            <td>Vercel / Cloudflare Pages</td>
            <td>Build command: <code>npm run build</code>, Output directory: <code>dist</code></td>
        </tr>
        <tr>
            <td>Relational Database</td>
            <td>Supabase / Neon (PostgreSQL)</td>
            <td>Set <code>DATABASE_URL=postgresql://user:pass@host:5432/db</code> in environment variables</td>
        </tr>
    </table>

    <div class="doc-footer">
        <strong>Smart Kisan</strong> &bull; Complete Technical Project Documentation &bull; Version 1.0.0 &bull; Generated for Developer Evaluation
    </div>
    """

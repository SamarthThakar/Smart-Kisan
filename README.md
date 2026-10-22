# 🌾 Smart Kisan — AI Farming Companion

**Smart Kisan** is an AI-powered agricultural advisory platform designed for Indian farmers. It combines computer vision, machine learning agronomic models, real-time weather analytics, market mandi pricing intelligence, and a multilingual generative AI assistant.

---

## 🌟 Key Features

1. **🍃 Leaf Disease Doctor (`/disease`)**:
   - Leaf image upload or instant camera capture (`JPG`, `PNG`, `WebP`).
   - Deep learning computer vision diagnosis with severity scoring and confidence percentage.
   - Prescriptive treatment plan, preventative cultural practices, and Krishi Vigyan Kendra (KVK) advisory.
   - Built-in sample leaves for instant 1-click testing.

2. **🌱 Crop Advisor (`/crop`)**:
   - Random Forest model matching Soil N-P-K, pH, temperature, humidity, and rainfall.
   - Regional soil presets (Black Cotton Soil, Alluvial Soil, Red Laterite).
   - Ranked crop recommendations with suitability percentage, water requirement, and seasonal demand.

3. **📊 Live Mandi Market Prices (`/market`)**:
   - Real-time and sample commodity rates across Indian APMC mandis.
   - Automated "Best Mandi" highlight badge to identify peak sale opportunities.
   - Interactive price comparison chart powered by Recharts.

4. **☀️ Weather & Advisory Widget (`/`)**:
   - Real-time temperature, humidity, wind speed, and precipitation forecasts.
   - Automated agronomic advisory alerts (optimal foliar spray windows, rain protection).
   - 7-day outlook tailored for farm operations.

5. **🏛️ Government Schemes Directory (`/schemes`)**:
   - Curated central and state farmer welfare schemes (PM-KISAN, PMFBY, KCC, e-NAM, AIF).
   - Search and filtering by subsidy, crop insurance, and credit categories.
   - Direct links to official government application portals.

6. **🤖 Krishi Mitra Multilingual AI (`/chat`)**:
   - 24/7 conversational agricultural specialist answering farming queries.
   - Full support for **English**, **हिंदी (Hindi)**, and **मराठी (Marathi)**.
   - Quick query chips for common agronomic challenges.

7. **👤 Farmer Profile & Activity History (`/profile`)**:
   - Landholding and soil type preferences.
   - Unified historical logs for previous leaf diagnoses and crop recommendations.
   - One-click language switching across the entire app.

---

## 🚀 Running the Project

### 1. Backend (FastAPI)
```bash
cd backend
# Activate virtual environment
venv\Scripts\activate
# Start FastAPI development server
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```
- Interactive API Docs: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- Alternative Redoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

### 2. Frontend (React + Vite)
```bash
cd frontend
# Start Vite development server
npm run dev
```
- Local Application: [http://localhost:5173](http://localhost:5173)

---

## 🛠️ Tech Stack

- **Backend**: Python 3.13, FastAPI, SQLAlchemy, SQLite, Pydantic, SlowAPI rate limiting.
- **Frontend**: React 19, Vite, Vanilla CSS Design System (`index.css`), React Router DOM, Recharts, Lucide Icons, i18next, React Hot Toast.
- **ML / AI**: EfficientNet leaf disease inference, Random Forest crop recommendation, Google Gemini & RAG architecture.

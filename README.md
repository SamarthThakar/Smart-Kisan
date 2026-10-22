# 🌾 Smart Kisan — AI Farming Companion

Smart Kisan is an AI-powered agricultural advisory platform designed for Indian farmers. It combines computer vision, machine learning-based agronomic models, weather analytics, mandi market price intelligence, and a multilingual generative AI assistant.

## 🌟 Key Features

### 1. 🍃 Leaf Disease Doctor (`/disease`)

* Upload leaf images or capture photos directly using a camera.
* Supports JPG, PNG, and WebP images.
* Provides AI-assisted disease diagnosis, severity scoring, and confidence percentages.
* Offers treatment recommendations, preventive farming practices, and Krishi Vigyan Kendra (KVK) advisory.
* Includes sample leaf images for quick testing.

### 2. 🌱 Crop Advisor (`/crop`)

* Uses a Random Forest model to recommend suitable crops based on soil N-P-K values, pH, temperature, humidity, and rainfall.
* Includes regional soil presets: Black Cotton Soil, Alluvial Soil, and Red Laterite Soil.
* Provides ranked crop recommendations, suitability percentages, water requirements, and seasonal demand information.

### 3. 📊 Mandi Market Prices (`/market`)

* Displays real-time or sample commodity prices across Indian APMC mandis, depending on data availability.
* Highlights potentially favorable markets using a "Best Mandi" indicator.
* Provides interactive price comparison charts using Recharts.

### 4. ☀️ Weather and Agricultural Advisory (`/`)

* Displays weather information, including temperature, humidity, wind speed, and precipitation, when weather data is available.
* Provides agricultural advisory alerts, such as suitable foliar spray windows and rain protection recommendations.
* Includes a seven-day weather outlook when supported by the configured weather service.

### 5. 🏛️ Government Schemes Directory (`/schemes`)

* Provides information about farmer welfare schemes, including PM-KISAN, PMFBY, KCC, e-NAM, and AIF.
* Supports searching and filtering schemes by categories such as subsidies, crop insurance, and credit.
* Provides links to official government application portals where available.

### 6. 🤖 Krishi Mitra — Multilingual AI Assistant (`/chat`)

* Provides a conversational assistant for agricultural questions.
* Supports English, Hindi (हिंदी), and Marathi (मराठी).
* Includes quick-query suggestions for common agricultural challenges.
* Uses the configured AI service and retrieval components where available.

### 7. 👤 Farmer Profile and Activity History (`/profile`)

* Stores farmer preferences, such as landholding and soil type, according to the application's configured storage.
* Provides historical records of disease diagnoses and crop recommendations where supported.
* Offers language switching across the application.

## 🛠️ Technology Stack

### Frontend

* React 19
* Vite
* React Router DOM
* Vanilla CSS
* Recharts
* Lucide Icons
* i18next
* React Hot Toast

### Backend

* Python
* FastAPI
* SQLAlchemy
* SQLite
* Pydantic
* SlowAPI

### Machine Learning and AI

* EfficientNet-based leaf disease inference components
* Random Forest crop recommendation
* Google Gemini integration
* Retrieval-Augmented Generation (RAG) components

*Actual model availability and external service functionality depend on the project's configuration and required model files, credentials, and data sources.*

## 📁 Project Structure

```text
Smart-Kisan/
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── ml/
│   │   ├── models/
│   │   ├── routers/
│   │   ├── schemas/
│   │   └── core/
│   ├── pyproject.toml
│   └── requirements.txt
├── database/
├── docs/
├── frontend/
│   ├── public/
│   ├── src/
│   ├── package.json
│   └── vite.config.js
├── scripts/
├── .env.example
├── .gitignore
└── README.md
```

## 🚀 Getting Started

### Prerequisites

Install the following before running the application:

* Git
* Node.js and npm
* A compatible Python version for the backend
* Required API credentials for any external services you want to use

### 1. Clone the Repository

```bash
git clone https://github.com/SamarthThakar/Smart-Kisan.git
cd Smart-Kisan
```

### 2. Configure Environment Variables

Review `.env.example` and configure the environment variables required by the application.

Create the appropriate local environment file based on the project's configuration. Never commit real API keys, passwords, or other secrets.

### 3. Start the Backend

Open a terminal in the project root.

Create a Python virtual environment:

```powershell
cd backend
python -m venv venv
```

Activate it in Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

If activation is blocked by your PowerShell execution policy, use the appropriate approved policy for your system or run the environment's Python executable directly.

Install dependencies:

```powershell
pip install -r requirements.txt
```

Start the FastAPI development server:

```powershell
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

API documentation:

* Swagger UI: http://127.0.0.1:8000/docs
* ReDoc: http://127.0.0.1:8000/redoc

Keep this terminal running while using the backend.

### 4. Start the Frontend

Open a second terminal in the project root:

```powershell
cd frontend
npm install
npm run dev
```

Open the local application at:

http://localhost:5173

Keep the frontend terminal running while using the application.

## 📚 Documentation

Additional project documents are available in the `docs/` directory, including project documentation, a project report, and a technical/viva guide.

## 🔐 Security Notes

* Keep API keys and passwords out of Git.
* Do not commit `.env` files containing secrets.
* Keep `.env.example` limited to placeholder values.
* Verify third-party API credentials and model files before deployment.

## ⚠️ Disclaimer

Smart Kisan is intended to support agricultural decision-making. AI-generated crop recommendations, disease assessments, weather-based advice, and market information should be verified with reliable agricultural sources or qualified local experts before making important farming decisions.

## 👨‍💻 Project Repository

GitHub: https://github.com/SamarthThakar/Smart-Kisan

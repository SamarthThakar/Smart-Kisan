"""Smart Kisan Backend - FastAPI Application"""
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
import os

from app.config import settings
from app.database import engine, Base
from app.routers import auth, disease, crop, weather, market, schemes, chat, history

# Create all database tables on startup
Base.metadata.create_all(bind=engine)

# Rate limiter
limiter = Limiter(key_func=get_remote_address)

app = FastAPI(
    title="Smart Kisan API",
    description="AI-Powered Smart Farming Assistant — Backend API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

@app.on_event("startup")
def startup_event():
    try:
        import sys
        backend_parent = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        if backend_parent not in sys.path:
            sys.path.insert(0, backend_parent)
        from database.seed_schemes import seed_schemes
        seed_schemes()
    except Exception as e:
        print(f"[WARN] Startup seeding notice: {e}")

# Rate limiting
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# CORS - Allow frontend to call backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL, "http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve uploaded images as static files
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=settings.UPLOAD_DIR), name="uploads")

# Register all routers
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(disease.router, prefix="/api/v1/predict", tags=["Disease Detection"])
app.include_router(crop.router, prefix="/api/v1/recommend", tags=["Crop Recommendation"])
app.include_router(weather.router, prefix="/api/v1/weather", tags=["Weather Advisory"])
app.include_router(market.router, prefix="/api/v1/market", tags=["Market Prices"])
app.include_router(schemes.router, prefix="/api/v1/schemes", tags=["Government Schemes"])
app.include_router(chat.router, prefix="/api/v1/chat", tags=["AI Assistant"])
app.include_router(history.router, prefix="/api/v1/history", tags=["History"])


@app.get("/", tags=["Health"])
async def root():
    return {
        "message": "🌾 Smart Kisan API is running!",
        "version": "1.0.0",
        "docs": "/docs",
        "status": "healthy"
    }


@app.get("/api/v1/health", tags=["Health"])
async def health_check():
    return {
        "status": "healthy",
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "database": "connected"
    }

"""Application configuration using Pydantic Settings"""
from pydantic_settings import BaseSettings
from functools import lru_cache
import os


BACKEND_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_DB_PATH = os.path.join(BACKEND_DIR, "smart_kisan.db").replace("\\", "/")


class Settings(BaseSettings):
    # Application
    APP_NAME: str = "Smart Kisan"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True

    # Database
    DATABASE_URL: str = f"sqlite:///{DEFAULT_DB_PATH}"

    # JWT
    SECRET_KEY: str = "dev_secret_key_change_in_production_please"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440  # 24 hours

    # Google Gemini AI
    GEMINI_API_KEY: str = ""

    # Weather API (Open-Meteo - no key needed)
    WEATHER_API_BASE_URL: str = "https://api.open-meteo.com/v1"

    # Market Price API (data.gov.in)
    DATA_GOV_API_KEY: str = ""
    DATA_GOV_RESOURCE_ID: str = "9ef84268-d588-465a-a308-a864a43d0070"

    # ML Model paths
    DISEASE_MODEL_PATH: str = "../models/disease_model.keras"
    DISEASE_CLASSES_PATH: str = "../models/class_names.json"
    CROP_MODEL_PATH: str = "../models/crop_model.joblib"
    CROP_SCALER_PATH: str = "../models/crop_scaler.joblib"
    CROP_ENCODER_PATH: str = "../models/crop_label_encoder.joblib"
    CHROMA_DB_PATH: str = "../models/chroma_db"

    # File Upload
    MAX_UPLOAD_SIZE_MB: int = 10
    ALLOWED_IMAGE_TYPES: str = "image/jpeg,image/png,image/webp"
    UPLOAD_DIR: str = "./uploads"

    # Frontend
    FRONTEND_URL: str = "http://localhost:5173"

    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()

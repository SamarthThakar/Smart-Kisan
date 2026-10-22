"""Crop Recommendation ML model loading and inference"""
from pathlib import Path
from typing import Optional, List
import numpy as np

from app.config import settings

_crop_model = None
_crop_scaler = None
_crop_encoder = None


def get_crop_model():
    """Load Random Forest model lazily on first call"""
    global _crop_model, _crop_scaler, _crop_encoder
    
    if _crop_model is not None:
        return {"model": _crop_model, "scaler": _crop_scaler, "encoder": _crop_encoder}
    
    model_path = Path(settings.CROP_MODEL_PATH)
    scaler_path = Path(settings.CROP_SCALER_PATH)
    encoder_path = Path(settings.CROP_ENCODER_PATH)
    
    if not model_path.exists():
        print(f"⚠️  Crop model not found at {model_path}. Running in demo mode.")
        return None
    
    try:
        import joblib
        print(f"Loading crop model from {model_path}...")
        _crop_model = joblib.load(str(model_path))
        _crop_scaler = joblib.load(str(scaler_path)) if scaler_path.exists() else None
        _crop_encoder = joblib.load(str(encoder_path)) if encoder_path.exists() else None
        print("✅ Crop recommendation model loaded successfully!")
        return {"model": _crop_model, "scaler": _crop_scaler, "encoder": _crop_encoder}
    except Exception as e:
        print(f"❌ Failed to load crop model: {e}")
        return None


def predict_crops(model_data: dict, features: List[float]) -> List[dict]:
    """
    Predict top 5 crop recommendations.
    features: [N, P, K, pH, temperature, humidity, rainfall]
    """
    model = model_data["model"]
    scaler = model_data["scaler"]
    encoder = model_data["encoder"]
    
    X = np.array(features).reshape(1, -1)
    
    if scaler:
        X = scaler.transform(X)
    
    # Get probability for all classes
    proba = model.predict_proba(X)[0]
    
    # Get top 5 indices
    top5_indices = np.argsort(proba)[-5:][::-1]
    
    results = []
    for idx in top5_indices:
        crop_name = encoder.classes_[idx] if encoder else f"crop_{idx}"
        results.append({
            "crop": crop_name,
            "confidence": float(proba[idx])
        })
    
    return results

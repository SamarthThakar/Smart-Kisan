"""ML model loading and inference for disease detection"""
import json
import numpy as np
from pathlib import Path
from io import BytesIO
from typing import Optional, List, Tuple
import os

from app.config import settings

# Lazy-loaded model (loaded on first request, not at startup)
_disease_model = None
_class_names = None


def get_disease_model():
    """Load EfficientNetB3 model lazily on first call"""
    global _disease_model, _class_names
    
    if _disease_model is not None:
        return _disease_model
    
    model_path = Path(settings.DISEASE_MODEL_PATH)
    classes_path = Path(settings.DISEASE_CLASSES_PATH)
    
    if not model_path.exists():
        print(f"⚠️  Disease model not found at {model_path}. Running in demo mode.")
        return None
    
    try:
        import tensorflow as tf
        print(f"Loading disease model from {model_path}...")
        _disease_model = tf.keras.models.load_model(str(model_path))
        
        if classes_path.exists():
            with open(classes_path, 'r') as f:
                _class_names = json.load(f)
        else:
            print(f"⚠️  Class names file not found at {classes_path}")
            _class_names = [f"class_{i}" for i in range(38)]
        
        print(f"✅ Disease model loaded successfully! Classes: {len(_class_names)}")
        return _disease_model
    except Exception as e:
        print(f"❌ Failed to load disease model: {e}")
        return None


def predict_disease_from_bytes(model, image_bytes: bytes) -> List[dict]:
    """
    Run disease prediction on image bytes.
    Returns list of top-3 predictions with class key and confidence.
    """
    from PIL import Image
    import tensorflow as tf
    
    # Load and preprocess image
    img = Image.open(BytesIO(image_bytes)).convert('RGB')
    img = img.resize((224, 224))
    img_array = np.array(img, dtype=np.float32)
    
    # EfficientNetB3 preprocessing (ImageNet normalization)
    img_array = tf.keras.applications.efficientnet.preprocess_input(img_array)
    img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension
    
    # Predict
    predictions = model.predict(img_array, verbose=0)[0]
    
    # Get top-3 predictions
    top3_indices = np.argsort(predictions)[-3:][::-1]
    
    results = [
        {
            "class_key": _class_names[idx] if _class_names else f"class_{idx}",
            "confidence": float(predictions[idx])
        }
        for idx in top3_indices
    ]
    
    return results

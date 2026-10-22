"""Disease Detection Router — EfficientNetB3 inference"""
import os
import uuid
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Request
from sqlalchemy.orm import Session
from slowapi import Limiter
from slowapi.util import get_remote_address

from app.database import get_db
from app.models import DiseasePrediction, User
from app.core.security import get_current_user
from app.ml.disease_model import get_disease_model, predict_disease_from_bytes
from app.config import settings

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)

ALLOWED_TYPES = {"image/jpeg", "image/png", "image/webp", "image/jpg"}
MAX_SIZE = settings.MAX_UPLOAD_SIZE_MB * 1024 * 1024  # Convert MB to bytes

# Disease treatment database (simplified subset — extend as needed)
DISEASE_INFO = {
    "Tomato___Late_blight": {
        "display_name": "Tomato Late Blight",
        "severity": "high",
        "description": "Caused by Phytophthora infestans. Spreads rapidly in cool, wet conditions.",
        "treatment": [
            "Remove and destroy infected plant parts immediately",
            "Apply copper-based fungicide (Bordeaux mixture) or mancozeb",
            "Ensure good air circulation between plants",
            "Avoid overhead irrigation — use drip irrigation instead"
        ],
        "prevention": [
            "Use certified disease-resistant varieties",
            "Avoid working in the field when plants are wet",
            "Rotate crops — don't plant tomatoes in the same spot every year",
            "Monitor crops regularly during cool, humid weather"
        ]
    },
    "Tomato___Early_blight": {
        "display_name": "Tomato Early Blight",
        "severity": "medium",
        "description": "Caused by Alternaria solani. Common in warm, humid conditions.",
        "treatment": [
            "Remove infected lower leaves",
            "Apply fungicide containing chlorothalonil or mancozeb",
            "Mulch around plants to prevent soil splash"
        ],
        "prevention": [
            "Maintain proper plant spacing for airflow",
            "Avoid overhead watering",
            "Use mulch to reduce soil splash"
        ]
    },
    "Tomato___healthy": {
        "display_name": "Healthy Tomato Plant",
        "severity": "none",
        "description": "Your plant appears healthy! No disease detected.",
        "treatment": ["Continue regular care and monitoring"],
        "prevention": [
            "Water consistently at the base",
            "Feed with balanced fertilizer",
            "Monitor weekly for early signs of disease"
        ]
    },
    "Potato___Late_blight": {
        "display_name": "Potato Late Blight",
        "severity": "high",
        "description": "Same pathogen as tomato late blight. Can destroy entire crop in days.",
        "treatment": [
            "Apply fungicide immediately (metalaxyl + mancozeb)",
            "Remove badly infected plants",
            "Hill up soil around plants to protect tubers"
        ],
        "prevention": [
            "Use certified disease-free seed potatoes",
            "Plant resistant varieties",
            "Ensure good drainage"
        ]
    },
    "Corn_(maize)___Common_rust_": {
        "display_name": "Corn Common Rust",
        "severity": "medium",
        "description": "Caused by Puccinia sorghi. Orange-red pustules on leaves.",
        "treatment": [
            "Apply fungicide (propiconazole or tebuconazole) at first sign",
            "Ensure adequate plant nutrition"
        ],
        "prevention": [
            "Plant rust-resistant hybrid varieties",
            "Early planting to avoid peak rust season"
        ]
    },
    "Rice___Leaf_scald": {
        "display_name": "Rice Leaf Scald",
        "severity": "medium",
        "description": "Fungal disease causing yellowing and brown lesions.",
        "treatment": ["Apply tricyclazole or carbendazim fungicide"],
        "prevention": ["Use resistant varieties", "Avoid excess nitrogen fertilization"]
    },
}

# Default info for unknown diseases
DEFAULT_DISEASE_INFO = {
    "severity": "unknown",
    "description": "Disease detected. Please consult your local agricultural extension officer for specific treatment.",
    "treatment": ["Consult a local agricultural expert", "Remove and destroy infected plant material", "Avoid spreading by cleaning tools"],
    "prevention": ["Use resistant varieties", "Practice crop rotation", "Maintain field hygiene"]
}


@router.post("/disease")
@limiter.limit("10/minute")
async def predict_disease(
    request: Request,
    image: UploadFile = File(..., description="Leaf image (JPG/PNG/WebP, max 10MB)"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Detect crop disease from a leaf image using EfficientNetB3.
    Returns top-3 predictions with treatment recommendations.
    """
    # Validate file type
    if image.content_type not in ALLOWED_TYPES:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type '{image.content_type}'. Please upload JPG, PNG, or WebP."
        )

    # Read file contents
    contents = await image.read()

    # Validate file size
    if len(contents) > MAX_SIZE:
        raise HTTPException(
            status_code=413,
            detail=f"File too large. Maximum size is {settings.MAX_UPLOAD_SIZE_MB}MB."
        )

    # Verify it's actually an image using magic bytes
    if not _is_valid_image_bytes(contents):
        raise HTTPException(
            status_code=400,
            detail="File does not appear to be a valid image. Please upload a clear leaf photograph."
        )

    # Save image
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    file_ext = image.filename.split('.')[-1].lower() if image.filename else 'jpg'
    filename = f"{uuid.uuid4()}.{file_ext}"
    filepath = os.path.join(settings.UPLOAD_DIR, filename)

    with open(filepath, 'wb') as f:
        f.write(contents)

    # Run inference
    model = get_disease_model()
    
    if model is None:
        # Model not loaded yet — return mock response for demo
        predictions = _get_mock_predictions()
        is_mock = True
    else:
        try:
            predictions = predict_disease_from_bytes(model, contents)
            is_mock = False
        except Exception as e:
            predictions = _get_mock_predictions()
            is_mock = True

    # Enrich with disease info
    top_disease_key = predictions[0]["class_key"]
    top_confidence = predictions[0]["confidence"]

    disease_info = DISEASE_INFO.get(top_disease_key, DEFAULT_DISEASE_INFO)
    display_name = disease_info.get("display_name", top_disease_key.replace("___", " - ").replace("_", " "))

    # Build full response
    result = {
        "status": "success",
        "predictions": [
            {
                "disease": DISEASE_INFO.get(p["class_key"], {}).get("display_name", 
                    p["class_key"].replace("___", " - ").replace("_", " ")),
                "class_key": p["class_key"],
                "confidence": round(p["confidence"], 4),
                "confidence_percent": f"{p['confidence']*100:.1f}%"
            }
            for p in predictions
        ],
        "primary_diagnosis": {
            "disease": display_name,
            "confidence": top_confidence,
            "severity": disease_info.get("severity", "unknown"),
            "description": disease_info.get("description", ""),
            "treatment": disease_info.get("treatment", []),
            "prevention": disease_info.get("prevention", [])
        },
        "disclaimer": (
            f"⚠️ This is an AI prediction with {top_confidence*100:.1f}% confidence. "
            "Results should be used as a guide only. For serious crop disease outbreaks, "
            "always consult your local Krishi Vigyan Kendra (KVK) or agricultural extension officer."
        ),
        "is_demo_mode": is_mock,
        "image_url": f"/uploads/{filename}"
    }

    # Save to database
    prediction_record = DiseasePrediction(
        user_id=current_user.id,
        image_path=filepath,
        disease_name=display_name,
        confidence=top_confidence,
        top3_results=predictions,
        treatment_shown=disease_info.get("treatment", []),
        crop_type=top_disease_key.split("___")[0] if "___" in top_disease_key else None,
    )
    db.add(prediction_record)
    db.commit()
    db.refresh(prediction_record)

    result["prediction_id"] = prediction_record.id
    return result


@router.get("/disease/history")
async def get_disease_history(
    limit: int = 10,
    offset: int = 0,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get disease prediction history for current user"""
    total = db.query(DiseasePrediction).filter(DiseasePrediction.user_id == current_user.id).count()
    predictions = (
        db.query(DiseasePrediction)
        .filter(DiseasePrediction.user_id == current_user.id)
        .order_by(DiseasePrediction.created_at.desc())
        .limit(limit)
        .offset(offset)
        .all()
    )
    return {
        "total": total,
        "predictions": [
            {
                "id": p.id,
                "disease_name": p.disease_name,
                "confidence": p.confidence,
                "crop_type": p.crop_type,
                "created_at": p.created_at.isoformat(),
                "image_url": f"/uploads/{os.path.basename(p.image_path)}" if p.image_path else None
            }
            for p in predictions
        ]
    }


def _is_valid_image_bytes(data: bytes) -> bool:
    """Verify image magic bytes to prevent malicious uploads"""
    magic_bytes = {
        b'\xff\xd8\xff': 'JPEG',
        b'\x89PNG': 'PNG',
        b'RIFF': 'WebP',  # WebP starts with RIFF
    }
    for magic, fmt in magic_bytes.items():
        if data[:len(magic)] == magic:
            return True
    return False


def _get_mock_predictions():
    """Return mock predictions when model is not loaded (demo mode)"""
    return [
        {"class_key": "Tomato___Late_blight", "confidence": 0.8734},
        {"class_key": "Tomato___Early_blight", "confidence": 0.0821},
        {"class_key": "Tomato___healthy", "confidence": 0.0217},
    ]

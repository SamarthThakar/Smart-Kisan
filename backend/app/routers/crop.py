"""Crop Recommendation Router — Random Forest inference"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from typing import Optional

from app.database import get_db
from app.models import CropRecommendation, User
from app.core.security import get_current_user
from app.ml.crop_model import get_crop_model, predict_crops

router = APIRouter()

# Crop descriptions and metadata
CROP_INFO = {
    "rice": {"water": "high", "season": "kharif", "demand": "high", "description": "Staple cereal crop. Best for waterlogged/clayey soils."},
    "maize": {"water": "medium", "season": "kharif/rabi", "demand": "high", "description": "Versatile cereal crop for food, fodder, and industry."},
    "chickpea": {"water": "low", "season": "rabi", "demand": "high", "description": "Protein-rich pulse. Suitable for dry, light soils."},
    "kidneybeans": {"water": "medium", "season": "kharif", "demand": "medium", "description": "High-value pulse crop."},
    "pigeonpeas": {"water": "low", "season": "kharif", "demand": "medium", "description": "Drought-tolerant pulse. Good for dry regions."},
    "mothbeans": {"water": "very_low", "season": "kharif", "demand": "medium", "description": "Extremely drought-tolerant. Suited for arid zones."},
    "mungbean": {"water": "low", "season": "kharif/zaid", "demand": "high", "description": "Short-duration pulse. Good intercrop option."},
    "blackgram": {"water": "low", "season": "kharif/rabi", "demand": "high", "description": "Popular pulse with strong market demand."},
    "lentil": {"water": "low", "season": "rabi", "demand": "high", "description": "Cool-season pulse rich in protein."},
    "pomegranate": {"water": "low", "season": "perennial", "demand": "very_high", "description": "High-value fruit. Drought-tolerant once established."},
    "banana": {"water": "high", "season": "perennial", "demand": "high", "description": "Year-round fruit crop requiring consistent moisture."},
    "mango": {"water": "medium", "season": "perennial", "demand": "very_high", "description": "India's most popular fruit. Long-term investment."},
    "grapes": {"water": "medium", "season": "perennial", "demand": "high", "description": "High-value fruit requiring careful management."},
    "watermelon": {"water": "medium", "season": "zaid/summer", "demand": "high", "description": "Fast-growing summer crop with good returns."},
    "muskmelon": {"water": "medium", "season": "zaid", "demand": "medium", "description": "Sweet fruit with good demand in summer."},
    "apple": {"water": "medium", "season": "perennial", "demand": "very_high", "description": "High-value temperate fruit."},
    "orange": {"water": "medium", "season": "perennial", "demand": "high", "description": "Popular citrus fruit with year-round demand."},
    "papaya": {"water": "medium", "season": "perennial", "demand": "medium", "description": "Fast-growing fruit, starts bearing in 9-12 months."},
    "coconut": {"water": "high", "season": "perennial", "demand": "high", "description": "Long-term crop, multiple uses including copra and oil."},
    "cotton": {"water": "medium", "season": "kharif", "demand": "high", "description": "Cash crop. High market value but requires careful management."},
    "jute": {"water": "high", "season": "kharif", "demand": "medium", "description": "Fiber crop best suited for humid regions."},
    "coffee": {"water": "medium", "season": "perennial", "demand": "high", "description": "High-value plantation crop. Requires specific climate."},
}


class CropInput(BaseModel):
    N: float = Field(..., ge=0, le=200, description="Nitrogen content in soil (kg/ha)")
    P: float = Field(..., ge=0, le=200, description="Phosphorus content (kg/ha)")
    K: float = Field(..., ge=0, le=200, description="Potassium content (kg/ha)")
    pH: float = Field(..., ge=0, le=14, description="Soil pH value")
    temperature: float = Field(..., ge=-10, le=60, description="Temperature in °C")
    humidity: float = Field(..., ge=0, le=100, description="Relative humidity %")
    rainfall: float = Field(..., ge=0, le=5000, description="Annual rainfall in mm")
    state: Optional[str] = Field(None, description="State name for context")
    season: Optional[str] = Field(None, pattern="^(kharif|rabi|zaid|perennial)?$")


@router.post("/crop")
async def recommend_crop(
    crop_input: CropInput,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Recommend suitable crops using Random Forest classifier.
    Input: Soil NPK, pH, climate parameters.
    Output: Top 5 crop recommendations with suitability score.
    """
    model_data = get_crop_model()
    
    features = [crop_input.N, crop_input.P, crop_input.K, crop_input.pH,
                crop_input.temperature, crop_input.humidity, crop_input.rainfall]
    
    if model_data is None:
        # Demo mode — rule-based fallback
        predictions = _rule_based_crop_recommendation(crop_input)
        is_demo = True
    else:
        try:
            predictions = predict_crops(model_data, features)
            is_demo = False
        except Exception as e:
            predictions = _rule_based_crop_recommendation(crop_input)
            is_demo = True

    # Enrich predictions with crop info
    enriched = []
    for pred in predictions[:5]:
        crop_name = pred["crop"].lower()
        info = CROP_INFO.get(crop_name, {})
        enriched.append({
            "rank": len(enriched) + 1,
            "crop": pred["crop"].capitalize(),
            "confidence": round(pred["confidence"], 4),
            "suitability_percent": f"{pred['confidence']*100:.1f}%",
            "water_requirement": info.get("water", "medium"),
            "best_season": info.get("season", "kharif"),
            "market_demand": info.get("demand", "medium"),
            "description": info.get("description", "Suitable crop for your conditions."),
        })

    # Save to database
    recommendation_record = CropRecommendation(
        user_id=current_user.id,
        input_params={
            "N": crop_input.N, "P": crop_input.P, "K": crop_input.K,
            "pH": crop_input.pH, "temperature": crop_input.temperature,
            "humidity": crop_input.humidity, "rainfall": crop_input.rainfall
        },
        recommended_crops=enriched,
        location=crop_input.state,
        season=crop_input.season,
    )
    db.add(recommendation_record)
    db.commit()
    db.refresh(recommendation_record)

    return {
        "status": "success",
        "recommendation_id": recommendation_record.id,
        "input_summary": {
            "soil": f"N:{crop_input.N}, P:{crop_input.P}, K:{crop_input.K}, pH:{crop_input.pH}",
            "climate": f"{crop_input.temperature}°C, {crop_input.humidity}% humidity, {crop_input.rainfall}mm rain",
            "location": crop_input.state or "Not specified"
        },
        "recommended_crops": enriched,
        "is_demo_mode": is_demo,
        "note": "Rankings based on soil and climate compatibility. Market conditions may also influence your final choice."
    }


def _rule_based_crop_recommendation(inp: CropInput):
    """Simple rule-based fallback when ML model is unavailable"""
    crops = []
    
    # Rice: needs high water, high N, high humidity
    if inp.rainfall > 150 and inp.humidity > 70 and inp.temperature > 20:
        crops.append({"crop": "Rice", "confidence": 0.85})
    
    # Cotton: medium water, moderate N, high temp
    if 20 < inp.temperature < 40 and inp.rainfall > 50:
        crops.append({"crop": "Cotton", "confidence": 0.75})
    
    # Chickpea: low water, cool temp
    if inp.temperature < 25 and inp.rainfall < 100:
        crops.append({"crop": "Chickpea", "confidence": 0.70})
    
    # Maize: medium everything
    crops.append({"crop": "Maize", "confidence": 0.65})
    crops.append({"crop": "Mungbean", "confidence": 0.55})
    
    return crops[:5] if crops else [{"crop": "Maize", "confidence": 0.6}, {"crop": "Rice", "confidence": 0.5}]

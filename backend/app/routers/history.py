"""History Router — Combined prediction history"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional

from app.database import get_db
from app.models import DiseasePrediction, CropRecommendation, User
from app.core.security import get_current_user

router = APIRouter()


@router.get("")
async def get_history(
    type: str = Query("all", pattern="^(all|disease|crop)$"),
    limit: int = Query(20, le=50),
    offset: int = 0,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get combined prediction history for the current user"""
    history_items = []

    if type in ("all", "disease"):
        diseases = (
            db.query(DiseasePrediction)
            .filter(DiseasePrediction.user_id == current_user.id)
            .order_by(DiseasePrediction.created_at.desc())
            .limit(limit)
            .all()
        )
        for d in diseases:
            history_items.append({
                "id": d.id,
                "type": "disease",
                "title": d.disease_name,
                "subtitle": f"{d.confidence*100:.1f}% confidence | {d.crop_type or 'Unknown crop'}",
                "icon": "🔬",
                "created_at": d.created_at.isoformat(),
                "data": {
                    "disease": d.disease_name,
                    "confidence": d.confidence,
                    "crop_type": d.crop_type,
                }
            })

    if type in ("all", "crop"):
        crops = (
            db.query(CropRecommendation)
            .filter(CropRecommendation.user_id == current_user.id)
            .order_by(CropRecommendation.created_at.desc())
            .limit(limit)
            .all()
        )
        for c in crops:
            top_crop = c.recommended_crops[0]["crop"] if c.recommended_crops else "Unknown"
            history_items.append({
                "id": c.id,
                "type": "crop",
                "title": f"Top recommendation: {top_crop}",
                "subtitle": c.location or "Location not specified",
                "icon": "🌾",
                "created_at": c.created_at.isoformat(),
                "data": {
                    "top_crop": top_crop,
                    "location": c.location,
                    "season": c.season,
                    "input_params": c.input_params,
                }
            })

    # Sort combined history by date
    history_items.sort(key=lambda x: x["created_at"], reverse=True)
    
    return {
        "total": len(history_items),
        "history": history_items[offset:offset+limit]
    }

"""Government Schemes Router — Database filtering + search"""
from fastapi import APIRouter, Query, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy import or_, func
from typing import Optional

from app.database import get_db
from app.models import GovernmentScheme

router = APIRouter()


@router.get("")
async def get_schemes(
    state: Optional[str] = Query(None, description="Filter by state e.g. Maharashtra"),
    crop: Optional[str] = Query(None, description="Filter by crop e.g. rice"),
    category: Optional[str] = Query(None, description="Farmer category: small/marginal/medium"),
    scheme_type: Optional[str] = Query(None, description="Type: insurance/subsidy/credit/training"),
    q: Optional[str] = Query(None, description="Search query for scheme name/description"),
    limit: int = Query(20, le=50),
    offset: int = 0,
    db: Session = Depends(get_db)
):
    """
    Get government agricultural schemes with filtering and search.
    Schemes are curated from official government sources.
    """
    query = db.query(GovernmentScheme).filter(GovernmentScheme.is_active == True)

    # Text search on scheme name and description
    if q:
        search_term = f"%{q.lower()}%"
        query = query.filter(
            or_(
                func.lower(GovernmentScheme.scheme_name).like(search_term),
                func.lower(GovernmentScheme.short_name).like(search_term),
                func.lower(GovernmentScheme.description).like(search_term),
            )
        )

    # Filter by scheme type
    if scheme_type:
        query = query.filter(GovernmentScheme.scheme_type == scheme_type.lower())

    total = query.count()
    schemes = query.limit(limit).offset(offset).all()

    # Client-side state/crop/category filtering (JSON field filtering)
    filtered = []
    for scheme in schemes:
        # Check state filter
        if state and scheme.applicable_states:
            states = scheme.applicable_states
            if "ALL" not in states and state.upper()[:2] not in [s.upper() for s in states]:
                if state.lower() not in [s.lower() for s in states]:
                    continue

        # Check crop filter
        if crop and scheme.applicable_crops:
            crops = [c.lower() for c in scheme.applicable_crops]
            if "all" not in crops and crop.lower() not in crops:
                continue

        # Check farmer category
        if category and scheme.farmer_categories:
            categories = [c.lower() for c in scheme.farmer_categories]
            if "all" not in categories and category.lower() not in categories:
                continue

        filtered.append({
            "id": scheme.id,
            "scheme_name": scheme.scheme_name,
            "short_name": scheme.short_name,
            "ministry": scheme.ministry,
            "scheme_type": scheme.scheme_type,
            "description": scheme.description,
            "benefits": scheme.benefits,
            "benefit_summary": scheme.benefits[0] if scheme.benefits else (scheme.description or "See details"),
            "eligibility_criteria": scheme.eligibility_criteria,
            "required_documents": scheme.required_documents,
            "official_url": scheme.official_url,
            "applicable_states": scheme.applicable_states,
            "applicable_crops": scheme.applicable_crops,
            "farmer_categories": scheme.farmer_categories,
            "is_national": "ALL" in (scheme.applicable_states or []),
        })

    return {
        "total": len(filtered),
        "schemes": filtered,
        "filters_applied": {
            "state": state,
            "crop": crop,
            "category": category,
            "scheme_type": scheme_type,
            "search": q
        }
    }


@router.get("/types")
async def get_scheme_types():
    """Get available scheme types for filtering"""
    return {
        "types": [
            {"key": "insurance", "label": "Crop Insurance", "icon": "🛡️"},
            {"key": "subsidy", "label": "Subsidies & Grants", "icon": "💰"},
            {"key": "credit", "label": "Credit & Loans", "icon": "🏦"},
            {"key": "training", "label": "Training & Extension", "icon": "📚"},
            {"key": "market", "label": "Market Linkage", "icon": "📈"},
            {"key": "irrigation", "label": "Irrigation Support", "icon": "💧"},
            {"key": "organic", "label": "Organic Farming", "icon": "🌿"},
        ]
    }


@router.get("/{scheme_id}")
async def get_scheme_detail(
    scheme_id: str,
    db: Session = Depends(get_db)
):
    """Get full details of a specific government scheme"""
    scheme = db.query(GovernmentScheme).filter(
        GovernmentScheme.id == scheme_id,
        GovernmentScheme.is_active == True
    ).first()

    if not scheme:
        raise HTTPException(status_code=404, detail="Scheme not found")

    return {
        "id": scheme.id,
        "scheme_name": scheme.scheme_name,
        "short_name": scheme.short_name,
        "ministry": scheme.ministry,
        "scheme_type": scheme.scheme_type,
        "description": scheme.description,
        "benefits": scheme.benefits,
        "eligibility_criteria": scheme.eligibility_criteria,
        "applicable_states": scheme.applicable_states,
        "applicable_crops": scheme.applicable_crops,
        "farmer_categories": scheme.farmer_categories,
        "max_land_acres": scheme.max_land_acres,
        "required_documents": scheme.required_documents,
        "application_mode": scheme.application_mode,
        "official_url": scheme.official_url,
        "last_verified": scheme.last_verified.isoformat() if scheme.last_verified else None,
        "disclaimer": "Scheme details verified from official government sources. Always check the official website for the most current eligibility criteria."
    }

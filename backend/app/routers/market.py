"""Market Prices Router — data.gov.in API + Mock fallback"""
import httpx
import json
from datetime import date, datetime
from fastapi import APIRouter, Query, HTTPException, Depends
from sqlalchemy.orm import Session
from pathlib import Path

from app.database import get_db
from app.models import MarketPrice
from app.config import settings

router = APIRouter()

COMMODITIES = [
    "Rice", "Wheat", "Maize", "Cotton", "Sugarcane", "Soybean",
    "Groundnut", "Onion", "Potato", "Tomato", "Chilli", "Turmeric",
    "Cumin", "Mustard", "Bajra", "Jowar", "Chickpea", "Lentil",
    "Mungbean", "Arhar", "Banana", "Mango", "Pomegranate"
]


@router.get("/commodities")
async def get_commodities():
    """Get list of available commodities"""
    return {"commodities": sorted(COMMODITIES)}


@router.get("/prices")
async def get_market_prices(
    commodity: str = Query(..., description="Commodity name e.g. Rice, Wheat"),
    state: str = Query(None, description="State name e.g. Maharashtra"),
    limit: int = Query(20, le=50),
    db: Session = Depends(get_db)
):
    """
    Get current mandi prices for a commodity.
    Tries data.gov.in API first, falls back to mock data if unavailable.
    """
    # Try live API first (only if API key is configured)
    if settings.DATA_GOV_API_KEY and settings.DATA_GOV_API_KEY != "REPLACE_WITH_DATA_GOV_API_KEY":
        try:
            data = await _fetch_live_prices(commodity, state, limit)
            if data:
                return {
                    "commodity": commodity,
                    "state": state or "All States",
                    "data_date": date.today().isoformat(),
                    "source": "data.gov.in (Live)",
                    "is_live": True,
                    "markets": data,
                    "trend": _calculate_trend(data)
                }
        except Exception as e:
            print(f"Live API failed: {e}, using mock data")

    # Fallback to mock data
    mock_data = _get_mock_prices(commodity, state)
    return {
        "commodity": commodity,
        "state": state or "All States",
        "data_date": date.today().isoformat(),
        "source": "Sample Data (Configure data.gov.in API for live prices)",
        "is_live": False,
        "markets": mock_data[:limit],
        "trend": _calculate_trend(mock_data),
        "notice": "Showing sample data. Register at data.gov.in to enable live market prices."
    }


async def _fetch_live_prices(commodity: str, state: str = None, limit: int = 20):
    """Fetch live prices from data.gov.in OGD API"""
    url = "https://api.data.gov.in/resource/9ef84268-d588-465a-a308-a864a43d0070"
    params = {
        "api-key": settings.DATA_GOV_API_KEY,
        "format": "json",
        "limit": limit,
        "filters[commodity]": commodity,
    }
    if state:
        params["filters[state]"] = state

    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.get(url, params=params)
        response.raise_for_status()
        data = response.json()

    records = data.get("records", [])
    formatted = []
    for r in records:
        formatted.append({
            "market": r.get("market", "Unknown"),
            "district": r.get("district", ""),
            "state": r.get("state", ""),
            "min_price": float(r.get("min_price", 0)),
            "max_price": float(r.get("max_price", 0)),
            "modal_price": float(r.get("modal_price", 0)),
            "unit": "₹/quintal",
            "variety": r.get("variety", ""),
            "arrival_date": r.get("arrival_date", ""),
        })
    
    # Mark best market (highest modal price)
    if formatted:
        max_modal = max(m["modal_price"] for m in formatted)
        for m in formatted:
            m["is_best_market"] = (m["modal_price"] == max_modal)
    
    return formatted


def _get_mock_prices(commodity: str, state: str = None):
    """Return realistic mock price data for demo purposes"""
    # Base prices per quintal (₹) for major commodities
    base_prices = {
        "Rice": 2100, "Wheat": 2200, "Maize": 1800, "Cotton": 6500,
        "Sugarcane": 350, "Soybean": 4200, "Groundnut": 5500,
        "Onion": 1200, "Potato": 1100, "Tomato": 1500,
        "Chilli": 8000, "Turmeric": 7500, "Cumin": 18000,
        "Mustard": 5200, "Bajra": 2100, "Jowar": 2100,
        "Chickpea": 4800, "Lentil": 5500, "Mungbean": 7200,
        "Arhar": 6200, "Banana": 1800, "Mango": 3500, "Pomegranate": 8500
    }
    
    base = base_prices.get(commodity, 2000)
    
    markets = [
        {"market": "Pune APMC", "district": "Pune", "state_name": "Maharashtra"},
        {"market": "Nashik Market", "district": "Nashik", "state_name": "Maharashtra"},
        {"market": "Nagpur Mandi", "district": "Nagpur", "state_name": "Maharashtra"},
        {"market": "Amravati Mandi", "district": "Amravati", "state_name": "Maharashtra"},
        {"market": "Delhi Azadpur", "district": "Delhi", "state_name": "Delhi"},
        {"market": "Lucknow Mandi", "district": "Lucknow", "state_name": "Uttar Pradesh"},
        {"market": "Kanpur Mandi", "district": "Kanpur", "state_name": "Uttar Pradesh"},
        {"market": "Ludhiana Mandi", "district": "Ludhiana", "state_name": "Punjab"},
        {"market": "Amritsar Mandi", "district": "Amritsar", "state_name": "Punjab"},
        {"market": "Ahmedabad APMC", "district": "Ahmedabad", "state_name": "Gujarat"},
        {"market": "Rajkot Mandi", "district": "Rajkot", "state_name": "Gujarat"},
        {"market": "Hyderabad Market", "district": "Hyderabad", "state_name": "Telangana"},
        {"market": "Warangal Mandi", "district": "Warangal", "state_name": "Telangana"},
        {"market": "Bangalore APMC", "district": "Bangalore", "state_name": "Karnataka"},
        {"market": "Mysore Mandi", "district": "Mysore", "state_name": "Karnataka"},
    ]
    
    import random
    random.seed(42)  # Fixed seed for consistent demo data
    
    result = []
    max_modal = 0
    
    for m in markets:
        # Filter by state if specified
        if state and state.lower() not in m["state_name"].lower():
            continue
            
        # Add realistic price variation
        variation = random.uniform(0.85, 1.15)
        min_p = round(base * variation * 0.92)
        max_p = round(base * variation * 1.08)
        modal_p = round(base * variation)
        
        if modal_p > max_modal:
            max_modal = modal_p
        
        result.append({
            "market": m["market"],
            "district": m["district"],
            "state": m["state_name"],
            "min_price": min_p,
            "max_price": max_p,
            "modal_price": modal_p,
            "unit": "₹/quintal",
            "variety": "Common",
            "arrival_date": date.today().isoformat(),
            "is_best_market": False
        })
    
    # Mark best market
    for m in result:
        m["is_best_market"] = (m["modal_price"] == max_modal)
    
    # Sort by modal price descending
    result.sort(key=lambda x: x["modal_price"], reverse=True)
    return result


def _calculate_trend(markets: list) -> dict:
    """Calculate price trend from available data"""
    if not markets:
        return {"direction": "neutral", "change_percent": 0}
    
    modal_prices = [m["modal_price"] for m in markets if m.get("modal_price")]
    if not modal_prices:
        return {"direction": "neutral", "change_percent": 0}
    
    avg_price = sum(modal_prices) / len(modal_prices)
    max_price = max(modal_prices)
    spread = ((max_price - avg_price) / avg_price * 100) if avg_price > 0 else 0
    
    return {
        "average_modal_price": round(avg_price),
        "highest_price": max_price,
        "price_spread_percent": round(spread, 1),
        "direction": "up" if spread > 5 else "down" if spread < -5 else "stable"
    }

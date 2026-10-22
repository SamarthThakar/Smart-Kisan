"""Weather Advisory Router"""
import httpx
import json
from fastapi import APIRouter, HTTPException, Query
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from fastapi import Depends

from app.database import get_db
from app.models import WeatherCache
from app.config import settings
from app.utils.weather_rules import generate_farming_advice

router = APIRouter()


@router.get("")
async def get_weather(
    lat: float = Query(..., ge=-90, le=90, description="Latitude"),
    lon: float = Query(..., ge=-180, le=180, description="Longitude"),
    db: Session = Depends(get_db)
):
    """Get weather data and farming advice for a location"""
    lat_lon_key = f"{round(lat, 2)}_{round(lon, 2)}"

    # Check cache (valid for 6 hours)
    cached = db.query(WeatherCache).filter(
        WeatherCache.lat_lon_key == lat_lon_key,
        WeatherCache.expires_at > datetime.utcnow()
    ).first()

    if cached:
        return cached.weather_data

    # Fetch from Open-Meteo (free, no API key!)
    url = f"{settings.WEATHER_API_BASE_URL}/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum,precipitation_probability_max,windspeed_10m_max,et0_fao_evapotranspiration,weathercode",
        "hourly": "relative_humidity_2m,soil_moisture_0_to_7cm",
        "current": "temperature_2m,relative_humidity_2m,apparent_temperature,precipitation,rain,windspeed_10m,weathercode",
        "timezone": "auto",
        "forecast_days": 7,
    }

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(url, params=params)
            response.raise_for_status()
            raw_data = response.json()
    except httpx.HTTPError as e:
        raise HTTPException(status_code=503, detail=f"Weather service unavailable: {str(e)}")

    # Process into farmer-friendly format
    farming_advice = generate_farming_advice(raw_data)
    
    # Build response
    current = raw_data.get("current", {})
    daily = raw_data.get("daily", {})
    
    def _format_day_name(date_str: str, index: int) -> str:
        if index == 0:
            return "Today"
        try:
            return datetime.strptime(date_str, "%Y-%m-%d").strftime("%a")
        except Exception:
            return f"+{index}d"

    forecast_list = []
    daily_times = daily.get("time", [])
    for i in range(min(7, len(daily_times))):
        d_date = daily_times[i]
        d_code = daily.get("weathercode", [0])[i] if daily.get("weathercode") and len(daily.get("weathercode")) > i else 0
        max_t = daily.get("temperature_2m_max", [None])[i] if daily.get("temperature_2m_max") and len(daily.get("temperature_2m_max")) > i else None
        min_t = daily.get("temperature_2m_min", [None])[i] if daily.get("temperature_2m_min") and len(daily.get("temperature_2m_min")) > i else None
        precip = daily.get("precipitation_sum", [None])[i] if daily.get("precipitation_sum") and len(daily.get("precipitation_sum")) > i else None
        rain_p = daily.get("precipitation_probability_max", [None])[i] if daily.get("precipitation_probability_max") and len(daily.get("precipitation_probability_max")) > i else None
        wind_s = daily.get("windspeed_10m_max", [None])[i] if daily.get("windspeed_10m_max") and len(daily.get("windspeed_10m_max")) > i else None
        et0 = daily.get("et0_fao_evapotranspiration", [None])[i] if daily.get("et0_fao_evapotranspiration") and len(daily.get("et0_fao_evapotranspiration")) > i else None

        forecast_list.append({
            "date": d_date,
            "day": _format_day_name(d_date, i),
            "max_temp": max_t,
            "temp_max": max_t,
            "min_temp": min_t,
            "temp_min": min_t,
            "precipitation": precip,
            "rain_probability": rain_p,
            "rain_prob": rain_p,
            "wind_speed": wind_s,
            "evapotranspiration": et0,
            "weather_code": d_code,
            "condition": get_weather_description(d_code),
        })

    weather_desc = get_weather_description(current.get("weathercode", 0))
    weather_response = {
        "location": {"latitude": lat, "longitude": lon},
        "timezone": raw_data.get("timezone", ""),
        "current": {
            "temperature": current.get("temperature_2m"),
            "feels_like": current.get("apparent_temperature"),
            "humidity": current.get("relative_humidity_2m"),
            "relative_humidity": current.get("relative_humidity_2m"),
            "precipitation": current.get("precipitation"),
            "wind_speed": current.get("windspeed_10m"),
            "weather_code": current.get("weathercode"),
            "conditions": weather_desc,
            "condition": weather_desc,
        },
        "forecast": forecast_list,
        "farming_advice": farming_advice,
        "alerts": farming_advice,
        "data_source": "Open-Meteo (open-meteo.com)",
        "last_updated": datetime.utcnow().isoformat()
    }

    # Cache for 6 hours
    cache_entry = db.query(WeatherCache).filter(WeatherCache.lat_lon_key == lat_lon_key).first()
    if cache_entry:
        cache_entry.weather_data = weather_response
        cache_entry.farming_advice = farming_advice
        cache_entry.expires_at = datetime.utcnow() + timedelta(hours=6)
    else:
        cache_entry = WeatherCache(
            lat_lon_key=lat_lon_key,
            weather_data=weather_response,
            farming_advice=farming_advice,
            expires_at=datetime.utcnow() + timedelta(hours=6)
        )
        db.add(cache_entry)
    db.commit()

    return weather_response


def get_weather_description(code: int) -> str:
    """Convert WMO weather code to human-readable description"""
    codes = {
        0: "Clear Sky", 1: "Mainly Clear", 2: "Partly Cloudy", 3: "Overcast",
        45: "Foggy", 48: "Icy Fog",
        51: "Light Drizzle", 53: "Moderate Drizzle", 55: "Dense Drizzle",
        61: "Slight Rain", 63: "Moderate Rain", 65: "Heavy Rain",
        71: "Slight Snowfall", 73: "Moderate Snowfall", 75: "Heavy Snowfall",
        80: "Slight Showers", 81: "Moderate Showers", 82: "Violent Showers",
        95: "Thunderstorm", 96: "Thunderstorm with Hail", 99: "Heavy Thunderstorm"
    }
    return codes.get(code, "Unknown")

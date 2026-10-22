"""Weather Rules Engine — Converts raw weather data into farming advice"""
from typing import List, Dict, Any


def generate_farming_advice(weather_data: Dict[str, Any]) -> List[Dict]:
    """
    Convert Open-Meteo API response into actionable farming advice.
    Returns list of advice objects with type, icon, title, message, action.
    """
    advice = []
    daily = weather_data.get("daily", {})
    current = weather_data.get("current", {})
    hourly = weather_data.get("hourly", {})

    # Get today's values
    today_rain_prob = _safe_get(daily, "precipitation_probability_max", 0)
    today_precipitation = _safe_get(daily, "precipitation_sum", 0)
    today_max_temp = _safe_get(daily, "temperature_2m_max", 25)
    today_min_temp = _safe_get(daily, "temperature_2m_min", 15)
    today_et0 = _safe_get(daily, "et0_fao_evapotranspiration", 4)

    current_temp = current.get("temperature_2m", 25)
    current_humidity = current.get("relative_humidity_2m", 60)

    # Soil moisture (average of today's hourly readings)
    soil_moisture_list = hourly.get("soil_moisture_0_to_7cm", [])
    avg_soil_moisture = sum(soil_moisture_list[:6]) / max(len(soil_moisture_list[:6]), 1) if soil_moisture_list else 0.3

    # --- IRRIGATION ADVICE ---
    if today_rain_prob > 70:
        advice.append({
            "type": "info",
            "icon": "🌧️",
            "title": "Rain Expected — Skip Irrigation",
            "message": f"High chance of rain ({today_rain_prob}%). Save water and delay irrigation today.",
            "action": "Delay irrigation by 1-2 days",
            "priority": "high"
        })
    elif avg_soil_moisture < 0.15:
        advice.append({
            "type": "urgent",
            "icon": "💧",
            "title": "Soil Moisture Very Low — Irrigate Now",
            "message": "Soil moisture is critically low. Plants may show drought stress. Irrigate immediately.",
            "action": "Irrigate immediately, preferably in early morning",
            "priority": "urgent"
        })
    elif avg_soil_moisture < 0.25 and today_rain_prob < 30:
        advice.append({
            "type": "warning",
            "icon": "💧",
            "title": "Irrigate Today",
            "message": f"Soil moisture is low ({avg_soil_moisture:.0%}) and no rain expected. Irrigate today.",
            "action": "Irrigate early morning or evening to reduce evaporation",
            "priority": "medium"
        })
    else:
        advice.append({
            "type": "success",
            "icon": "✅",
            "title": "Irrigation Not Needed",
            "message": "Soil moisture is adequate. No irrigation needed today.",
            "action": "Monitor soil moisture tomorrow",
            "priority": "low"
        })

    # --- TEMPERATURE ALERTS ---
    if today_max_temp > 40:
        advice.append({
            "type": "danger",
            "icon": "🌡️",
            "title": "Extreme Heat Warning",
            "message": f"Temperature expected to reach {today_max_temp}°C. Risk of heat stress for crops.",
            "action": "Irrigate early morning. Provide shade for sensitive crops. Avoid spraying pesticides.",
            "priority": "urgent"
        })
    elif today_max_temp > 35:
        advice.append({
            "type": "warning",
            "icon": "🔆",
            "title": "High Temperature Alert",
            "message": f"High temperature of {today_max_temp}°C expected. Monitor crop health.",
            "action": "Water crops early morning. Avoid fieldwork midday.",
            "priority": "medium"
        })

    if today_min_temp < 5:
        advice.append({
            "type": "danger",
            "icon": "❄️",
            "title": "Frost Risk Tonight",
            "message": f"Temperature may drop to {today_min_temp}°C. Risk of frost damage.",
            "action": "Cover sensitive crops. Light irrigation at night can protect against frost.",
            "priority": "urgent"
        })

    # --- DISEASE RISK (based on humidity + temperature) ---
    # Fungal disease conditions: high humidity + moderate temperature
    if current_humidity > 80 and 18 <= current_temp <= 28:
        advice.append({
            "type": "warning",
            "icon": "🍄",
            "title": "High Fungal Disease Risk",
            "message": f"Current conditions (humidity {current_humidity}%, temp {current_temp}°C) are ideal for fungal diseases like blight, rust, and mildew.",
            "action": "Inspect crops for early signs of disease. Consider preventive fungicide if symptoms appear.",
            "priority": "medium"
        })
    elif current_humidity > 70 and today_precipitation > 5:
        advice.append({
            "type": "info",
            "icon": "👀",
            "title": "Monitor for Disease",
            "message": "Recent rain and moderate humidity create some disease risk. Check crops in the coming days.",
            "action": "Check crops for spots, discoloration, or wilting after rain.",
            "priority": "low"
        })

    # --- SOWING SUITABILITY ---
    if 15 <= current_temp <= 30 and current_humidity > 40 and today_rain_prob < 50:
        advice.append({
            "type": "success",
            "icon": "🌱",
            "title": "Good Conditions for Sowing/Transplanting",
            "message": "Temperature and humidity are favorable for planting or transplanting seedlings.",
            "action": "Ideal window for sowing or transplanting. Early morning is best.",
            "priority": "low"
        })

    # --- SPRAY ADVISORY ---
    if today_rain_prob > 50:
        advice.append({
            "type": "info",
            "icon": "🚫",
            "title": "Avoid Spraying Today",
            "message": "Rain expected. Spraying pesticides or fertilizers will be washed away.",
            "action": "Postpone spraying. Wait for a dry window of at least 6 hours.",
            "priority": "medium"
        })

    # --- HARVESTING ADVISORY ---
    if today_rain_prob < 20 and 20 <= today_max_temp <= 35:
        advice.append({
            "type": "success",
            "icon": "🌾",
            "title": "Good Day for Harvesting/Drying",
            "message": "Low rain probability and good temperature. Excellent conditions for harvesting and grain drying.",
            "action": "Schedule harvest activities today for best results.",
            "priority": "low"
        })
    elif today_rain_prob > 60:
        advice.append({
            "type": "warning",
            "icon": "⚠️",
            "title": "Postpone Harvesting",
            "message": "Rain expected today. Wet conditions will make harvesting difficult and may damage grain quality.",
            "action": "Delay harvest by 1-2 days for better conditions.",
            "priority": "medium"
        })

    # Sort by priority
    priority_order = {"urgent": 0, "high": 1, "medium": 2, "low": 3}
    advice.sort(key=lambda x: priority_order.get(x.get("priority", "low"), 3))

    return advice


def _safe_get(data: dict, key: str, default=0):
    """Safely get first element from daily arrays"""
    values = data.get(key, [])
    if isinstance(values, list) and len(values) > 0:
        val = values[0]
        return val if val is not None else default
    return default

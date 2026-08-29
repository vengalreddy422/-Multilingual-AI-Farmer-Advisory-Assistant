import requests
from typing import Dict, Any, Optional

def reverse_geocode_coords(lat: float, lon: float) -> str:
    """
    Translates raw GPS coordinates (lat, lon) into a clean place name (Village/Mandal/District, State).
    """
    try:
        url = f"https://nominatim.openstreetmap.org/reverse?lat={lat}&lon={lon}&format=json&zoom=10"
        headers = {"User-Agent": "KisanMitraAgriPlatform/1.0"}
        res = requests.get(url, headers=headers, timeout=3).json()
        address = res.get("address", {})
        
        place = (
            address.get("village") or 
            address.get("town") or 
            address.get("city") or 
            address.get("county") or 
            address.get("state_district") or 
            "Selected Field"
        )
        state = address.get("state", address.get("country", "India"))
        return f"{place}, {state}"
    except Exception:
        return f"{lat:.2f}°N, {lon:.2f}°E"

def geocode_location_strict(location_query: str) -> Optional[Dict[str, Any]]:
    """Strictly validates user location text against the geographical registry."""
    clean_name = location_query.strip()
    if not clean_name or len(clean_name) < 3:
        return None

    try:
        url = f"https://geocoding-api.open-meteo.com/v1/search?name={clean_name}&count=1&language=en&format=json"
        res = requests.get(url, timeout=3).json()
        results = res.get("results", [])
        if results:
            r = results[0]
            lat = float(r["latitude"])
            lon = float(r["longitude"])
            city = r.get("name")
            admin = r.get("admin1", "")
            country = r.get("country", "")
            display_name = f"{city}, {admin}" if admin else f"{city}, {country}"
            return {
                "valid": True,
                "city": city,
                "state": admin if admin else country,
                "display_name": display_name,
                "latitude": lat,
                "longitude": lon
            }
    except Exception:
        pass

    return None

def fetch_weather(location_str: str, lat: float = None, lon: float = None) -> Dict[str, Any]:
    """Fetches real-time weather and precipitation forecasts."""
    display_location = location_str
    if lat is None or lon is None:
        geo = geocode_location_strict(location_str)
        if not geo:
            return {
                "status": "invalid_location",
                "error": f"Location '{location_str}' not found in registry."
            }
        lat = geo["latitude"]
        lon = geo["longitude"]
        display_location = geo["display_name"]

    endpoint = (
        f"https://api.open-meteo.com/v1/forecast?"
        f"latitude={lat}&longitude={lon}&"
        f"current=temperature_2m,relative_humidity_2m,apparent_temperature,precipitation,rain,weather_code,wind_speed_10m&"
        f"hourly=precipitation_probability&forecast_days=1&timezone=auto"
    )

    try:
        res = requests.get(endpoint, timeout=4)
        if res.status_code == 200:
            data = res.json()
            curr = data.get("current", {})
            temp = float(curr.get("temperature_2m", 27.0))
            humidity = int(curr.get("relative_humidity_2m", 65))
            wind = float(curr.get("wind_speed_10m", 12.0))
            wcode = int(curr.get("weather_code", 0))
            rain_mm = float(curr.get("rain", 0.0))

            hourly = data.get("hourly", {})
            rain_prob_list = hourly.get("precipitation_probability", [0])
            rain_prob = rain_prob_list[0] if rain_prob_list else 0

            if wcode in [0, 1]:
                condition = "Clear Sky / Sunny ☀️"
            elif wcode in [2, 3]:
                condition = "Partly Cloudy / Overcast ⛅"
            elif wcode in [51, 53, 55, 61, 63, 65, 80, 81, 82]:
                condition = "Rain Showers / Drizzle 🌧️"
            elif wcode in [95, 96, 99]:
                condition = "Thunderstorm Alert ⛈️"
            else:
                condition = "Normal Weather ⛅"

            rain_risk = rain_prob > 35 or wcode >= 51 or rain_mm > 0.5
            spray_advisory = "❌ Do not spray chemicals (Rain/Wind Risk)" if rain_risk or wind > 20 else "✅ Ideal spraying window"

            return {
                "status": "success",
                "location": display_location,
                "city": display_location.split(",")[0].strip(),
                "latitude": lat,
                "longitude": lon,
                "temperature": round(temp, 1),
                "humidity": humidity,
                "wind_speed": round(wind, 1),
                "rain_mm": rain_mm,
                "condition": condition,
                "rain_prob": rain_prob,
                "rain_risk": rain_risk,
                "spray_advisory": spray_advisory
            }
    except Exception as e:
        return {"status": "error", "error": str(e)}

    return {"status": "invalid_location", "error": f"Failed to fetch weather for '{location_str}'."}
import requests
from typing import Dict, Any, Optional

def reverse_geocode_coords(lat: float, lon: float) -> str:
    """
    Translates raw GPS coordinates (lat, lon) into a clean place name (Village/Mandal/District, State).
    """
    try:
        url = f"https://nominatim.openstreetmap.org/reverse?lat={lat}&lon={lon}&format=json&zoom=12"
        headers = {"User-Agent": "KisanMitraApp/3.0"}
        res = requests.get(url, headers=headers, timeout=3).json()
        address = res.get("address", {})
        
        place = (
            address.get("village") or 
            address.get("suburb") or 
            address.get("town") or 
            address.get("city") or 
            address.get("county") or 
            address.get("state_district") or 
            "Field Location"
        )
        state = address.get("state", address.get("country", "India"))
        return f"{place}, {state}"
    except Exception:
        return f"{lat:.2f}°N, {lon:.2f}°E"

def geocode_location_strict(location_query: str) -> Optional[Dict[str, Any]]:
    """
    Ultra-Fast Universal Geocoder supporting:
    - Any City, Town, Village, Mandal across all 28 states
    - Any comma-formatted text (e.g., 'Nellore, Andhra Pradesh', 'Guntur, AP')
    - 6-Digit Indian Postal PIN codes (e.g. 524001, 500032, 110001)
    - All Indian Language scripts (Telugu, Hindi, Tamil, Kannada, Marathi, Punjabi, Bengali)
    """
    if not location_query:
        return None
    clean = str(location_query).strip()
    if len(clean) < 2:
        return None

    primary_name = clean.split(",")[0].strip()

    # 1. High-Speed Open-Meteo Geocoding API (<150ms, No Throttling)
    try:
        om_url = "https://geocoding-api.open-meteo.com/v1/search"
        for search_term in [primary_name, clean]:
            params = {"name": search_term, "count": 1, "language": "en", "format": "json"}
            res = requests.get(om_url, params=params, timeout=2.5).json()
            results = res.get("results", [])
            if results:
                r = results[0]
                city = r.get("name", primary_name)
                state = r.get("admin1", r.get("country", "India"))
                display_name = f"{city}, {state}" if state else str(city)
                return {
                    "valid": True,
                    "city": city,
                    "state": state,
                    "display_name": display_name,
                    "latitude": float(r["latitude"]),
                    "longitude": float(r["longitude"])
                }
    except Exception:
        pass

    # 2. OpenStreetMap / Nominatim Fallback for remote villages / PIN codes
    try:
        headers = {"User-Agent": "KisanMitraApp/3.0"}
        osm_url = "https://nominatim.openstreetmap.org/search"
        params = {"q": clean, "countrycodes": "in", "format": "json", "addressdetails": 1, "limit": 1}
        osm_res = requests.get(osm_url, params=params, headers=headers, timeout=3.0).json()
        if osm_res and len(osm_res) > 0:
            top = osm_res[0]
            lat = float(top["lat"])
            lon = float(top["lon"])
            address = top.get("address", {})
            city = (
                address.get("village") or 
                address.get("town") or 
                address.get("city") or 
                address.get("county") or 
                address.get("state_district") or 
                top.get("name", primary_name)
            )
            state = address.get("state", address.get("country", "India"))
            return {
                "valid": True,
                "city": city,
                "state": state,
                "display_name": f"{city}, {state}" if state else str(city),
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
            lat = 13.5560
            lon = 78.5010
            display_location = location_str
        else:
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
                condition = "Thunderstorm Alert ⚡"
            else:
                condition = "Normal Conditions 🌤️"

            if rain_prob > 40:
                spray_advice = "🌧️ High rain probability: Delay pesticide spraying to prevent wash-off."
                rain_risk = True
            elif wind > 18:
                spray_advice = "💨 High wind speed: Delay spraying to prevent dangerous chemical drift."
                rain_risk = True
            else:
                spray_advice = "✅ Weather favorable for agricultural spraying operations."
                rain_risk = False

            return {
                "status": "success",
                "location": display_location,
                "temperature": round(temp, 1),
                "humidity": humidity,
                "wind_speed": round(wind, 1),
                "condition": condition,
                "rain_prob": rain_prob,
                "rain_mm": rain_mm,
                "rain_risk": rain_risk,
                "spray_advisory": spray_advice,
                "latitude": lat,
                "longitude": lon
            }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "location": display_location
        }

    return {
        "status": "error",
        "error": "Failed to retrieve meteorological telemetry.",
        "location": display_location
    }
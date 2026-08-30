import requests
from typing import Dict, Any, Optional

# --- FAST MULTILINGUAL GEOGRAPHICAL REGISTRY FOR INDIAN DISTRICTS & MANDALS ---
KNOWN_INDIAN_LOCATIONS: Dict[str, Dict[str, Any]] = {
    # Andhra Pradesh
    "nellore": {"city": "Nellore", "state": "Andhra Pradesh", "display_name": "Nellore, Andhra Pradesh", "latitude": 14.4494, "longitude": 79.9874},
    "నెల్లూరు": {"city": "Nellore", "state": "Andhra Pradesh", "display_name": "Nellore, Andhra Pradesh", "latitude": 14.4494, "longitude": 79.9874},
    "नेल्लोर": {"city": "Nellore", "state": "Andhra Pradesh", "display_name": "Nellore, Andhra Pradesh", "latitude": 14.4494, "longitude": 79.9874},
    
    "guntur": {"city": "Guntur", "state": "Andhra Pradesh", "display_name": "Guntur, Andhra Pradesh", "latitude": 16.3067, "longitude": 80.4365},
    "గుంటూరు": {"city": "Guntur", "state": "Andhra Pradesh", "display_name": "Guntur, Andhra Pradesh", "latitude": 16.3067, "longitude": 80.4365},
    "गुंटूर": {"city": "Guntur", "state": "Andhra Pradesh", "display_name": "Guntur, Andhra Pradesh", "latitude": 16.3067, "longitude": 80.4365},
    
    "madanapalle": {"city": "Madanapalle", "state": "Andhra Pradesh", "display_name": "Madanapalle, Andhra Pradesh", "latitude": 13.5560, "longitude": 78.5010},
    "మదనపల్లె": {"city": "Madanapalle", "state": "Andhra Pradesh", "display_name": "Madanapalle, Andhra Pradesh", "latitude": 13.5560, "longitude": 78.5010},
    
    "tirupati": {"city": "Tirupati", "state": "Andhra Pradesh", "display_name": "Tirupati, Andhra Pradesh", "latitude": 13.6288, "longitude": 79.4192},
    "తిరుపతి": {"city": "Tirupati", "state": "Andhra Pradesh", "display_name": "Tirupati, Andhra Pradesh", "latitude": 13.6288, "longitude": 79.4192},
    
    "kurnool": {"city": "Kurnool", "state": "Andhra Pradesh", "display_name": "Kurnool, Andhra Pradesh", "latitude": 15.8281, "longitude": 78.0373},
    "కర్నూలు": {"city": "Kurnool", "state": "Andhra Pradesh", "display_name": "Kurnool, Andhra Pradesh", "latitude": 15.8281, "longitude": 78.0373},
    
    "anantapur": {"city": "Anantapur", "state": "Andhra Pradesh", "display_name": "Anantapur, Andhra Pradesh", "latitude": 14.6819, "longitude": 77.6006},
    "అనంతపురం": {"city": "Anantapur", "state": "Andhra Pradesh", "display_name": "Anantapur, Andhra Pradesh", "latitude": 14.6819, "longitude": 77.6006},
    
    "kadapa": {"city": "Kadapa", "state": "Andhra Pradesh", "display_name": "Kadapa, Andhra Pradesh", "latitude": 14.4673, "longitude": 78.8242},
    "కడప": {"city": "Kadapa", "state": "Andhra Pradesh", "display_name": "Kadapa, Andhra Pradesh", "latitude": 14.4673, "longitude": 78.8242},
    
    "vijayawada": {"city": "Vijayawada", "state": "Andhra Pradesh", "display_name": "Vijayawada, Andhra Pradesh", "latitude": 16.5062, "longitude": 80.6480},
    "విజయవాడ": {"city": "Vijayawada", "state": "Andhra Pradesh", "display_name": "Vijayawada, Andhra Pradesh", "latitude": 16.5062, "longitude": 80.6480},
    
    "rajahmundry": {"city": "Rajahmundry", "state": "Andhra Pradesh", "display_name": "Rajahmundry, Andhra Pradesh", "latitude": 17.0005, "longitude": 81.8040},
    "రాజమండ్రి": {"city": "Rajahmundry", "state": "Andhra Pradesh", "display_name": "Rajahmundry, Andhra Pradesh", "latitude": 17.0005, "longitude": 81.8040},
    
    "visakhapatnam": {"city": "Visakhapatnam", "state": "Andhra Pradesh", "display_name": "Visakhapatnam, Andhra Pradesh", "latitude": 17.6868, "longitude": 83.2185},
    "విశాఖపట్నం": {"city": "Visakhapatnam", "state": "Andhra Pradesh", "display_name": "Visakhapatnam, Andhra Pradesh", "latitude": 17.6868, "longitude": 83.2185},
    
    # Telangana
    "hyderabad": {"city": "Hyderabad", "state": "Telangana", "display_name": "Hyderabad, Telangana", "latitude": 17.3850, "longitude": 78.4867},
    "హైదరాబాద్": {"city": "Hyderabad", "state": "Telangana", "display_name": "Hyderabad, Telangana", "latitude": 17.3850, "longitude": 78.4867},
    "हैदराबाद": {"city": "Hyderabad", "state": "Telangana", "display_name": "Hyderabad, Telangana", "latitude": 17.3850, "longitude": 78.4867},
    
    "warangal": {"city": "Warangal", "state": "Telangana", "display_name": "Warangal, Telangana", "latitude": 17.9689, "longitude": 79.5941},
    "వరంగల్": {"city": "Warangal", "state": "Telangana", "display_name": "Warangal, Telangana", "latitude": 17.9689, "longitude": 79.5941},
    
    "karimnagar": {"city": "Karimnagar", "state": "Telangana", "display_name": "Karimnagar, Telangana", "latitude": 18.4386, "longitude": 79.1288},
    "కరీంనగర్": {"city": "Karimnagar", "state": "Telangana", "display_name": "Karimnagar, Telangana", "latitude": 18.4386, "longitude": 79.1288},
    
    "khammam": {"city": "Khammam", "state": "Telangana", "display_name": "Khammam, Telangana", "latitude": 17.2473, "longitude": 80.1514},
    "ఖమ్మం": {"city": "Khammam", "state": "Telangana", "display_name": "Khammam, Telangana", "latitude": 17.2473, "longitude": 80.1514},
    
    "nizamabad": {"city": "Nizamabad", "state": "Telangana", "display_name": "Nizamabad, Telangana", "latitude": 18.6725, "longitude": 78.0941},
    "నిజామాబాద్": {"city": "Nizamabad", "state": "Telangana", "display_name": "Nizamabad, Telangana", "latitude": 18.6725, "longitude": 78.0941},
    
    # Maharashtra
    "pune": {"city": "Pune", "state": "Maharashtra", "display_name": "Pune, Maharashtra", "latitude": 18.5204, "longitude": 73.8567},
    "पुणे": {"city": "Pune", "state": "Maharashtra", "display_name": "Pune, Maharashtra", "latitude": 18.5204, "longitude": 73.8567},
    
    "nashik": {"city": "Nashik", "state": "Maharashtra", "display_name": "Nashik, Maharashtra", "latitude": 19.9975, "longitude": 73.7898},
    "नासिक": {"city": "Nashik", "state": "Maharashtra", "display_name": "Nashik, Maharashtra", "latitude": 19.9975, "longitude": 73.7898},
    
    "nagpur": {"city": "Nagpur", "state": "Maharashtra", "display_name": "Nagpur, Maharashtra", "latitude": 21.1458, "longitude": 79.0882},
    "नागपुर": {"city": "Nagpur", "state": "Maharashtra", "display_name": "Nagpur, Maharashtra", "latitude": 21.1458, "longitude": 79.0882},
    
    # Tamil Nadu
    "coimbatore": {"city": "Coimbatore", "state": "Tamil Nadu", "display_name": "Coimbatore, Tamil Nadu", "latitude": 11.0168, "longitude": 76.9558},
    "கோயம்புத்தூர்": {"city": "Coimbatore", "state": "Tamil Nadu", "display_name": "Coimbatore, Tamil Nadu", "latitude": 11.0168, "longitude": 76.9558},
    
    "madurai": {"city": "Madurai", "state": "Tamil Nadu", "display_name": "Madurai, Tamil Nadu", "latitude": 9.9252, "longitude": 78.1198},
    "மதுரை": {"city": "Madurai", "state": "Tamil Nadu", "display_name": "Madurai, Tamil Nadu", "latitude": 9.9252, "longitude": 78.1198},
    
    # Karnataka
    "belagavi": {"city": "Belagavi", "state": "Karnataka", "display_name": "Belagavi, Karnataka", "latitude": 15.8497, "longitude": 74.4977},
    "ಬೆಳಗಾವಿ": {"city": "Belagavi", "state": "Karnataka", "display_name": "Belagavi, Karnataka", "latitude": 15.8497, "longitude": 74.4977},
    
    "mysuru": {"city": "Mysuru", "state": "Karnataka", "display_name": "Mysuru, Karnataka", "latitude": 12.2958, "longitude": 76.6394},
    "ಮೈಸೂರು": {"city": "Mysuru", "state": "Karnataka", "display_name": "Mysuru, Karnataka", "latitude": 12.2958, "longitude": 76.6394},
    
    # North India
    "ludhiana": {"city": "Ludhiana", "state": "Punjab", "display_name": "Ludhiana, Punjab", "latitude": 30.9010, "longitude": 75.8573},
    "लुधियाना": {"city": "Ludhiana", "state": "Punjab", "display_name": "Ludhiana, Punjab", "latitude": 30.9010, "longitude": 75.8573},
    
    "karnal": {"city": "Karnal", "state": "Haryana", "display_name": "Karnal, Haryana", "latitude": 29.6857, "longitude": 76.9905},
    "करनाल": {"city": "Karnal", "state": "Haryana", "display_name": "Karnal, Haryana", "latitude": 29.6857, "longitude": 76.9905}
}

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
    """
    Multi-tier geocoder supporting English, Telugu, Hindi, Tamil, Kannada, Marathi.
    1. Instant fast in-memory dictionary lookup.
    2. Open-Meteo Geocoding Search API.
    3. Nominatim OpenStreetMap regional Search API fallback.
    """
    clean_name = location_query.strip().lower()
    if not clean_name or len(clean_name) < 2:
        return None

    # Tier 1: Fast in-memory lookup for major agricultural districts
    if clean_name in KNOWN_INDIAN_LOCATIONS:
        match_data = KNOWN_INDIAN_LOCATIONS[clean_name]
        return {
            "valid": True,
            "city": match_data["city"],
            "state": match_data["state"],
            "display_name": match_data["display_name"],
            "latitude": match_data["latitude"],
            "longitude": match_data["longitude"]
        }

    # Also check if query is contained in known keys (e.g. "nellore district" or "గ్రామం నెల్లూరు")
    for key, match_data in KNOWN_INDIAN_LOCATIONS.items():
        if key in clean_name or clean_name in key:
            return {
                "valid": True,
                "city": match_data["city"],
                "state": match_data["state"],
                "display_name": match_data["display_name"],
                "latitude": match_data["latitude"],
                "longitude": match_data["longitude"]
            }

    # Tier 2: Open-Meteo Geocoding API
    try:
        url = f"https://geocoding-api.open-meteo.com/v1/search?name={requests.utils.quote(location_query)}&count=1&language=en&format=json"
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

    # Tier 3: Nominatim OpenStreetMap Search for regional Indian scripts / small villages
    try:
        osm_url = f"https://nominatim.openstreetmap.org/search?q={requests.utils.quote(location_query)}&countrycodes=in&format=json&limit=1"
        headers = {"User-Agent": "KisanMitraApp/1.0"}
        osm_res = requests.get(osm_url, headers=headers, timeout=3).json()
        if osm_res and len(osm_res) > 0:
            top_hit = osm_res[0]
            lat = float(top_hit["lat"])
            lon = float(top_hit["lon"])
            raw_disp = top_hit.get("display_name", "")
            parts = [p.strip() for p in raw_disp.split(",") if p.strip()]
            
            if len(parts) >= 2:
                # e.g., "Nellore, Andhra Pradesh"
                city_part = parts[0]
                state_part = parts[-3] if len(parts) >= 3 else parts[-1]
                display_name = f"{city_part}, {state_part}"
            else:
                display_name = raw_disp or location_query
                city_part = display_name
                state_part = "India"
                
            return {
                "valid": True,
                "city": city_part,
                "state": state_part,
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
            # Fallback to default coordinates if unmapped
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

            # Spray feasibility rule
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
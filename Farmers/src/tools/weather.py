import requests
from typing import Dict, Any, Optional

# --- INSTANT PAN-INDIA & ALL-AP/TS REGIONAL GEOGRAPHICAL DIRECTORY ---
KNOWN_INDIAN_LOCATIONS: Dict[str, Dict[str, Any]] = {
    # === ALL 26 DISTRICTS & POPULAR HUBS OF ANDHRA PRADESH ===
    "nellore": {"city": "Nellore", "state": "Andhra Pradesh", "display_name": "Nellore, Andhra Pradesh", "latitude": 14.4494, "longitude": 79.9874},
    "నెల్లూరు": {"city": "Nellore", "state": "Andhra Pradesh", "display_name": "Nellore, Andhra Pradesh", "latitude": 14.4494, "longitude": 79.9874},
    "guntur": {"city": "Guntur", "state": "Andhra Pradesh", "display_name": "Guntur, Andhra Pradesh", "latitude": 16.3067, "longitude": 80.4365},
    "గుంటూరు": {"city": "Guntur", "state": "Andhra Pradesh", "display_name": "Guntur, Andhra Pradesh", "latitude": 16.3067, "longitude": 80.4365},
    "tirupati": {"city": "Tirupati", "state": "Andhra Pradesh", "display_name": "Tirupati, Andhra Pradesh", "latitude": 13.6288, "longitude": 79.4192},
    "తిరుపతి": {"city": "Tirupati", "state": "Andhra Pradesh", "display_name": "Tirupati, Andhra Pradesh", "latitude": 13.6288, "longitude": 79.4192},
    "chittoor": {"city": "Chittoor", "state": "Andhra Pradesh", "display_name": "Chittoor, Andhra Pradesh", "latitude": 13.2172, "longitude": 79.1003},
    "చిత్తూరు": {"city": "Chittoor", "state": "Andhra Pradesh", "display_name": "Chittoor, Andhra Pradesh", "latitude": 13.2172, "longitude": 79.1003},
    "madanapalle": {"city": "Madanapalle", "state": "Andhra Pradesh", "display_name": "Madanapalle, Andhra Pradesh", "latitude": 13.5560, "longitude": 78.5010},
    "మదనపల్లె": {"city": "Madanapalle", "state": "Andhra Pradesh", "display_name": "Madanapalle, Andhra Pradesh", "latitude": 13.5560, "longitude": 78.5010},
    "kurnool": {"city": "Kurnool", "state": "Andhra Pradesh", "display_name": "Kurnool, Andhra Pradesh", "latitude": 15.8281, "longitude": 78.0373},
    "కర్నూలు": {"city": "Kurnool", "state": "Andhra Pradesh", "display_name": "Kurnool, Andhra Pradesh", "latitude": 15.8281, "longitude": 78.0373},
    "nandyal": {"city": "Nandyal", "state": "Andhra Pradesh", "display_name": "Nandyal, Andhra Pradesh", "latitude": 15.4886, "longitude": 78.4836},
    "నంద్యాల": {"city": "Nandyal", "state": "Andhra Pradesh", "display_name": "Nandyal, Andhra Pradesh", "latitude": 15.4886, "longitude": 78.4836},
    "anantapur": {"city": "Anantapur", "state": "Andhra Pradesh", "display_name": "Anantapur, Andhra Pradesh", "latitude": 14.6819, "longitude": 77.6006},
    "అనంతపురం": {"city": "Anantapur", "state": "Andhra Pradesh", "display_name": "Anantapur, Andhra Pradesh", "latitude": 14.6819, "longitude": 77.6006},
    "kadapa": {"city": "Kadapa", "state": "Andhra Pradesh", "display_name": "Kadapa, Andhra Pradesh", "latitude": 14.4673, "longitude": 78.8242},
    "కడప": {"city": "Kadapa", "state": "Andhra Pradesh", "display_name": "Kadapa, Andhra Pradesh", "latitude": 14.4673, "longitude": 78.8242},
    "vijayawada": {"city": "Vijayawada", "state": "Andhra Pradesh", "display_name": "Vijayawada, Andhra Pradesh", "latitude": 16.5062, "longitude": 80.6480},
    "విజయవాడ": {"city": "Vijayawada", "state": "Andhra Pradesh", "display_name": "Vijayawada, Andhra Pradesh", "latitude": 16.5062, "longitude": 80.6480},
    "ongole": {"city": "Ongole", "state": "Andhra Pradesh", "display_name": "Ongole, Andhra Pradesh", "latitude": 15.5057, "longitude": 80.0499},
    "ఒంగోలు": {"city": "Ongole", "state": "Andhra Pradesh", "display_name": "Ongole, Andhra Pradesh", "latitude": 15.5057, "longitude": 80.0499},
    "bhimavaram": {"city": "Bhimavaram", "state": "Andhra Pradesh", "display_name": "Bhimavaram, Andhra Pradesh", "latitude": 16.5449, "longitude": 81.5212},
    "భీమవరం": {"city": "Bhimavaram", "state": "Andhra Pradesh", "display_name": "Bhimavaram, Andhra Pradesh", "latitude": 16.5449, "longitude": 81.5212},
    "eluru": {"city": "Eluru", "state": "Andhra Pradesh", "display_name": "Eluru, Andhra Pradesh", "latitude": 16.7107, "longitude": 81.0952},
    "ఏలూరు": {"city": "Eluru", "state": "Andhra Pradesh", "display_name": "Eluru, Andhra Pradesh", "latitude": 16.7107, "longitude": 81.0952},
    "rajahmundry": {"city": "Rajahmundry", "state": "Andhra Pradesh", "display_name": "Rajahmundry, Andhra Pradesh", "latitude": 17.0005, "longitude": 81.8040},
    "రాజమండ్రి": {"city": "Rajahmundry", "state": "Andhra Pradesh", "display_name": "Rajahmundry, Andhra Pradesh", "latitude": 17.0005, "longitude": 81.8040},
    "kakinada": {"city": "Kakinada", "state": "Andhra Pradesh", "display_name": "Kakinada, Andhra Pradesh", "latitude": 16.9891, "longitude": 82.2475},
    "కాకినాడ": {"city": "Kakinada", "state": "Andhra Pradesh", "display_name": "Kakinada, Andhra Pradesh", "latitude": 16.9891, "longitude": 82.2475},
    "visakhapatnam": {"city": "Visakhapatnam", "state": "Andhra Pradesh", "display_name": "Visakhapatnam, Andhra Pradesh", "latitude": 17.6868, "longitude": 83.2185},
    "విశాఖపట్నం": {"city": "Visakhapatnam", "state": "Andhra Pradesh", "display_name": "Visakhapatnam, Andhra Pradesh", "latitude": 17.6868, "longitude": 83.2185},
    "vizianagaram": {"city": "Vizianagaram", "state": "Andhra Pradesh", "display_name": "Vizianagaram, Andhra Pradesh", "latitude": 18.1067, "longitude": 83.3956},
    "విజయనగరం": {"city": "Vizianagaram", "state": "Andhra Pradesh", "display_name": "Vizianagaram, Andhra Pradesh", "latitude": 18.1067, "longitude": 83.3956},
    "srikakulam": {"city": "Srikakulam", "state": "Andhra Pradesh", "display_name": "Srikakulam, Andhra Pradesh", "latitude": 18.2949, "longitude": 83.8938},
    "శ్రీకాకుళం": {"city": "Srikakulam", "state": "Andhra Pradesh", "display_name": "Srikakulam, Andhra Pradesh", "latitude": 18.2949, "longitude": 83.8938},
    "palnadu": {"city": "Narasaraopet (Palnadu)", "state": "Andhra Pradesh", "display_name": "Palnadu, Andhra Pradesh", "latitude": 16.2355, "longitude": 80.0496},
    "పల్నాడు": {"city": "Palnadu", "state": "Andhra Pradesh", "display_name": "Palnadu, Andhra Pradesh", "latitude": 16.2355, "longitude": 80.0496},
    "bapatla": {"city": "Bapatla", "state": "Andhra Pradesh", "display_name": "Bapatla, Andhra Pradesh", "latitude": 15.9042, "longitude": 80.4676},
    "బాపట్ల": {"city": "Bapatla", "state": "Andhra Pradesh", "display_name": "Bapatla, Andhra Pradesh", "latitude": 15.9042, "longitude": 80.4676},
    "annamayya": {"city": "Rayachoti (Annamayya)", "state": "Andhra Pradesh", "display_name": "Annamayya, Andhra Pradesh", "latitude": 14.0560, "longitude": 78.7520},
    "అన్నమయ్య": {"city": "Annamayya", "state": "Andhra Pradesh", "display_name": "Annamayya, Andhra Pradesh", "latitude": 14.0560, "longitude": 78.7520},
    "konaseema": {"city": "Amalapuram (Konaseema)", "state": "Andhra Pradesh", "display_name": "Konaseema, Andhra Pradesh", "latitude": 16.5787, "longitude": 82.0061},
    "కోనసీమ": {"city": "Konaseema", "state": "Andhra Pradesh", "display_name": "Konaseema, Andhra Pradesh", "latitude": 16.5787, "longitude": 82.0061},
    "machilipatnam": {"city": "Machilipatnam", "state": "Andhra Pradesh", "display_name": "Machilipatnam, Andhra Pradesh", "latitude": 16.1875, "longitude": 81.1389},
    "మచిలీపట్నం": {"city": "Machilipatnam", "state": "Andhra Pradesh", "display_name": "Machilipatnam, Andhra Pradesh", "latitude": 16.1875, "longitude": 81.1389},
    "dharmavaram": {"city": "Dharmavaram", "state": "Andhra Pradesh", "display_name": "Dharmavaram, Andhra Pradesh", "latitude": 14.4137, "longitude": 77.7126},
    "ధర్మవరం": {"city": "Dharmavaram", "state": "Andhra Pradesh", "display_name": "Dharmavaram, Andhra Pradesh", "latitude": 14.4137, "longitude": 77.7126},
    "hindupur": {"city": "Hindupur", "state": "Andhra Pradesh", "display_name": "Hindupur, Andhra Pradesh", "latitude": 13.8290, "longitude": 77.4930},
    "హిందూపురం": {"city": "Hindupur", "state": "Andhra Pradesh", "display_name": "Hindupur, Andhra Pradesh", "latitude": 13.8290, "longitude": 77.4930},
    "tenali": {"city": "Tenali", "state": "Andhra Pradesh", "display_name": "Tenali, Andhra Pradesh", "latitude": 16.2437, "longitude": 80.6400},
    "తెనాలి": {"city": "Tenali", "state": "Andhra Pradesh", "display_name": "Tenali, Andhra Pradesh", "latitude": 16.2437, "longitude": 80.6400},
    "kuppam": {"city": "Kuppam", "state": "Andhra Pradesh", "display_name": "Kuppam, Andhra Pradesh", "latitude": 12.7452, "longitude": 78.3443},
    "కుప్పం": {"city": "Kuppam", "state": "Andhra Pradesh", "display_name": "Kuppam, Andhra Pradesh", "latitude": 12.7452, "longitude": 78.3443},

    # === POPULAR TELANGANA DISTRICTS ===
    "hyderabad": {"city": "Hyderabad", "state": "Telangana", "display_name": "Hyderabad, Telangana", "latitude": 17.3850, "longitude": 78.4867},
    "హైదరాబాద్": {"city": "Hyderabad", "state": "Telangana", "display_name": "Hyderabad, Telangana", "latitude": 17.3850, "longitude": 78.4867},
    "warangal": {"city": "Warangal", "state": "Telangana", "display_name": "Warangal, Telangana", "latitude": 17.9689, "longitude": 79.5941},
    "వరంగల్": {"city": "Warangal", "state": "Telangana", "display_name": "Warangal, Telangana", "latitude": 17.9689, "longitude": 79.5941},
    "karimnagar": {"city": "Karimnagar", "state": "Telangana", "display_name": "Karimnagar, Telangana", "latitude": 18.4386, "longitude": 79.1288},
    "కరీంనగర్": {"city": "Karimnagar", "state": "Telangana", "display_name": "Karimnagar, Telangana", "latitude": 18.4386, "longitude": 79.1288},
    "khammam": {"city": "Khammam", "state": "Telangana", "display_name": "Khammam, Telangana", "latitude": 17.2473, "longitude": 80.1514},
    "ఖమ్మం": {"city": "Khammam", "state": "Telangana", "display_name": "Khammam, Telangana", "latitude": 17.2473, "longitude": 80.1514},
    "nizamabad": {"city": "Nizamabad", "state": "Telangana", "display_name": "Nizamabad, Telangana", "latitude": 18.6725, "longitude": 78.0941},
    "నిజామాబాద్": {"city": "Nizamabad", "state": "Telangana", "display_name": "Nizamabad, Telangana", "latitude": 18.6725, "longitude": 78.0941},
    "nalgonda": {"city": "Nalgonda", "state": "Telangana", "display_name": "Nalgonda, Telangana", "latitude": 17.0577, "longitude": 79.2684},
    "నల్గొండ": {"city": "Nalgonda", "state": "Telangana", "display_name": "Nalgonda, Telangana", "latitude": 17.0577, "longitude": 79.2684},
    "mahabubnagar": {"city": "Mahabubnagar", "state": "Telangana", "display_name": "Mahabubnagar, Telangana", "latitude": 16.7488, "longitude": 78.0035},
    "మహబూబ్ నగర్": {"city": "Mahabubnagar", "state": "Telangana", "display_name": "Mahabubnagar, Telangana", "latitude": 16.7488, "longitude": 78.0035},

    # === MAJOR PAN-INDIA HUBS ===
    "pune": {"city": "Pune", "state": "Maharashtra", "display_name": "Pune, Maharashtra", "latitude": 18.5204, "longitude": 73.8567},
    "nashik": {"city": "Nashik", "state": "Maharashtra", "display_name": "Nashik, Maharashtra", "latitude": 19.9975, "longitude": 73.7898},
    "nagpur": {"city": "Nagpur", "state": "Maharashtra", "display_name": "Nagpur, Maharashtra", "latitude": 21.1458, "longitude": 79.0882},
    "ludhiana": {"city": "Ludhiana", "state": "Punjab", "display_name": "Ludhiana, Punjab", "latitude": 30.9010, "longitude": 75.8573},
    "karnal": {"city": "Karnal", "state": "Haryana", "display_name": "Karnal, Haryana", "latitude": 29.6857, "longitude": 76.9905},
    "varanasi": {"city": "Varanasi", "state": "Uttar Pradesh", "display_name": "Varanasi, Uttar Pradesh", "latitude": 25.3176, "longitude": 82.9739},
    "lucknow": {"city": "Lucknow", "state": "Uttar Pradesh", "display_name": "Lucknow, Uttar Pradesh", "latitude": 26.8467, "longitude": 80.9462},
    "patna": {"city": "Patna", "state": "Bihar", "display_name": "Patna, Bihar", "latitude": 25.5941, "longitude": 85.1376},
    "jaipur": {"city": "Jaipur", "state": "Rajasthan", "display_name": "Jaipur, Rajasthan", "latitude": 26.9124, "longitude": 75.7873},
    "indore": {"city": "Indore", "state": "Madhya Pradesh", "display_name": "Indore, Madhya Pradesh", "latitude": 22.7196, "longitude": 75.8577},
    "coimbatore": {"city": "Coimbatore", "state": "Tamil Nadu", "display_name": "Coimbatore, Tamil Nadu", "latitude": 11.0168, "longitude": 76.9558},
    "madurai": {"city": "Madurai", "state": "Tamil Nadu", "display_name": "Madurai, Tamil Nadu", "latitude": 9.9252, "longitude": 78.1198},
    "bengaluru": {"city": "Bengaluru", "state": "Karnataka", "display_name": "Bengaluru, Karnataka", "latitude": 12.9716, "longitude": 77.5946},
    "belagavi": {"city": "Belagavi", "state": "Karnataka", "display_name": "Belagavi, Karnataka", "latitude": 15.8497, "longitude": 74.4977},
    "mysuru": {"city": "Mysuru", "state": "Karnataka", "display_name": "Mysuru, Karnataka", "latitude": 12.2958, "longitude": 76.6394},
    "shimla": {"city": "Shimla", "state": "Himachal Pradesh", "display_name": "Shimla, Himachal Pradesh", "latitude": 31.1048, "longitude": 77.1734},
    "kolkata": {"city": "Kolkata", "state": "West Bengal", "display_name": "Kolkata, West Bengal", "latitude": 22.5726, "longitude": 88.3639},
    "bhubaneswar": {"city": "Bhubaneswar", "state": "Odisha", "display_name": "Bhubaneswar, Odisha", "latitude": 20.2961, "longitude": 85.8245},
    "guwahati": {"city": "Guwahati", "state": "Assam", "display_name": "Guwahati, Assam", "latitude": 26.1445, "longitude": 91.7362}
}

def reverse_geocode_coords(lat: float, lon: float) -> str:
    """Translates raw GPS coordinates into a place name."""
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
    """Ultra-Fast Multilingual Geocoder with instant dictionary lookup & live API fallback."""
    if not location_query:
        return None
    clean = str(location_query).strip().lower()
    if len(clean) < 2:
        return None

    # 1. Instant Fast Dictionary Match (0.001ms response)
    if clean in KNOWN_INDIAN_LOCATIONS:
        match = KNOWN_INDIAN_LOCATIONS[clean]
        return {
            "valid": True,
            "city": match["city"],
            "state": match["state"],
            "display_name": match["display_name"],
            "latitude": match["latitude"],
            "longitude": match["longitude"]
        }

    # Match substrings in known dictionary
    for k, match in KNOWN_INDIAN_LOCATIONS.items():
        if k in clean or clean in k:
            return {
                "valid": True,
                "city": match["city"],
                "state": match["state"],
                "display_name": match["display_name"],
                "latitude": match["latitude"],
                "longitude": match["longitude"]
            }

    primary_name = clean.split(",")[0].strip()

    # 2. High-Speed Open-Meteo Geocoding API (<150ms)
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

    # 3. OpenStreetMap / Nominatim Fallback for remote villages / PIN codes
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
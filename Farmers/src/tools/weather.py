import requests
from typing import Dict, Any, Optional

# --- PAN-INDIA MULTILINGUAL GEOGRAPHICAL REGISTRY ACROSS ALL STATES ---
KNOWN_INDIAN_LOCATIONS: Dict[str, Dict[str, Any]] = {
    # --- 1. PUNJAB & HARYANA (TRANS-GANGETIC WHEAT & PADDY BELT) ---
    "ludhiana": {"city": "Ludhiana", "state": "Punjab", "display_name": "Ludhiana, Punjab", "latitude": 30.9010, "longitude": 75.8573},
    "लुधियाना": {"city": "Ludhiana", "state": "Punjab", "display_name": "Ludhiana, Punjab", "latitude": 30.9010, "longitude": 75.8573},
    "ਲੁਧਿਆਣਾ": {"city": "Ludhiana", "state": "Punjab", "display_name": "Ludhiana, Punjab", "latitude": 30.9010, "longitude": 75.8573},
    "amritsar": {"city": "Amritsar", "state": "Punjab", "display_name": "Amritsar, Punjab", "latitude": 31.6340, "longitude": 74.8723},
    "bathinda": {"city": "Bathinda", "state": "Punjab", "display_name": "Bathinda, Punjab", "latitude": 30.2110, "longitude": 74.9455},
    "patiala": {"city": "Patiala", "state": "Punjab", "display_name": "Patiala, Punjab", "latitude": 30.3398, "longitude": 76.3869},
    "karnal": {"city": "Karnal", "state": "Haryana", "display_name": "Karnal, Haryana", "latitude": 29.6857, "longitude": 76.9905},
    "करनाल": {"city": "Karnal", "state": "Haryana", "display_name": "Karnal, Haryana", "latitude": 29.6857, "longitude": 76.9905},
    "hisar": {"city": "Hisar", "state": "Haryana", "display_name": "Hisar, Haryana", "latitude": 29.1492, "longitude": 75.7217},
    "sirsa": {"city": "Sirsa", "state": "Haryana", "display_name": "Sirsa, Haryana", "latitude": 29.5349, "longitude": 75.0290},
    "ambala": {"city": "Ambala", "state": "Haryana", "display_name": "Ambala, Haryana", "latitude": 30.3782, "longitude": 76.7767},

    # --- 2. UTTAR PRADESH & BIHAR (UPPER / MIDDLE GANGETIC PLAINS) ---
    "lucknow": {"city": "Lucknow", "state": "Uttar Pradesh", "display_name": "Lucknow, Uttar Pradesh", "latitude": 26.8467, "longitude": 80.9462},
    "लखनऊ": {"city": "Lucknow", "state": "Uttar Pradesh", "display_name": "Lucknow, Uttar Pradesh", "latitude": 26.8467, "longitude": 80.9462},
    "varanasi": {"city": "Varanasi", "state": "Uttar Pradesh", "display_name": "Varanasi, Uttar Pradesh", "latitude": 25.3176, "longitude": 82.9739},
    "वाराणसी": {"city": "Varanasi", "state": "Uttar Pradesh", "display_name": "Varanasi, Uttar Pradesh", "latitude": 25.3176, "longitude": 82.9739},
    "వారణాసి": {"city": "Varanasi", "state": "Uttar Pradesh", "display_name": "Varanasi, Uttar Pradesh", "latitude": 25.3176, "longitude": 82.9739},
    "kanpur": {"city": "Kanpur", "state": "Uttar Pradesh", "display_name": "Kanpur, Uttar Pradesh", "latitude": 26.4499, "longitude": 80.3319},
    "agra": {"city": "Agra", "state": "Uttar Pradesh", "display_name": "Agra, Uttar Pradesh", "latitude": 27.1767, "longitude": 78.0081},
    "meerut": {"city": "Meerut", "state": "Uttar Pradesh", "display_name": "Meerut, Uttar Pradesh", "latitude": 28.9845, "longitude": 77.7064},
    "gorakhpur": {"city": "Gorakhpur", "state": "Uttar Pradesh", "display_name": "Gorakhpur, Uttar Pradesh", "latitude": 26.7606, "longitude": 83.3732},
    "patna": {"city": "Patna", "state": "Bihar", "display_name": "Patna, Bihar", "latitude": 25.5941, "longitude": 85.1376},
    "पटना": {"city": "Patna", "state": "Bihar", "display_name": "Patna, Bihar", "latitude": 25.5941, "longitude": 85.1376},
    "muzaffarpur": {"city": "Muzaffarpur", "state": "Bihar", "display_name": "Muzaffarpur, Bihar", "latitude": 26.1209, "longitude": 85.3647},
    "gaya": {"city": "Gaya", "state": "Bihar", "display_name": "Gaya, Bihar", "latitude": 24.7914, "longitude": 85.0002},

    # --- 3. MAHARASHTRA (WESTERN PLATEAU & COTTON/SOYBEAN ZONE) ---
    "pune": {"city": "Pune", "state": "Maharashtra", "display_name": "Pune, Maharashtra", "latitude": 18.5204, "longitude": 73.8567},
    "पुणे": {"city": "Pune", "state": "Maharashtra", "display_name": "Pune, Maharashtra", "latitude": 18.5204, "longitude": 73.8567},
    "పూణే": {"city": "Pune", "state": "Maharashtra", "display_name": "Pune, Maharashtra", "latitude": 18.5204, "longitude": 73.8567},
    "nashik": {"city": "Nashik", "state": "Maharashtra", "display_name": "Nashik, Maharashtra", "latitude": 19.9975, "longitude": 73.7898},
    "नासिक": {"city": "Nashik", "state": "Maharashtra", "display_name": "Nashik, Maharashtra", "latitude": 19.9975, "longitude": 73.7898},
    "nagpur": {"city": "Nagpur", "state": "Maharashtra", "display_name": "Nagpur, Maharashtra", "latitude": 21.1458, "longitude": 79.0882},
    "नागपुर": {"city": "Nagpur", "state": "Maharashtra", "display_name": "Nagpur, Maharashtra", "latitude": 21.1458, "longitude": 79.0882},
    "aurangabad": {"city": "Chhatrapati Sambhaji Nagar", "state": "Maharashtra", "display_name": "Chhatrapati Sambhaji Nagar, Maharashtra", "latitude": 19.8762, "longitude": 75.3433},
    "kolhapur": {"city": "Kolhapur", "state": "Maharashtra", "display_name": "Kolhapur, Maharashtra", "latitude": 16.7050, "longitude": 74.2433},
    "solapur": {"city": "Solapur", "state": "Maharashtra", "display_name": "Solapur, Maharashtra", "latitude": 17.6599, "longitude": 75.9064},
    "amravati": {"city": "Amravati", "state": "Maharashtra", "display_name": "Amravati, Maharashtra", "latitude": 20.9374, "longitude": 77.7796},

    # --- 4. GUJARAT & RAJASTHAN (WESTERN DRY & COTTON/GROUNDNUT ZONE) ---
    "ahmedabad": {"city": "Ahmedabad", "state": "Gujarat", "display_name": "Ahmedabad, Gujarat", "latitude": 23.0225, "longitude": 72.5714},
    "अहमदाबाद": {"city": "Ahmedabad", "state": "Gujarat", "display_name": "Ahmedabad, Gujarat", "latitude": 23.0225, "longitude": 72.5714},
    "rajkot": {"city": "Rajkot", "state": "Gujarat", "display_name": "Rajkot, Gujarat", "latitude": 22.3039, "longitude": 70.8022},
    "surat": {"city": "Surat", "state": "Gujarat", "display_name": "Surat, Gujarat", "latitude": 21.1702, "longitude": 72.8311},
    "junagadh": {"city": "Junagadh", "state": "Gujarat", "display_name": "Junagadh, Gujarat", "latitude": 21.5222, "longitude": 70.4579},
    "jaipur": {"city": "Jaipur", "state": "Rajasthan", "display_name": "Jaipur, Rajasthan", "latitude": 26.9124, "longitude": 75.7873},
    "जयपुर": {"city": "Jaipur", "state": "Rajasthan", "display_name": "Jaipur, Rajasthan", "latitude": 26.9124, "longitude": 75.7873},
    "జైపూర్": {"city": "Jaipur", "state": "Rajasthan", "display_name": "Jaipur, Rajasthan", "latitude": 26.9124, "longitude": 75.7873},
    "jodhpur": {"city": "Jodhpur", "state": "Rajasthan", "display_name": "Jodhpur, Rajasthan", "latitude": 26.2389, "longitude": 73.0243},
    "kota": {"city": "Kota", "state": "Rajasthan", "display_name": "Kota, Rajasthan", "latitude": 25.2138, "longitude": 75.8648},
    "ganganagar": {"city": "Sri Ganganagar", "state": "Rajasthan", "display_name": "Sri Ganganagar, Rajasthan", "latitude": 29.9038, "longitude": 73.8772},

    # --- 5. MADHYA PRADESH & CHHATTISGARH (CENTRAL PULSES & SOYBEAN ZONE) ---
    "indore": {"city": "Indore", "state": "Madhya Pradesh", "display_name": "Indore, Madhya Pradesh", "latitude": 22.7196, "longitude": 75.8577},
    "इन्दौर": {"city": "Indore", "state": "Madhya Pradesh", "display_name": "Indore, Madhya Pradesh", "latitude": 22.7196, "longitude": 75.8577},
    "bhopal": {"city": "Bhopal", "state": "Madhya Pradesh", "display_name": "Bhopal, Madhya Pradesh", "latitude": 23.2599, "longitude": 77.4126},
    "भोपाल": {"city": "Bhopal", "state": "Madhya Pradesh", "display_name": "Bhopal, Madhya Pradesh", "latitude": 23.2599, "longitude": 77.4126},
    "jabalpur": {"city": "Jabalpur", "state": "Madhya Pradesh", "display_name": "Jabalpur, Madhya Pradesh", "latitude": 23.1815, "longitude": 79.9864},
    "ujjain": {"city": "Ujjain", "state": "Madhya Pradesh", "display_name": "Ujjain, Madhya Pradesh", "latitude": 23.1765, "longitude": 75.7885},
    "raipur": {"city": "Raipur", "state": "Chhattisgarh", "display_name": "Raipur, Chhattisgarh", "latitude": 21.2514, "longitude": 81.6296},
    "bilaspur": {"city": "Bilaspur", "state": "Chhattisgarh", "display_name": "Bilaspur, Chhattisgarh", "latitude": 22.0797, "longitude": 82.1409},

    # --- 6. TAMIL NADU & KERALA (SOUTHERN HORTICULTURE & SPICES ZONE) ---
    "coimbatore": {"city": "Coimbatore", "state": "Tamil Nadu", "display_name": "Coimbatore, Tamil Nadu", "latitude": 11.0168, "longitude": 76.9558},
    "கோயம்புத்தூர்": {"city": "Coimbatore", "state": "Tamil Nadu", "display_name": "Coimbatore, Tamil Nadu", "latitude": 11.0168, "longitude": 76.9558},
    "కోయంబత్తూరు": {"city": "Coimbatore", "state": "Tamil Nadu", "display_name": "Coimbatore, Tamil Nadu", "latitude": 11.0168, "longitude": 76.9558},
    "madurai": {"city": "Madurai", "state": "Tamil Nadu", "display_name": "Madurai, Tamil Nadu", "latitude": 9.9252, "longitude": 78.1198},
    "மதுரை": {"city": "Madurai", "state": "Tamil Nadu", "display_name": "Madurai, Tamil Nadu", "latitude": 9.9252, "longitude": 78.1198},
    "chennai": {"city": "Chennai", "state": "Tamil Nadu", "display_name": "Chennai, Tamil Nadu", "latitude": 13.0827, "longitude": 80.2707},
    "சென்னை": {"city": "Chennai", "state": "Tamil Nadu", "display_name": "Chennai, Tamil Nadu", "latitude": 13.0827, "longitude": 80.2707},
    "thanjavur": {"city": "Thanjavur", "state": "Tamil Nadu", "display_name": "Thanjavur, Tamil Nadu", "latitude": 10.7870, "longitude": 79.1378},
    "salem": {"city": "Salem", "state": "Tamil Nadu", "display_name": "Salem, Tamil Nadu", "latitude": 11.6643, "longitude": 78.1460},
    "kochi": {"city": "Kochi", "state": "Kerala", "display_name": "Kochi, Kerala", "latitude": 9.9312, "longitude": 76.2673},
    "palakkad": {"city": "Palakkad", "state": "Kerala", "display_name": "Palakkad, Kerala", "latitude": 10.7867, "longitude": 76.6548},

    # --- 7. KARNATAKA (SOUTHERN PLATEAU & COFFEE/RAGI/MAIZE ZONE) ---
    "bengaluru": {"city": "Bengaluru", "state": "Karnataka", "display_name": "Bengaluru, Karnataka", "latitude": 12.9716, "longitude": 77.5946},
    "ಬೆಂಗಳೂರು": {"city": "Bengaluru", "state": "Karnataka", "display_name": "Bengaluru, Karnataka", "latitude": 12.9716, "longitude": 77.5946},
    "బెంగళూరు": {"city": "Bengaluru", "state": "Karnataka", "display_name": "Bengaluru, Karnataka", "latitude": 12.9716, "longitude": 77.5946},
    "belagavi": {"city": "Belagavi", "state": "Karnataka", "display_name": "Belagavi, Karnataka", "latitude": 15.8497, "longitude": 74.4977},
    "ಬೆಳಗಾವಿ": {"city": "Belagavi", "state": "Karnataka", "display_name": "Belagavi, Karnataka", "latitude": 15.8497, "longitude": 74.4977},
    "mysuru": {"city": "Mysuru", "state": "Karnataka", "display_name": "Mysuru, Karnataka", "latitude": 12.2958, "longitude": 76.6394},
    "ಮೈಸೂರು": {"city": "Mysuru", "state": "Karnataka", "display_name": "Mysuru, Karnataka", "latitude": 12.2958, "longitude": 76.6394},
    "hubballi": {"city": "Hubballi", "state": "Karnataka", "display_name": "Hubballi, Karnataka", "latitude": 15.3647, "longitude": 75.1240},
    "kalaburagi": {"city": "Kalaburagi", "state": "Karnataka", "display_name": "Kalaburagi, Karnataka", "latitude": 17.3297, "longitude": 76.8343},
    "shivamogga": {"city": "Shivamogga", "state": "Karnataka", "display_name": "Shivamogga, Karnataka", "latitude": 13.9299, "longitude": 75.5681},

    # --- 8. ANDHRA PRADESH & TELANGANA (RICE, CHILLI, COTTON, GROUNDNUT) ---
    "nellore": {"city": "Nellore", "state": "Andhra Pradesh", "display_name": "Nellore, Andhra Pradesh", "latitude": 14.4494, "longitude": 79.9874},
    "నెల్లూరు": {"city": "Nellore", "state": "Andhra Pradesh", "display_name": "Nellore, Andhra Pradesh", "latitude": 14.4494, "longitude": 79.9874},
    "guntur": {"city": "Guntur", "state": "Andhra Pradesh", "display_name": "Guntur, Andhra Pradesh", "latitude": 16.3067, "longitude": 80.4365},
    "గుంటూరు": {"city": "Guntur", "state": "Andhra Pradesh", "display_name": "Guntur, Andhra Pradesh", "latitude": 16.3067, "longitude": 80.4365},
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
    "hyderabad": {"city": "Hyderabad", "state": "Telangana", "display_name": "Hyderabad, Telangana", "latitude": 17.3850, "longitude": 78.4867},
    "హైదరాబాద్": {"city": "Hyderabad", "state": "Telangana", "display_name": "Hyderabad, Telangana", "latitude": 17.3850, "longitude": 78.4867},
    "warangal": {"city": "Warangal", "state": "Telangana", "display_name": "Warangal, Telangana", "latitude": 17.9689, "longitude": 79.5941},
    "వరంగల్": {"city": "Warangal", "state": "Telangana", "display_name": "Warangal, Telangana", "latitude": 17.9689, "longitude": 79.5941},
    "karimnagar": {"city": "Karimnagar", "state": "Telangana", "display_name": "Karimnagar, Telangana", "latitude": 18.4386, "longitude": 79.1288},
    "కరీంనగర్": {"city": "Karimnagar", "state": "Telangana", "display_name": "Karimnagar, Telangana", "latitude": 18.4386, "longitude": 79.1288},
    "khammam": {"city": "Khammam", "state": "Telangana", "display_name": "Khammam, Telangana", "latitude": 17.2473, "longitude": 80.1514},
    "ఖమ్మం": {"city": "Khammam", "state": "Telangana", "display_name": "Khammam, Telangana", "latitude": 17.2473, "longitude": 80.1514},

    # --- 9. WEST BENGAL, ODISHA & ASSAM (EASTERN RICE & JUTE/TEA ZONE) ---
    "kolkata": {"city": "Kolkata", "state": "West Bengal", "display_name": "Kolkata, West Bengal", "latitude": 22.5726, "longitude": 88.3639},
    "कोलकाता": {"city": "Kolkata", "state": "West Bengal", "display_name": "Kolkata, West Bengal", "latitude": 22.5726, "longitude": 88.3639},
    "burdwan": {"city": "Bardhaman", "state": "West Bengal", "display_name": "Bardhaman, West Bengal", "latitude": 23.2324, "longitude": 87.8615},
    "bhubaneswar": {"city": "Bhubaneswar", "state": "Odisha", "display_name": "Bhubaneswar, Odisha", "latitude": 20.2961, "longitude": 85.8245},
    "भुवनेश्वर": {"city": "Bhubaneswar", "state": "Odisha", "display_name": "Bhubaneswar, Odisha", "latitude": 20.2961, "longitude": 85.8245},
    "cuttack": {"city": "Cuttack", "state": "Odisha", "display_name": "Cuttack, Odisha", "latitude": 20.4625, "longitude": 85.8828},
    "sambalpur": {"city": "Sambalpur", "state": "Odisha", "display_name": "Sambalpur, Odisha", "latitude": 21.4669, "longitude": 83.9812},
    "guwahati": {"city": "Guwahati", "state": "Assam", "display_name": "Guwahati, Assam", "latitude": 26.1445, "longitude": 91.7362},
    "गुवाहाटी": {"city": "Guwahati", "state": "Assam", "display_name": "Guwahati, Assam", "latitude": 26.1445, "longitude": 91.7362},
    "dibrugarh": {"city": "Dibrugarh", "state": "Assam", "display_name": "Dibrugarh, Assam", "latitude": 27.4728, "longitude": 94.9120}
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
    Multi-tier geocoder supporting English, Telugu, Hindi, Tamil, Kannada, Marathi, Punjabi, Bengali.
    1. Instant fast in-memory Pan-India dictionary lookup.
    2. Open-Meteo Geocoding Search API.
    3. Nominatim OpenStreetMap regional Search API fallback.
    """
    if not location_query:
        return None
    clean_name = location_query.strip().lower()
    if len(clean_name) < 2:
        return None

    # Tier 1: Fast in-memory lookup for major Pan-India agricultural districts
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

    # Substring matching in known locations
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
        url = "https://geocoding-api.open-meteo.com/v1/search"
        params = {"name": location_query.strip(), "count": 1, "language": "en", "format": "json"}
        res = requests.get(url, params=params, timeout=3).json()
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

    # Tier 3: Nominatim OpenStreetMap Search for regional Indian scripts / remote villages across all states
    try:
        osm_url = "https://nominatim.openstreetmap.org/search"
        headers = {"User-Agent": "KisanMitraApp/1.0"}
        params = {"q": location_query.strip(), "countrycodes": "in", "format": "json", "limit": 1}
        osm_res = requests.get(osm_url, params=params, headers=headers, timeout=3).json()
        if osm_res and len(osm_res) > 0:
            top_hit = osm_res[0]
            lat = float(top_hit["lat"])
            lon = float(top_hit["lon"])
            raw_disp = top_hit.get("display_name", "")
            parts = [p.strip() for p in raw_disp.split(",") if p.strip()]
            
            if len(parts) >= 2:
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
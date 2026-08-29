from pathlib import Path

i18n_code = '''
TRANSLATIONS = {
    "te": {
        "app_title": "కిసాన్ మిత్ర: AI వ్యవసాయ ఆపరేటింగ్ సిస్టమ్",
        "app_sub": "లైవ్ మార్కెట్ ధరలు • ఆటో లొకేషన్ • ఆకు తెగుళ్ల గుర్తింపు • వాట్సాప్ & టెలిగ్రామ్ కమ్యూనిటీ",
        "select_lang": "భాషను ఎంచుకోండి",
        "location": "గుర్తించిన ప్రాంతం",
        "farmer_profile": "రైతు ప్రొఫైల్",
        "weather": "ప్రత్యక్ష వాతావరణం",
        "rain_alert": "వర్షం సూచన: మందులు పిచికారీ చేయవద్దు.",
        "tabs": {
            "community": "👥 రైతు కమ్యూనిటీ",
            "crops": "🌱 అనువైన పంటలు",
            "mandi": "💰 మార్కెట్ లైవ్ ధరలు",
            "voice": "🎙️ వాయిస్ సలహా",
            "leaf": "📷 ఆకు డాక్టర్ (స్కాన్)",
            "radar": "🚨 తెగుళ్ల రాడార్",
            "water": "💧 నీటి పారుదల",
            "soil": "🧪 నేల & NPK ఎరువులు",
            "calendar": "📅 పంట కాలెండర్",
            "profit": "📈 ఆదాయం అంచనా",
            "schemes": "🏛️ ప్రభుత్వ పథకాలు",
            "pdf": "📜 ప్రిస్క్రిప్షన్ కార్డ్"
        },
        "community_title": "ప్రాంతీయ రైతు వాట్సాప్ & టెలిగ్రామ్ గ్రూపులు",
        "community_sub": "మీ మండలం మరియు జిల్లా రైతులతో చేరి లైవ్ మార్కెట్ రేట్లు మరియు వ్యవసాయ సలహాలు పొందండి.",
        "share_whatsapp": "📲 మిత్రులకు WhatsApp లో షేర్ చేయండి",
        "crops_title": "ప్రాంతానికి అత్యంత అనువైన సమగ్ర పంటలు",
        "crops_sub": "నేల స్వభావం, వర్షపాతం మరియు మార్కెట్ డిమాండ్ ఆధారంగా సిఫార్సులు",
        "mandi_title": "క్లస్టర్ ప్రత్యక్ష మార్కెట్ ధరల సూచిక",
        "voice_title": "మైక్ మాట్లాడండి - వాయిస్ అసిస్టెంట్",
        "voice_listen": "వింటున్నాను...",
        "leaf_title": "ఆకు తెగుళ్ల స్కానర్ & చికిత్స ప్రిస్క్రిప్షన్",
        "scan_btn": "⚡ తెగులును గుర్తించు",
        "irrigation_title": "స్మార్ట్ నీటి లెక్కలు & పంపు రన్-టైమ్",
        "irrigation_btn": "💧 నేటి నీటి అవసరం లెక్కించు",
        "soil_title": "నేల సారవంతం & NPK ఎరువుల మోతాదు",
        "soil_btn": "🧪 సరైన ఎరువుల ప్రిస్క్రిప్షన్",
        "profit_title": "దిగుబడి & నికర లాభం అంచనా",
        "profit_btn": "📈 లాభం లెక్కించు",
        "download_pdf": "📄 హెల్త్ కార్డ్ డౌన్‌లోడ్ (PDF)"
    },
    "en": {
        "app_title": "Kisan Mitra: AI Agricultural Operating System",
        "app_sub": "Live APMC Mandi Rates • Auto Geolocation • Leaf Vision • WhatsApp & Telegram Community",
        "select_lang": "Select Interface Language",
        "location": "Detected Location",
        "farmer_profile": "Farmer Profile",
        "weather": "Live Local Weather",
        "rain_alert": "Rain Alert: Delay pesticide/fertilizer spraying.",
        "tabs": {
            "community": "👥 Farmer Community",
            "crops": "🌱 Suitable Crops",
            "mandi": "💰 Live Mandi Rates",
            "voice": "🎙️ Voice Advisory",
            "leaf": "📷 Leaf Disease Doctor",
            "radar": "🚨 Pest Alert Radar",
            "water": "💧 Smart Irrigation",
            "soil": "🧪 Soil Health & NPK",
            "calendar": "📅 Crop Calendar",
            "profit": "📈 Yield & Profit",
            "schemes": "🏛️ Govt Schemes",
            "pdf": "📜 Prescription PDF"
        },
        "community_title": "Regional WhatsApp & Telegram Farmer Groups",
        "community_sub": "Connect with local cluster farmers for real-time market arrivals, rentals, and expert agronomy advice.",
        "share_whatsapp": "📲 Share with Friends on WhatsApp",
        "crops_title": "Optimal Recommended Crop Portfolio",
        "crops_sub": "Auto-ranked based on soil composition, annual rainfall, and APMC market access.",
        "mandi_title": "Live Regulated APMC Mandi Trading Rates",
        "voice_title": "Voice-to-Voice Farmer Advisory",
        "voice_listen": "Listening...",
        "leaf_title": "Universal Crop Leaf Diagnostic Scanner",
        "scan_btn": "⚡ Scan & Diagnose Leaf",
        "irrigation_title": "Smart Evapotranspiration Irrigation & Pump Runtime",
        "irrigation_btn": "💧 Calculate Water Requirement",
        "soil_title": "Soil Nutrient & NPK Fertilizer Recommendation",
        "soil_btn": "🧪 Calculate Fertilizer Dose",
        "profit_title": "Crop Harvest Yield & Revenue Forecaster",
        "profit_btn": "📈 Forecast Farm Economics",
        "download_pdf": "📄 Download Health Card (PDF)"
    }
}

def get_text(lang_key: str = "te") -> dict:
    return TRANSLATIONS.get(lang_key, TRANSLATIONS["te"])
'''
Path("src/tools/i18n.py").write_text(i18n_code, encoding="utf-8")
print("✅ i18n localization dictionary created successfully!")
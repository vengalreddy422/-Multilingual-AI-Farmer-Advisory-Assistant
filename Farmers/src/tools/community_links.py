import urllib.parse
from typing import Dict, Any, List

def get_regional_communities(location_name: str) -> Dict[str, Any]:
    """
    Generates dynamic WhatsApp and Telegram group links 
    tailored to the farmer's specific Mandal and District.
    """
    loc_clean = location_name.split(",")[0].strip()
    district_clean = "Annamayya" if "Kurabala" in loc_clean or "Madanapalle" in loc_clean else loc_clean

    whatsapp_groups = [
        {
            "name": f"🌿 {loc_clean} రైతు మిత్ర గ్రూప్ (Farmer Hub)",
            "platform": "WhatsApp",
            "category": "General Agronomy & Crop Chat",
            "members": "740+ రైతులు",
            "icon": "💬",
            "link": f"https://chat.whatsapp.com/invite/sample_{loc_clean.lower()}_farmers",
            "description": f"{loc_clean} మండల రైతులందరి రోజువారీ వ్యవసాయ సమస్యలు మరియు అనుభవాల మార్పిడి."
        },
        {
            "name": f"🍅 {district_clean} మార్కెట్ & లైవ్ APMC ధరలు",
            "platform": "WhatsApp",
            "category": "Daily Mandi Price Alerts",
            "members": "1,020+ రైతులు & వ్యాపారులు",
            "icon": "💰",
            "link": f"https://chat.whatsapp.com/invite/sample_{district_clean.lower()}_mandi",
            "description": f"మదనపల్లె, గుంటూరు మరియు పరిసర మార్కెట్ల ప్రతిరోజూ ఉదయం టమాటా, వేరుశనగ లైవ్ ధరల అప్‌డేట్స్."
        },
        {
            "name": f"🚜 {loc_clean} యంత్రాల అద్దె & డ్రోన్ స్ప్రేయింగ్",
            "platform": "WhatsApp",
            "category": "Machinery & Drone Rentals",
            "members": "380+ సభ్యులు",
            "icon": "🚜",
            "link": f"https://chat.whatsapp.com/invite/sample_{loc_clean.lower()}_machinery",
            "description": "ట్రాక్టర్లు, రోటవేటర్లు, హార్వెస్టర్లు మరియు తక్కువ ధరకు డ్రోన్ స్ప్రేయింగ్ బుకింగ్స్."
        }
    ]

    telegram_channels = [
        {
            "name": f"🚨 {district_clean} KVK సైంటిస్టుల అధికారిక ఛానల్",
            "platform": "Telegram",
            "category": "Official KVK Scientists & Pest Alerts",
            "members": "4,500+ సభ్యులు",
            "icon": "📢",
            "link": f"https://t.me/KVK_{district_clean}_AgriAlerts",
            "description": "వ్యవసాయ విశ్వవిద్యాలయ శాస్త్రవేత్తల నుండి నేరుగా చీడపీడల నివారణ మరియు వాతావరణ హెచ్చరికలు."
        },
        {
            "name": f"🌾 ఆంధ్రప్రదేశ్ దేశవాళీ విత్తనాలు & ప్రకృతి వ్యవసాయం",
            "platform": "Telegram",
            "category": "Organic Farming & Seed Exchange",
            "members": "8,900+ సభ్యులు",
            "icon": "🌱",
            "link": "https://t.me/AP_Natural_Farming_Seeds",
            "description": "దేశీ విత్తనాల కొనుగోలు, జీవామృతం తయారీ మరియు సహజ ఎరువుల తయారీ విధానాల సమాచారం."
        }
    ]

    # Pre-formatted WhatsApp share text for the farmer
    share_msg = f"నమస్కారం! మన {loc_clean} మండల రైతుల కోసం కిసాన్ మిత్ర (Kisan Mitra) AI వేదికలో చేరండి. ఇక్కడ లైవ్ వాతావరణం, పంటల వ్యాధి గుర్తింపు మరియు గ్రూప్ లింక్స్ లభిస్తాయి."
    encoded_share = urllib.parse.quote(share_msg)
    share_url = f"https://api.whatsapp.com/send?text={encoded_share}"

    return {
        "mandal": loc_clean,
        "district": district_clean,
        "whatsapp_groups": whatsapp_groups,
        "telegram_channels": telegram_channels,
        "share_url": share_url
    }

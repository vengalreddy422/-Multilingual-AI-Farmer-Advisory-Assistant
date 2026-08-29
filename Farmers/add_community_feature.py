from pathlib import Path

# --- 1. src/tools/community_links.py ---
community_code = '''import urllib.parse
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
'''
Path("src/tools/community_links.py").write_text(community_code, encoding="utf-8")

# --- 2. Update app.py to integrate the Community Tab ---
app_code = '''import streamlit as st
from PIL import Image
from datetime import date
from dotenv import load_dotenv

load_dotenv()

from config.settings import settings
from src.database.session_state import init_session, append_message
from src.database.db_ledger import log_diagnostic, get_recent_history, get_dynamic_community_outbreaks
from src.tools.weather import fetch_weather
from src.tools.soil_advisor import analyze_soil_npk
from src.tools.dynamic_engine import (
    auto_detect_farmer_location,
    get_location_crop_suitability,
    get_live_dynamic_mandi_rates
)
from src.tools.community_links import get_regional_communities
from src.tools.agri_modules import (
    get_crop_calendar, calculate_irrigation, forecast_yield_and_profit,
    get_dynamic_schemes, get_dynamic_service_centers
)
from src.tools.pdf_generator import generate_pdf_health_card
from src.vision.disease_classifier import PlantDiseaseClassifier
from src.intelligence.rag_engine import AgriRAGEngine
from src.intelligence.advisory_chain import AdvisoryOrchestrator
from src.audio.speech_to_text import transcribe_audio_bytes
from src.audio.text_to_speech import generate_voice_audio

st.set_page_config(page_title="Kisan Mitra - Dynamic Farm AI", page_icon="🌾", layout="wide")
init_session()

# High-Speed Cached Singletons
@st.cache_resource(show_spinner=False)
def load_vision_classifier():
    return PlantDiseaseClassifier()

@st.cache_resource(show_spinner=False)
def load_rag_and_chain():
    return AgriRAGEngine(), AdvisoryOrchestrator()

@st.cache_data(ttl=300, show_spinner=False)
def get_cached_weather(city_str):
    return fetch_weather(city_str)

@st.cache_data(ttl=600, show_spinner=False)
def get_cached_location():
    return auto_detect_farmer_location()

classifier = load_vision_classifier()
rag_engine, orchestrator = load_rag_and_chain()

detected_loc_data = get_cached_location()
default_location_name = detected_loc_data["location_name"]

# Header
st.markdown("""
<div style="background: linear-gradient(135deg, #1b5e20, #2e7d32); color: white; padding: 20px; border-radius: 16px; text-align: center; margin-bottom: 15px;">
    <h1 style="color:white; margin:0;">🌾 కిసాన్ మిత్ర / Kisan Mitra</h1>
    <p style="color:#e8f5e9; margin:4px 0 0 0; font-size:1.15rem;">
        🟢 <b>ఆటో లొకేషన్ • ప్రాంతీయ పంటల సూచిక • లైవ్ మార్కెట్ • వాట్సాప్ & టెలిగ్రామ్ కమ్యూనిటీ</b>
    </p>
</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("### 📍 గుర్తించిన ప్రాంతం (Location)")
    farmer_location = st.text_input("Village / Mandal", value=default_location_name)
    
    st.markdown("### 👤 రైతు ప్రొఫైల్ (Member Profile)")
    test_member = st.selectbox(
        "Active Farmer Account",
        ["Kammari Charan Kumar (2.5 Acres)", "Ramesh Reddy (5.0 Acres)", "Siva Naidu (1.5 Acres)"]
    )
    farmer_name_clean = test_member.split(" (")[0]
    farmer_acres = 2.5 if "2.5" in test_member else (5.0 if "5.0" in test_member else 1.5)

    st.divider()
    st.markdown("### 🌐 భాష / Language")
    lang_code = st.selectbox(
        "Language",
        options=list(settings.SUPPORTED_LANGUAGES.keys()),
        format_func=lambda x: f"🗣️ {settings.SUPPORTED_LANGUAGES[x]}",
        index=0,
        label_visibility="collapsed"
    )
    lang_name = settings.SUPPORTED_LANGUAGES[lang_code]

    st.divider()
    st.markdown("### 🌦️ ప్రత్యక్ష వాతావరణం (Live Weather)")
    weather_info = get_cached_weather(farmer_location)
    if weather_info.get("status") == "success":
        st.success(f"📍 {weather_info['location']}")
        c1, c2 = st.columns(2)
        c1.metric("🌡️ Temp", f"{weather_info['temperature']} °C")
        c2.metric("💧 Humidity", f"{weather_info['humidity']}%")
        st.info(f"⛅ {weather_info['condition']} | 💨 Wind: {weather_info['wind_speed']} km/h")
        if weather_info.get("rain_risk"):
            st.warning("⚠️ **వర్షం హెచ్చరిక:** మందులు స్ప్రే చేయవద్దు.")

# Main Navigation Tabs (Includes Community)
tabs = st.tabs([
    "👥 రైతు కమ్యూనిటీ (Community)",
    "🌱 అనువైన అన్ని పంటలు (All Crops)",
    "💰 లైవ్ మార్కెట్ ధరలు (Live Mandi)",
    "🎙️ మైక్ మాట్లాడండి (Voice)",
    "📷 ఆకు స్కానర్ (Leaf Doctor)",
    "🚨 కమ్యూనిటీ రాడార్ (Pest Radar)",
    "💧 నీటి పంపు (Smart Water)",
    "🧪 ఎరువుల మోతాదు (NPK Soil)",
    "📅 పంట కాలెండర్ (Calendar)",
    "📈 ఆదాయం అంచనా (Profit)",
    "🏛️ ప్రభుత్వ పథకాలు (Schemes)",
    "📜 ప్రిస్క్రిప్షన్ & PDF"
])

# TAB 1: REGIONAL WHATSAPP & TELEGRAM COMMUNITY
with tabs[0]:
    st.subheader(f"👥 {farmer_location} ప్రాంతీయ రైతు కమ్యూనిటీ గ్రూపులు")
    st.caption("మీ మండలం మరియు జిల్లా రైతులతో చేరి లైవ్ మార్కెట్ రేట్లు, యంత్రాల అద్దె మరియు వ్యవసాయ సలహాలు పంచుకోండి.")

    comm_data = get_regional_communities(farmer_location)

    col_btn1, col_btn2 = st.columns([2, 1])
    with col_btn1:
        st.info(f"📍 ప్రస్తుత క్లస్టర్: **{comm_data['mandal']} మండలం / {comm_data['district']} జిల్లా**")
    with col_btn2:
        st.link_button("📲 మిత్రులకు WhatsApp లో షేర్ చేయండి", comm_data["share_url"], use_container_width=True)

    st.markdown("### 🟢 వాట్సాప్ గ్రూపులు (WhatsApp Farmer Groups)")
    col_w1, col_w2, col_w3 = st.columns(3)
    cols_w = [col_w1, col_w2, col_w3]

    for idx, grp in enumerate(comm_data["whatsapp_groups"]):
        with cols_w[idx % 3]:
            with st.container(border=True):
                st.markdown(f"#### {grp['name']}")
                st.caption(f"📂 వర్గం: **{grp['category']}**")
                st.write(f"👥 సభ్యులు: **{grp['members']}**")
                st.write(grp["description"])
                st.link_button(f"🟢 Join WhatsApp Group", grp["link"], use_container_width=True)

    st.markdown("### 🔵 టెలిగ్రామ్ ఛానల్స్ & ఫోరమ్స్ (Telegram Channels)")
    col_t1, col_t2 = st.columns(2)
    cols_t = [col_t1, col_t2]

    for idx, ch in enumerate(comm_data["telegram_channels"]):
        with cols_t[idx % 2]:
            with st.container(border=True):
                st.markdown(f"#### {ch['name']}")
                st.caption(f"📂 కేటగిరీ: **{ch['category']}**")
                st.write(f"👥 సభ్యులు: **{ch['members']}**")
                st.write(ch["description"])
                st.link_button(f"🔵 Join Telegram Channel", ch["link"], use_container_width=True)

# TAB 2: MULTI-CROP SUITABILITY
with tabs[1]:
    st.subheader(f"🌱 {farmer_location} ప్రాంతానికి అనువైన సమగ్ర పంటలు")
    crop_intel = get_location_crop_suitability(farmer_location)

    col_m1, col_m2, col_m3 = st.columns(3)
    col_m1.info(f"🏛️ **అగ్రో జోన్:** {crop_intel['zone_name']}")
    col_m2.info(f"🟤 **నేల స్వభావం:** {crop_intel['soil_profile']}")
    col_m3.info(f"🌧️ **వాతావరణం:** {crop_intel['climate_profile']}")

    for c in crop_intel["all_crops"]:
        with st.container(border=True):
            head_col, score_col = st.columns([3, 1])
            head_col.markdown(f"### {c['crop']}")
            head_col.caption(f"వర్గం: **{c['category']}** | సీజన్: **{c['season']}**")
            score_col.metric("అనుకూలత స్కోరు", f"{c['suitability']}%")

            d_col1, d_col2 = st.columns(2)
            with d_col1:
                st.write(f"🧬 **సిఫార్సు చేసిన రకాలు:** `{c['varieties']}`")
                st.write(f"💧 **నీటి అవసరం:** {c['water_need']}")
            with d_col2:
                st.write(f"🔬 **అనుకూలత కారణం:** {c['why_suitable']}")
                st.write(f"🚛 **మార్కెట్ రవాణా:** **{c['market_link']}**")

# TAB 3: DYNAMIC LIVE MANDI PRICES
with tabs[2]:
    st.subheader(f"💰 {farmer_location} క్లస్టర్ లైవ్ మార్కెట్ ధరలు")
    live_prices = get_live_dynamic_mandi_rates(farmer_location)

    cols = st.columns(3)
    for idx, p in enumerate(live_prices):
        with cols[idx % 3]:
            with st.container(border=True):
                st.markdown(f"### {p['crop']}")
                st.caption(f"యార్డ్: **{p['primary_market']}**")
                st.metric(
                    label=f"సగటు ధర: ₹{p['modal_price']:,} / Q",
                    value=f"₹{p['modal_price']:,}",
                    delta=p["trend"]
                )
                st.write(f"ధరల పరిధి: ₹{p['min_price']:,} - ₹{p['max_price']:,}")
                st.write(f"రాక: **{p['arrivals_tonnes']} టన్నులు**")
                st.caption(f"స్టేటస్: {p['updated']}")

# TAB 4: VOICE-TO-VOICE
with tabs[3]:
    st.subheader("🗣️ మాట్లాడండి - వాయిస్ సలహా")
    audio_val = st.audio_input("🔴 RECORD VOICE HERE")
    user_query = None

    if audio_val is not None:
        audio_bytes = audio_val.read()
        with st.spinner("🎧 వింటున్నాను..."):
            recognized_text = transcribe_audio_bytes(audio_bytes, lang_code=lang_code)
            if recognized_text:
                user_query = recognized_text
                st.success(f"🗣️ **మీరు అడిగినది:** {recognized_text}")

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            if "audio_bytes" in msg and msg["audio_bytes"]:
                st.audio(msg["audio_bytes"], format="audio/mp3")

    text_input = st.chat_input("లేదా ఇక్కడ టైప్ చేయండి...")
    if text_input:
        user_query = text_input

    if user_query:
        append_message("user", user_query)
        with st.chat_message("user"):
            st.markdown(user_query)

        with st.chat_message("assistant"):
            with st.spinner("🌾 సమాధానం సిద్ధం చేస్తున్నాను..."):
                advice = orchestrator.generate_advisory(
                    query=user_query,
                    language=lang_name,
                    weather_info=weather_info if weather_info.get("status") == "success" else None,
                    disease_data=st.session_state.latest_disease,
                    soil_data=st.session_state.latest_soil
                )
                st.markdown(advice)
                try:
                    audio_fp = generate_voice_audio(advice, lang=lang_code)
                    audio_data = audio_fp.getvalue()
                    st.audio(audio_data, format="audio/mp3", autoplay=True)
                    st.session_state.messages.append({"role": "assistant", "content": advice, "audio_bytes": audio_data})
                except Exception:
                    append_message("assistant", advice)

# TAB 5: LEAF SCANNER
with tabs[4]:
    st.subheader("📷 Universal Leaf Disease Scanner")
    input_mode = st.radio("ఇన్పుట్", ["📷 లైవ్ కెమెరా", "📁 ఫోటో అప్‌లోడ్"], horizontal=True)
    img_to_analyze = None

    if input_mode == "📷 లైవ్ కెమెరా":
        cam_shot = st.camera_input("ఆకు ఫోటో తీయండి")
        if cam_shot:
            img_to_analyze = Image.open(cam_shot)
    else:
        uploaded_file = st.file_uploader("ఆకు ఫోటోను ఎంచుకోండి", type=["jpg", "jpeg", "png", "webp", "heic"])
        if uploaded_file:
            img_to_analyze = Image.open(uploaded_file)

    if img_to_analyze:
        c_img, c_diag = st.columns([1, 2])
        with c_img:
            st.image(img_to_analyze, caption="స్కాన్ చేసిన ఆకు", use_container_width=True)
        with c_diag:
            if st.button("⚡ తెగులును గుర్తించు (Run Diagnostic)", use_container_width=True):
                result = classifier.predict(img_to_analyze)
                st.session_state.latest_disease = result
                log_diagnostic(farmer_name_clean, farmer_location, result["leaf_name"], result["disease"], result["confidence"], result["treatment"])

                st.success(f"🌱 **గుర్తించిన పంట:** {result['leaf_name']}")
                st.info(f"🔬 **వచ్చిన సమస్య:** {result['disease']} ({int(result['confidence']*100)}% Match)")
                st.write(f"🦠 **కారకం:** {result['pathogen']}")
                st.write(f"🔍 **లక్షణాలు:** {result['symptoms']}")
                st.warning(f"💊 **నివారణ మందులు:** {result['treatment']}")

# TAB 6: PEST RADAR
with tabs[5]:
    st.subheader(f"🚨 {farmer_location} పరిసర గ్రామాల తెగుళ్ల రాడార్")
    outbreaks = get_dynamic_community_outbreaks(farmer_location)
    if outbreaks:
        for ob in outbreaks:
            with st.container(border=True):
                st.markdown(f"### 📍 {ob['mandal']} మండలం | పంట: **{ob['crop']}**")
                st.markdown(f"⚠️ సమస్య: **{ob['threat']}** (నమోదైన కేసులు: `{ob['reported_cases']}` మంది రైతులు)")
                st.info(f"తీవ్రత: **{ob['severity']}**")
                st.write(f"🛡️ **క్షేత్రస్థాయి సూచన:** {ob['advisory']}")

# TAB 7: IRRIGATION
with tabs[6]:
    st.subheader("💧 స్మార్ట్ నీటి లెక్కలు & పంపు రన్-టైమ్")
    c_ir1, c_ir2 = st.columns(2)
    with c_ir1:
        irr_crop = st.selectbox("సాగు చేస్తున్న పంట", ["Tomato", "Groundnut", "Chilli", "Cotton", "Maize", "Rice"])
        acres_in = st.number_input("విస్తీర్ణం (ఎకరాలు)", value=farmer_acres, min_value=0.5, step=0.5)
    with c_ir2:
        pump_hp = st.number_input("మోటారు సామర్థ్యం (HP)", value=5.0, min_value=1.0, step=1.0)

    if st.button("💧 నేటి నీటి అవసరం లెక్కించు", use_container_width=True):
        irr_res = calculate_irrigation(irr_crop, acres_in, pump_hp, weather_info.get("temperature", 30.0))
        st.success(f"💧 **ఈరోజు కావలసిన మొత్తం నీరు:** {irr_res['liters_per_day']:,} లీటర్లు")
        st.info(f"⏱️ **మోటారు వేయవలసిన సమయం:** {irr_res['pump_runtime_hours']} గంటలు")
        st.write(irr_res['recommendation'])

# TAB 8: SOIL NPK
with tabs[7]:
    st.subheader("🧪 నేల సారవంతం & NPK ఎరువుల మోతాదు")
    col1, col2 = st.columns(2)
    with col1:
        s_crop = st.selectbox("ఎరువుల సిఫార్సు కోసం పంట", ["Tomato", "Groundnut", "Chilli", "Cotton", "Maize"])
        n_in = st.number_input("Nitrogen (N) kg/ha", value=80.0)
        p_in = st.number_input("Phosphorus (P) kg/ha", value=30.0)
    with col2:
        k_in = st.number_input("Potassium (K) kg/ha", value=35.0)
        ph_in = st.number_input("pH విలువ", value=6.5, min_value=1.0, max_value=14.0)

    if st.button("🧪 సరైన ఎరువుల ప్రిస్క్రిప్షన్"):
        res = analyze_soil_npk(s_crop, n_in, p_in, k_in, ph_in)
        st.session_state.latest_soil = res
        for item in res["recommendations"]:
            st.info(item)

# TAB 9: CALENDAR
with tabs[8]:
    st.subheader("📅 దశలవారీ పంట పనుల కాలెండర్")
    cal_crop = st.selectbox("పంట కాలెండర్", ["Tomato", "Cotton", "Rice"])
    sow_d = st.date_input("విత్తిన తేదీ", value=date.today())
    schedule = get_crop_calendar(cal_crop, sow_d)
    for title, dt, desc in schedule:
        with st.expander(f"📍 {dt.strftime('%d %b %Y')} - {title}", expanded=True):
            st.write(desc)

# TAB 10: PROFIT
with tabs[9]:
    st.subheader("📈 దిగుబడి & లాభం అంచనా")
    cy1, cy2 = st.columns(2)
    with cy1:
        f_crop = st.selectbox("దిగుబడి పంట", ["Tomato", "Cotton", "Rice", "Wheat", "Maize"])
        f_acres = st.number_input("సాగు విస్తీర్ణం (Acres)", value=farmer_acres, min_value=0.5)
    with cy2:
        f_price = st.number_input("అంచనా క్వింటాల్ ధర (₹/Quintal)", value=2200.0, step=100.0)

    if st.button("📈 లాభం లెక్కించు"):
        f_res = forecast_yield_and_profit(f_crop, f_acres, f_price)
        st.metric("అంచనా దిగుబడి", f"{f_res['expected_yield_quintals']} క్వింటాళ్లు")
        c_m1, c_m2, c_m3 = st.columns(3)
        c_m1.metric("పెట్టుబడి (Cost)", f"₹{f_res['total_cost']:,}")
        c_m2.metric("మొత్తం అమ్మకం (Gross)", f"₹{f_res['gross_revenue']:,}")
        c_m3.metric("నికర లాభం (Net Profit)", f"₹{f_res['net_profit']:,}", delta=f"₹{f_res['net_profit']:,}")

# TAB 11: SCHEMES
with tabs[10]:
    st.subheader(f"🏛️ {farmer_name_clean} గారి కోసం అర్హత గల పథకాలు")
    matched_schemes = get_dynamic_schemes(farmer_acres)
    for sch in matched_schemes:
        with st.container(border=True):
            st.markdown(f"### 🏷️ {sch['name']}")
            st.write(f"🎁 **లబ్ది:** {sch['benefit']}")
            st.caption(f"👤 **అర్హత:** {sch['eligibility']}")

# TAB 12: PDF & HISTORY
with tabs[11]:
    st.subheader("📜 డిజిటల్ ప్రిస్క్రిప్షన్ & టెస్టింగ్ రికార్డులు")
    col_pdf1, col_pdf2 = st.columns([1, 2])
    with col_pdf1:
        farmer_n = st.text_input("రైతు పేరు", value=farmer_name_clean)
        if st.button("📄 హెల్త్ కార్డ్ డౌన్‌లోడ్ (PDF)", use_container_width=True):
            pdf_fp = generate_pdf_health_card(
                farmer_name=farmer_n,
                location=weather_info.get("location", farmer_location),
                disease_data=st.session_state.latest_disease,
                soil_data=st.session_state.latest_soil,
                weather_data=weather_info
            )
            st.download_button(
                label="⬇️ PDF డౌన్‌లోడ్ చేసుకోండి",
                data=pdf_fp,
                file_name="Kisan_Mitra_Farm_Health_Card.pdf",
                mime="application/pdf",
                use_container_width=True
            )

    with col_pdf2:
        st.markdown("### 🗄️ గత పరీక్షల రికార్డులు")
        history = get_recent_history(10)
        if history:
            for row in history:
                st.write(f"• **{row[0]}** | రైతు: `{row[1]}` ({row[2]}) | ఆకు: **{row[3]}** | ఫలితం: *{row[4]}* ({int(row[5]*100)}%)")
        else:
            st.info("ఇంకా ఎలాంటి రికార్డులు నమోదు కాలేదు.")
'''
Path("app.py").write_text(app_code, encoding="utf-8")
print("✅ WhatsApp & Telegram Community features successfully installed!")
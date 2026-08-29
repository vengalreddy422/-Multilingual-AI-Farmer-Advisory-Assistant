from pathlib import Path

code = """import streamlit as st
from PIL import Image
from datetime import date
from dotenv import load_dotenv

load_dotenv()

from config.settings import settings
from src.database.session_state import init_session, append_message
from src.database.db_ledger import log_diagnostic, get_recent_history
from src.tools.weather import fetch_weather
from src.tools.mandi_prices import get_mandi_rates
from src.tools.soil_advisor import analyze_soil_npk
from src.tools.agri_modules import (
    get_crop_calendar, calculate_irrigation, forecast_yield_and_profit,
    GOVERNMENT_SCHEMES, COMMUNITY_RADAR_ALERTS, NEARBY_SERVICE_CENTERS
)
from src.tools.pdf_generator import generate_pdf_health_card
from src.vision.disease_classifier import PlantDiseaseClassifier
from src.intelligence.rag_engine import AgriRAGEngine
from src.intelligence.advisory_chain import AdvisoryOrchestrator
from src.audio.speech_to_text import transcribe_audio_bytes
from src.audio.text_to_speech import generate_voice_audio

st.set_page_config(page_title="Kisan Mitra - AI Farmer Hub", page_icon="🌾", layout="wide")
init_session()

# High-Speed Cached Singletons
@st.cache_resource(show_spinner=False)
def load_vision_classifier():
    return PlantDiseaseClassifier()

@st.cache_resource(show_spinner=False)
def load_rag_and_chain():
    return AgriRAGEngine(), AdvisoryOrchestrator()

@st.cache_data(ttl=600, show_spinner=False)
def get_cached_weather(city_str):
    return fetch_weather(city_str)

classifier = load_vision_classifier()
rag_engine, orchestrator = load_rag_and_chain()

# --- CUSTOM CSS FOR HIGH-VISIBILITY FARMER ICONS & BUTTONS ---
st.markdown(\"\"\"
<style>
    .big-voice-card {
        background: linear-gradient(135deg, #1b5e20, #2e7d32);
        color: white;
        padding: 22px;
        border-radius: 18px;
        text-align: center;
        margin-bottom: 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.15);
    }
    .big-voice-card h1 {
        color: #ffffff;
        font-size: 2.2rem;
        margin-bottom: 4px;
    }
    .big-voice-card p {
        font-size: 1.15rem;
        color: #e8f5e9;
    }
    .stAudioInput {
        border: 3px solid #2e7d32;
        border-radius: 16px;
        padding: 8px;
        background-color: #f1f8e9;
    }
</style>
\"\"\", unsafe_allow_html=True)

# --- HEADER WITH REGIONAL VISUAL CUES ---
st.markdown(\"\"\"
<div class="big-voice-card">
    <h1>🎙️ కిసాన్ మిత్ర / किसान मित्र / Kisan Mitra</h1>
    <p>🟢 <b>మాట్లాడండి • ఫోటో తీయండి • సూచనలు వినండి</b> (Speak • Snap Leaf • Listen Advice)</p>
</div>
\"\"\", unsafe_allow_html=True)

# --- SIDEBAR (VISUAL CUES) ---
with st.sidebar:
    st.markdown("### 🌐 భాష / भाषा / Language")
    lang_code = st.selectbox(
        "Select Language",
        options=list(settings.SUPPORTED_LANGUAGES.keys()),
        format_func=lambda x: f"🗣️ {settings.SUPPORTED_LANGUAGES[x]}",
        index=0,
        label_visibility="collapsed"
    )
    lang_name = settings.SUPPORTED_LANGUAGES[lang_code]

    st.divider()
    st.markdown("### 🌦️ వాతావరణం / Weather")
    village_input = st.text_input("Village / ఊరు", value="Kurabala Kota")
    weather_info = get_cached_weather(village_input)

    if weather_info.get("status") == "success":
        st.success(f"📍 {weather_info['location']}")
        c1, c2 = st.columns(2)
        c1.metric("🌡️ Temp", f"{weather_info['temperature']} °C")
        c2.metric("💧 Humidity", f"{weather_info['humidity']}%")
        st.info(f"⛅ {weather_info['condition']}")
        if weather_info.get("rain_risk"):
            st.warning("⚠️ వర్షం సూచన (Rain Alert): మందులు స్ప్రే చేయవద్దు.")

    st.divider()
    st.markdown("### 💰 మార్కెట్ ధరలు / Mandi Rates")
    crop_mandi = st.selectbox("పంట / Commodity", ["Cotton", "Rice", "Tomato", "Wheat", "Maize"])
    rates = get_mandi_rates(crop_mandi)
    for r in rates:
        st.write(f"📍 **{r['market']}**: 💵 ₹{r['modal_price']}/Q")

# --- LARGE ICON NAVIGATION TABS FOR EASY IDENTIFICATION ---
tabs = st.tabs([
    "🎙️ మైక్ మాట్లాడండి (Voice)",
    "📷 ఆకు స్కానర్ (Leaf Doctor)",
    "💧 నీటి పంపు (Water/Pump)",
    "🧪 ఎరువుల మోతాదు (NPK/Soil)",
    "📅 పంట కాలెండర్ (Calendar)",
    "📈 ఆదాయం అంచనా (Profit)",
    "🏛️ ప్రభుత్వ పథకాలు (Schemes)",
    "🚨 పురుగు హెచ్చరిక (Pest Alert)",
    "🏢 రైతు కేంద్రాలు (RBK/CHC)",
    "📜 ప్రిస్క్రిప్షన్ (PDF Card)"
])

# 1. VOICE TAB (PROMINENT LARGE MIC INTERFACE)
with tabs[0]:
    st.markdown("### 🎙️ మైక్ బటన్ నొక్కి మాట్లాడండి (Press Mic & Speak)")
    st.info("💡 **ఉదాహరణలు:** 'టమాటాలో ఆకుముడత నివారణ ఎలా?' లేదా 'వరిలో ఎరువుల మోతాదు ఎంత?'")

    audio_val = st.audio_input("🔴 RECORD VOICE HERE", label_visibility="collapsed")
    user_query = None

    if audio_val is not None:
        audio_bytes = audio_val.read()
        with st.spinner("🎧 వింటున్నాను... (Listening)..."):
            recognized_text = transcribe_audio_bytes(audio_bytes, lang_code=lang_code)
            if recognized_text:
                user_query = recognized_text
                st.success(f"🗣️ **మీరు మాట్లాడినది (You said):** {recognized_text}")

    # Chat history display
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            if "audio_bytes" in msg and msg["audio_bytes"]:
                st.audio(msg["audio_bytes"], format="audio/mp3")

    text_input = st.chat_input("లేదా ఇక్కడ టైప్ చేయండి (Or type question)...")
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

# 2. LEAF DOCTOR TAB
with tabs[1]:
    st.markdown("### 📷 తెగులు వచ్చిన ఆకు ఫోటో తీయండి (Leaf Disease Scanner)")
    input_mode = st.radio("ఎంచుకోండి (Select)", ["📷 కెమెరాతో ఫోటో తీయండి (Live Camera)", "📁 గ్యాలరీ నుండి అప్‌లోడ్ (Upload File)"], horizontal=True)
    img_to_analyze = None

    if input_mode == "📷 కెమెరాతో ఫోటో తీయండి (Live Camera)":
        cam_shot = st.camera_input("ఆకు ఫోటో తీయండి")
        if cam_shot:
            img_to_analyze = Image.open(cam_shot)
    else:
        uploaded_file = st.file_uploader("ఆకు ఫోటో అప్‌లోడ్ చేయండి", type=["jpg", "jpeg", "png", "webp", "heic"])
        if uploaded_file:
            img_to_analyze = Image.open(uploaded_file)

    if img_to_analyze:
        c_img, c_diag = st.columns([1, 2])
        with c_img:
            st.image(img_to_analyze, caption="స్కాన్ చేసిన ఆకు", use_container_width=True)
        with c_diag:
            if st.button("⚡ తెగులును గుర్తించు (Scan Leaf)", use_container_width=True):
                result = classifier.predict(img_to_analyze)
                st.session_state.latest_disease = result
                log_diagnostic(result["leaf_name"], result["disease"], result["confidence"], result["treatment"])

                st.success(f"🌱 **గుర్తించిన పంట (Crop):** {result['leaf_name']}")
                st.info(f"🔬 **వచ్చిన తెగులు (Disease):** {result['disease']} ({int(result['confidence']*100)}% Match)")
                st.write(f"🦠 **కారకం (Pathogen):** {result['pathogen']}")
                st.write(f"🔍 **లక్షణాలు (Symptoms):** {result['symptoms']}")
                st.warning(f"💊 **మందుల పిచికారీ (Prescription):** {result['treatment']}")

# 3. IRRIGATION & PUMP TAB
with tabs[2]:
    st.markdown("### 💧 నీటి పారుదల & మోటారు సమయం (Pump Runtime Calculator)")
    c_ir1, c_ir2 = st.columns(2)
    with c_ir1:
        irr_crop = st.selectbox("పంట (Crop)", ["Tomato", "Cotton", "Rice", "Maize", "Wheat"])
        acres_in = st.number_input("ఎకరాలు (Acres)", value=2.0, min_value=0.5, step=0.5)
    with c_ir2:
        pump_hp = st.number_input("మోటారు సామర్థ్యం / Pump HP", value=5.0, min_value=1.0, step=1.0)

    if st.button("💧 నీటి లెక్కలు చూపించు (Calculate)", use_container_width=True):
        irr_res = calculate_irrigation(irr_crop, acres_in, pump_hp, weather_info.get("temperature", 30.0))
        st.success(f"💧 **ఈరోజు కావలసిన నీరు:** {irr_res['liters_per_day']:,} లీటర్లు")
        st.info(f"⏱️ **మోటారు వేయవలసిన సమయం:** {irr_res['pump_runtime_hours']} గంటలు")
        st.write(irr_res['recommendation'])

# 4. SOIL & NPK TAB
with tabs[3]:
    st.markdown("### 🧪 ఎరువుల మోతాదు లెక్కించండి (Soil & NPK Calculator)")
    col1, col2 = st.columns(2)
    with col1:
        s_crop = st.selectbox("సాగు చేసే పంట", ["Tomato", "Cotton", "Rice", "Wheat", "Maize"])
        n_in = st.number_input("నత్రజని / Nitrogen (N) kg/ha", value=80.0)
        p_in = st.number_input("భాస్వరం / Phosphorus (P) kg/ha", value=30.0)
    with col2:
        k_in = st.number_input("పొటాష్ / Potassium (K) kg/ha", value=35.0)
        ph_in = st.number_input("నేల pH విలువ", value=6.5, min_value=1.0, max_value=14.0)

    if st.button("🧪 ఎరువుల సిఫార్సు (Get Dosage)", use_container_width=True):
        res = analyze_soil_npk(s_crop, n_in, p_in, k_in, ph_in)
        st.session_state.latest_soil = res
        for item in res["recommendations"]:
            st.info(item)

# 5. CROP CALENDAR TAB
with tabs[4]:
    st.markdown("### 📅 పంట పనుల కాలెండర్ (Crop Activity Schedule)")
    cal_crop = st.selectbox("పంట ఎంచుకోండి", ["Tomato", "Cotton", "Rice"])
    sow_d = st.date_input("విత్తిన తేదీ (Sowing Date)", value=date.today())
    schedule = get_crop_calendar(cal_crop, sow_d)
    for title, dt, desc in schedule:
        with st.expander(f"📍 {dt.strftime('%d %b %Y')} - {title}", expanded=True):
            st.write(desc)

# 6. REVENUE TAB
with tabs[5]:
    st.markdown("### 📈 దిగుబడి & ఆదాయం అంచనా (Yield & Profit Forecaster)")
    cy1, cy2 = st.columns(2)
    with cy1:
        f_crop = st.selectbox("పంట ఎంపిక", ["Tomato", "Cotton", "Rice", "Wheat", "Maize"])
        f_acres = st.number_input("సాగు విస్తీర్ణం (ఎకరాలు)", value=2.0, min_value=0.5)
    with cy2:
        f_price = st.number_input("అంచనా మార్కెట్ ధర (₹/క్వింటాల్)", value=2200.0, step=100.0)

    if st.button("📈 లాభం లెక్కించు (Calculate Profit)", use_container_width=True):
        f_res = forecast_yield_and_profit(f_crop, f_acres, f_price)
        st.metric("అంచనా దిగుబడి", f"{f_res['expected_yield_quintals']} క్వింటాళ్లు")
        c_m1, c_m2, c_m3 = st.columns(3)
        c_m1.metric("ఖర్చు (Investment)", f"₹{f_res['total_cost']:,}")
        c_m2.metric("మొత్తం అమ్మకం (Gross)", f"₹{f_res['gross_revenue']:,}")
        c_m3.metric("నికర లాభం (Net Profit)", f"₹{f_res['net_profit']:,}", delta=f"₹{f_res['net_profit']:,}")

# 7. SCHEMES TAB
with tabs[6]:
    st.markdown("### 🏛️ రైతు ప్రభుత్వ పథకాలు & సబ్సిడీలు (Government Schemes)")
    for sch in GOVERNMENT_SCHEMES:
        with st.container(border=True):
            st.markdown(f"### 🏷️ {sch['name']}")
            st.write(f"🎁 **లబ్ది (Benefit):** {sch['benefit']}")
            st.caption(f"👤 **అర్హత (Eligibility):** {sch['eligibility']}")

# 8. PEST RADAR TAB
with tabs[7]:
    st.markdown("### 🚨 పరిసర ప్రాంతాల తెగుళ్ల హెచ్చరికలు (Pest Radar)")
    for r in COMMUNITY_RADAR_ALERTS:
        with st.container(border=True):
            st.markdown(f"📍 **మండలం:** {r['mandal']} | తెగులు: `{r['threat']}` | పరిస్థితి: **{r['severity']}**")
            st.write(f"🛡️ **ముందుజాగ్రత్త:** {r['advisory']}")

# 9. RBK & CHC LOCATOR TAB
with tabs[8]:
    st.markdown("### 🏢 రైతు భరోసా కేంద్రాలు & యంత్రాల అద్దె (Agri Hubs & Rentals)")
    for ch in NEARBY_SERVICE_CENTERS:
        with st.container(border=True):
            st.markdown(f"🏢 **{ch['name']}** ({ch['type']})")
            st.write(f"📍 దూరం: **{ch['distance']}** | 📞 ఫోన్: `{ch['contact']}`")
            st.caption(f"సేవలు: {ch['services']}")

# 10. PDF & HISTORY TAB
with tabs[9]:
    st.markdown("### 📜 డిజిటల్ ప్రిస్క్రిప్షన్ కార్డ్ (Health Card PDF)")
    col_pdf1, col_pdf2 = st.columns([1, 2])
    with col_pdf1:
        farmer_n = st.text_input("రైతు పేరు (Farmer Name)", value="Kammari Charan Kumar")
        if st.button("📄 హెల్త్ కార్డ్ డౌన్‌లోడ్ (PDF)", use_container_width=True):
            pdf_fp = generate_pdf_health_card(
                farmer_name=farmer_n,
                location=weather_info.get("location", village_input),
                disease_data=st.session_state.latest_disease,
                soil_data=st.session_state.latest_soil,
                weather_data=weather_info
            )
            st.download_button(
                label="⬇️ PDF సేవ్ చేసుకోండి (Download)",
                data=pdf_fp,
                file_name="Kisan_Mitra_Farm_Health_Card.pdf",
                mime="application/pdf",
                use_container_width=True
            )

    with col_pdf2:
        st.markdown("### 🗄️ గత పరీక్షల వివరాలు (Past Scans)")
        history = get_recent_history(5)
        if history:
            for row in history:
                st.write(f"• **{row[0]}** | ఆకు: `{row[1]}` | తెగులు: **{row[2]}** ({int(row[3]*100)}%)")
        else:
            st.info("ఇంకా ఎలాంటి పరీక్షలు నమోదు కాలేదు.")
"""

Path("app.py").write_text(code, encoding="utf-8")
print("✅ Farmer Icon UI successfully installed into app.py!")
from pathlib import Path

app_code = """import streamlit as st
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

st.set_page_config(page_title="Kisan Mitra - AI Farmer Operating System", page_icon="🌾", layout="wide")
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

st.title("🌾 Kisan Mitra: AI Agricultural Operating System")
st.caption("Voice-to-Voice Agronomy • Instant Leaf Vision • Smart Irrigation • Crop Calendar • Farm Ledger")

# --- SIDEBAR ---
with st.sidebar:
    st.header("⚙️ Village and Language")
    lang_code = st.selectbox(
        "Preferred Language",
        options=list(settings.SUPPORTED_LANGUAGES.keys()),
        format_func=lambda x: settings.SUPPORTED_LANGUAGES[x],
        index=0
    )
    lang_name = settings.SUPPORTED_LANGUAGES[lang_code]

    st.divider()
    st.subheader("🌦️ Live Village Weather")
    village_input = st.text_input("Village / Mandal", value="Kurabala Kota")
    weather_info = get_cached_weather(village_input)

    if weather_info.get("status") == "success":
        st.success(f"📍 **{weather_info['location']}**")
        c1, c2 = st.columns(2)
        c1.metric("Temp", f"{weather_info['temperature']} °C")
        c2.metric("Humidity", f"{weather_info['humidity']}%")
        st.info(f"Sky: **{weather_info['condition']}** | Wind: {weather_info['wind_speed']} km/h")
        if weather_info.get("rain_risk"):
            st.warning("⚠️ **Rain Alert:** Delay pesticide/fertilizer spraying.")

    st.divider()
    st.subheader("💰 Live Mandi Price")
    crop_mandi = st.selectbox("Commodity", ["Cotton", "Rice", "Tomato", "Wheat", "Maize"])
    rates = get_mandi_rates(crop_mandi)
    for r in rates:
        st.write(f"📍 **{r['market']}**: ₹{r['modal_price']}/Q")

# --- 10 FEATURE TABS ---
tabs = st.tabs([
    "🎙️ Voice Advisory",
    "🍃 Universal Leaf Vision",
    "🧪 Soil and NPK",
    "📅 Crop Calendar",
    "💧 Irrigation and Pump",
    "📈 Yield and Revenue",
    "🏛️ Schemes and Subsidies",
    "🚨 Pest Alert Radar",
    "📍 Agri Hubs and CHC",
    "📜 Farm Ledger and PDF"
])

# Tab 1: Voice Chat
with tabs[0]:
    st.subheader("🗣️ Voice-to-Voice Farmer Advisory")
    audio_val = st.audio_input("Tap to speak your question in your regional language")
    user_query = None

    if audio_val is not None:
        audio_bytes = audio_val.read()
        with st.spinner("🎙️ Recognizing speech..."):
            recognized_text = transcribe_audio_bytes(audio_bytes, lang_code=lang_code)
            if recognized_text:
                user_query = recognized_text
                st.success(f"🗣️ **Understood:** {recognized_text}")

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            if "audio_bytes" in msg and msg["audio_bytes"]:
                st.audio(msg["audio_bytes"], format="audio/mp3")

    text_input = st.chat_input("Or type your farming question...")
    if text_input:
        user_query = text_input

    if user_query:
        append_message("user", user_query)
        with st.chat_message("user"):
            st.markdown(user_query)

        with st.chat_message("assistant"):
            with st.spinner("🌾 Generating advice..."):
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

# Tab 2: Universal Leaf Vision Scanner
with tabs[1]:
    st.subheader("🍃 Universal Crop Leaf & Disease Scanner")
    input_mode = st.radio("Input Method", ["📁 Upload Image", "📷 Camera Capture"], horizontal=True)
    img_to_analyze = None

    if input_mode == "📁 Upload Image":
        uploaded_file = st.file_uploader(
            "Upload crop image",
            type=["jpg", "jpeg", "png", "webp", "bmp", "tiff", "heic"]
        )
        if uploaded_file:
            img_to_analyze = Image.open(uploaded_file)
    else:
        cam_shot = st.camera_input("Snap a photo of the affected plant leaf")
        if cam_shot:
            img_to_analyze = Image.open(cam_shot)

    if img_to_analyze:
        c_img, c_diag = st.columns([1, 2])
        with c_img:
            st.image(img_to_analyze, caption="Processed Image", use_container_width=True)
        with c_diag:
            if st.button("⚡ Fast Scan & Diagnose Leaf", use_container_width=True):
                result = classifier.predict(img_to_analyze)
                st.session_state.latest_disease = result
                log_diagnostic(result["leaf_name"], result["disease"], result["confidence"], result["treatment"])

                st.success(f"🌱 **Identified Plant:** {result['leaf_name']}")
                st.info(f"🔬 **Diagnosis:** {result['disease']} ({int(result['confidence']*100)}% match)")
                st.write(f"🦠 **Pathogen Category:** {result['pathogen']}")
                st.write(f"🔍 **Symptoms:** {result['symptoms']}")
                st.warning(f"💊 **Prescription:** {result['treatment']}")

# Tab 3: Soil & NPK
with tabs[2]:
    st.subheader("🧪 Soil Health & NPK Recommendation")
    col1, col2 = st.columns(2)
    with col1:
        s_crop = st.selectbox("Crop", ["Tomato", "Cotton", "Rice", "Wheat", "Maize"])
        n_in = st.number_input("Nitrogen (N) kg/ha", value=80.0)
        p_in = st.number_input("Phosphorus (P) kg/ha", value=30.0)
    with col2:
        k_in = st.number_input("Potassium (K) kg/ha", value=35.0)
        ph_in = st.number_input("Soil pH", value=6.5, min_value=1.0, max_value=14.0)

    if st.button("Calculate Fertilizer Dose"):
        res = analyze_soil_npk(s_crop, n_in, p_in, k_in, ph_in)
        st.session_state.latest_soil = res
        for item in res["recommendations"]:
            st.info(item)

# Tab 4: Crop Calendar
with tabs[3]:
    st.subheader("📅 Stage-by-Stage Crop Activity Timeline")
    cal_crop = st.selectbox("Select Sown Crop", ["Tomato", "Cotton", "Rice"])
    sow_d = st.date_input("Sowing Date", value=date.today())
    schedule = get_crop_calendar(cal_crop, sow_d)
    for title, dt, desc in schedule:
        with st.expander(f"📍 {dt.strftime('%d %b %Y')} - {title}", expanded=True):
            st.write(desc)

# Tab 5: Irrigation & Pump
with tabs[4]:
    st.subheader("💧 Smart Irrigation & Pump Runtime Calculator")
    c_ir1, c_ir2 = st.columns(2)
    with c_ir1:
        irr_crop = st.selectbox("Crop for Irrigation", ["Tomato", "Cotton", "Rice", "Maize", "Wheat"])
        acres_in = st.number_input("Field Area (Acres)", value=2.0, min_value=0.5, step=0.5)
    with c_ir2:
        pump_hp = st.number_input("Borewell / Drip Pump (HP)", value=5.0, min_value=1.0, step=1.0)
    
    if st.button("Calculate Water Requirement"):
        irr_res = calculate_irrigation(irr_crop, acres_in, pump_hp, weather_info.get("temperature", 30.0))
        st.success(f"💧 **Total Water Needed Today:** {irr_res['liters_per_day']:,} Liters")
        st.info(f"⏱️ **Recommended Pump Runtime:** {irr_res['pump_runtime_hours']} Hours")
        st.write(irr_res['recommendation'])

# Tab 6: Yield & Revenue
with tabs[5]:
    st.subheader("📈 Harvest Yield & Revenue Forecaster")
    cy1, cy2 = st.columns(2)
    with cy1:
        f_crop = st.selectbox("Crop Forecast", ["Tomato", "Cotton", "Rice", "Wheat", "Maize"])
        f_acres = st.number_input("Harvest Area (Acres)", value=2.0, min_value=0.5)
    with cy2:
        f_price = st.number_input("Expected Mandi Rate (₹/Quintal)", value=2200.0, step=100.0)

    if st.button("Forecast Farm Economics"):
        f_res = forecast_yield_and_profit(f_crop, f_acres, f_price)
        st.metric("Expected Harvest Yield", f"{f_res['expected_yield_quintals']} Quintals")
        c_m1, c_m2, c_m3 = st.columns(3)
        c_m1.metric("Est. Total Input Cost", f"₹{f_res['total_cost']:,}")
        c_m2.metric("Gross Mandi Sales", f"₹{f_res['gross_revenue']:,}")
        c_m3.metric("Estimated Net Profit", f"₹{f_res['net_profit']:,}", delta=f"₹{f_res['net_profit']:,}")

# Tab 7: Schemes & Subsidies
with tabs[6]:
    st.subheader("🏛️ Active Government Agricultural Schemes & Grants")
    for sch in GOVERNMENT_SCHEMES:
        with st.container(border=True):
            st.markdown(f"### {sch['name']}")
            st.write(f"🎁 **Financial Benefit:** {sch['benefit']}")
            st.caption(f"👤 **Eligibility:** {sch['eligibility']}")

# Tab 8: Pest Radar
with tabs[7]:
    st.subheader("🚨 Regional Pest & Disease Outbreak Radar")
    for r in COMMUNITY_RADAR_ALERTS:
        with st.container(border=True):
            st.markdown(f"**Mandal: {r['mandal']}** | Threat: `{r['threat']}` | Status: **{r['severity']}**")
            st.write(f"🛡️ **Precaution:** {r['advisory']}")

# Tab 9: Agri Hubs & CHC
with tabs[8]:
    st.subheader("📍 Nearby Rythu Bharosa Kendras & Rental Centers")
    for ch in NEARBY_SERVICE_CENTERS:
        with st.container(border=True):
            st.markdown(f"🏢 **{ch['name']}** ({ch['type']})")
            st.write(f"📍 Distance: **{ch['distance']}** | 📞 Contact: `{ch['contact']}`")
            st.caption(f"Services: {ch['services']}")

# Tab 10: Farm Ledger & PDF
with tabs[9]:
    st.subheader("📜 Farm Diagnostic Ledger & Download Prescription PDF")
    col_pdf1, col_pdf2 = st.columns([1, 2])
    with col_pdf1:
        farmer_n = st.text_input("Farmer Full Name", value="Kammari Charan Kumar")
        if st.button("📄 Generate Digital Health Card (PDF)"):
            pdf_fp = generate_pdf_health_card(
                farmer_name=farmer_n,
                location=weather_info.get("location", village_input),
                disease_data=st.session_state.latest_disease,
                soil_data=st.session_state.latest_soil,
                weather_data=weather_info
            )
            st.download_button(
                label="⬇️ Download Health Card PDF",
                data=pdf_fp,
                file_name="Kisan_Mitra_Farm_Health_Card.pdf",
                mime="application/pdf"
            )
    
    with col_pdf2:
        st.markdown("### 🗄️ Past Diagnostic Scans on this Farm")
        history = get_recent_history(5)
        if history:
            for row in history:
                st.write(f"• **{row[0]}** | Leaf: `{row[1]}` | Diagnosis: **{row[2]}** ({int(row[3]*100)}%)")
        else:
            st.info("No prior diagnostic scans recorded yet.")
"""

Path("app.py").write_text(app_code, encoding="utf-8")
print("✅ app.py written with complete UTF-8 encoding successfully!")
from pathlib import Path

full_app_code = '''import streamlit as st
from PIL import Image
from datetime import date
from dotenv import load_dotenv

load_dotenv()

from config.settings import settings
from src.tools.i18n import get_text
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

st.set_page_config(page_title="Kisan Mitra - AI Agricultural Operating System", page_icon="🌾", layout="wide")
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

# --- SIDEBAR: 3-WAY LANGUAGE SELECTOR BUTTONS ---
with st.sidebar:
    st.markdown("### 🌐 భాష / भाषा / Language")
    selected_language = st.radio(
        "Language Selection",
        ["తెలుగు (Telugu)", "हिन्दी (Hindi)", "English (English)"],
        index=0,
        label_visibility="collapsed"
    )
    
    if "తెలుగు" in selected_language:
        lang_key = "te"
        lang_full = "Telugu"
    elif "हिन्दी" in selected_language:
        lang_key = "hi"
        lang_full = "Hindi"
    else:
        lang_key = "en"
        lang_full = "English"

    t = get_text(lang_key)

    st.divider()
    st.markdown(f"### 📍 {t['location']}")
    farmer_location = st.text_input("Village / Mandal", value=default_location_name, label_visibility="collapsed")
    
    st.markdown(f"### 👤 {t['farmer_profile']}")
    test_member = st.selectbox(
        "Account",
        ["Kammari Charan Kumar (2.5 Acres)", "Ramesh Reddy (5.0 Acres)", "Siva Naidu (1.5 Acres)"],
        label_visibility="collapsed"
    )
    farmer_name_clean = test_member.split(" (")[0]
    farmer_acres = 2.5 if "2.5" in test_member else (5.0 if "5.0" in test_member else 1.5)

    st.divider()
    st.markdown(f"### 🌦️ {t['weather']}")
    weather_info = get_cached_weather(farmer_location)
    if weather_info.get("status") == "success":
        st.success(f"📍 {weather_info['location']}")
        c1, c2 = st.columns(2)
        c1.metric(f"🌡️ {t['temp']}", f"{weather_info['temperature']} °C")
        c2.metric(f"💧 {t['humidity']}", f"{weather_info['humidity']}%")
        st.info(f"⛅ {weather_info['condition']} | 💨 {weather_info['wind_speed']} km/h")
        if weather_info.get("rain_risk"):
            st.warning(f"⚠️ {t['rain_alert']}")

# Top Header in Selected Pure Language
st.markdown(f"""
<div style="background: linear-gradient(135deg, #1b5e20, #2e7d32); color: white; padding: 20px; border-radius: 16px; text-align: center; margin-bottom: 15px;">
    <h1 style="color:white; margin:0;">🌾 {t['app_title']}</h1>
    <p style="color:#e8f5e9; margin:4px 0 0 0; font-size:1.15rem;">
        🟢 <b>{t['app_sub']}</b>
    </p>
</div>
""", unsafe_allow_html=True)

# 12 Navigation Tabs in Selected Pure Language
tab_labels = [
    t["tabs"]["community"],
    t["tabs"]["crops"],
    t["tabs"]["mandi"],
    t["tabs"]["voice"],
    t["tabs"]["leaf"],
    t["tabs"]["radar"],
    t["tabs"]["water"],
    t["tabs"]["soil"],
    t["tabs"]["calendar"],
    t["tabs"]["profit"],
    t["tabs"]["schemes"],
    t["tabs"]["pdf"]
]
tabs = st.tabs(tab_labels)

# 1. COMMUNITY
with tabs[0]:
    st.subheader(f"{t['community_title']} ({farmer_location})")
    st.caption(t["community_sub"])

    comm_data = get_regional_communities(farmer_location)
    c_b1, c_b2 = st.columns([2, 1])
    with c_b1:
        st.info(f"📍 Cluster: **{comm_data['mandal']} / {comm_data['district']}**")
    with c_b2:
        st.link_button(t["share_whatsapp"], comm_data["share_url"], use_container_width=True)

    st.markdown(f"### {t['wa_heading']}")
    cols_w = st.columns(3)
    for idx, grp in enumerate(comm_data["whatsapp_groups"]):
        with cols_w[idx % 3]:
            with st.container(border=True):
                st.markdown(f"#### {grp['name']}")
                st.caption(f"📂 {grp['category']}")
                st.write(f"👥 {grp['members']}")
                st.write(grp["description"])
                st.link_button("Join WhatsApp Group", grp["link"], use_container_width=True)

    st.markdown(f"### {t['tg_heading']}")
    cols_t = st.columns(2)
    for idx, ch in enumerate(comm_data["telegram_channels"]):
        with cols_t[idx % 2]:
            with st.container(border=True):
                st.markdown(f"#### {ch['name']}")
                st.caption(f"📂 {ch['category']}")
                st.write(f"👥 {ch['members']}")
                st.write(ch["description"])
                st.link_button("Join Telegram Channel", ch["link"], use_container_width=True)

# 2. CROPS
with tabs[1]:
    st.subheader(f"{t['crops_title']} ({farmer_location})")
    st.caption(t["crops_sub"])
    crop_intel = get_location_crop_suitability(farmer_location)

    col_m1, col_m2, col_m3 = st.columns(3)
    col_m1.info(f"🏛️ Zone: **{crop_intel['zone_name']}**")
    col_m2.info(f"🟤 Soil: **{crop_intel['soil_profile']}**")
    col_m3.info(f"🌧️ Climate: **{crop_intel['climate_profile']}**")

    for c in crop_intel["all_crops"]:
        with st.container(border=True):
            head_col, score_col = st.columns([3, 1])
            head_col.markdown(f"### {c['crop']}")
            head_col.caption(f"Category: **{c.get('category', 'Cash Crop')}** | Season: **{c.get('season', 'Kharif / Rabi')}**")
            score_col.metric("Suitability", f"{c.get('suitability', 90)}%")

            d_col1, d_col2 = st.columns(2)
            with d_col1:
                st.write(f"🧬 **Varieties:** `{c.get('varieties', 'High-Yielding Hybrid')}`")
                st.write(f"💧 **Water Need:** {c.get('water_need', 'Medium')}")
            with d_col2:
                st.write(f"🔬 **Agro Match:** {c.get('why_suitable', 'Optimal soil and drainage.')}")
                st.write(f"🚛 **Market Access:** **{c.get('market_link', 'APMC Mandi')}**")

# 3. MANDI
with tabs[2]:
    st.subheader(f"{t['mandi_title']} ({farmer_location})")
    live_prices = get_live_dynamic_mandi_rates(farmer_location)

    cols = st.columns(3)
    for idx, p in enumerate(live_prices):
        with cols[idx % 3]:
            with st.container(border=True):
                st.markdown(f"### {p['crop']}")
                st.caption(f"Market: **{p['primary_market']}**")
                st.metric(
                    label=f"Modal Rate: ₹{p['modal_price']:,} / Q",
                    value=f"₹{p['modal_price']:,}",
                    delta=p["trend"]
                )
                st.write(f"Range: ₹{p['min_price']:,} - ₹{p['max_price']:,}")
                st.write(f"Arrivals: **{p['arrivals_tonnes']} Tonnes**")
                st.caption(f"Status: {p['updated']}")

# 4. VOICE
with tabs[3]:
    st.subheader(t["voice_title"])
    audio_val = st.audio_input("RECORD VOICE HERE")
    user_query = None

    if audio_val is not None:
        audio_bytes = audio_val.read()
        with st.spinner(t["voice_listen"]):
            recognized_text = transcribe_audio_bytes(audio_bytes, lang_code=lang_key)
            if recognized_text:
                user_query = recognized_text
                st.success(f"🗣️ {t['voice_spoken']}: {recognized_text}")

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            if "audio_bytes" in msg and msg["audio_bytes"]:
                st.audio(msg["audio_bytes"], format="audio/mp3")

    text_input = st.chat_input("Ask farming question...")
    if text_input:
        user_query = text_input

    if user_query:
        append_message("user", user_query)
        with st.chat_message("user"):
            st.markdown(user_query)

        with st.chat_message("assistant"):
            with st.spinner("🌾 Consulting AI..."):
                advice = orchestrator.generate_advisory(
                    query=user_query,
                    language=lang_full,
                    weather_info=weather_info if weather_info.get("status") == "success" else None,
                    disease_data=st.session_state.latest_disease,
                    soil_data=st.session_state.latest_soil
                )
                st.markdown(advice)
                try:
                    audio_fp = generate_voice_audio(advice, lang=lang_key)
                    audio_data = audio_fp.getvalue()
                    st.audio(audio_data, format="audio/mp3", autoplay=True)
                    st.session_state.messages.append({"role": "assistant", "content": advice, "audio_bytes": audio_data})
                except Exception:
                    append_message("assistant", advice)

# 5. LEAF DOCTOR
with tabs[4]:
    st.subheader(t["leaf_title"])
    input_mode = st.radio("Input Mode", ["Camera Capture", "Upload File"], horizontal=True)
    img_to_analyze = None

    if input_mode == "Camera Capture":
        cam_shot = st.camera_input("Snap a photo of the affected plant leaf")
        if cam_shot:
            img_to_analyze = Image.open(cam_shot)
    else:
        uploaded_file = st.file_uploader("Upload leaf picture", type=["jpg", "jpeg", "png", "webp", "heic"])
        if uploaded_file:
            img_to_analyze = Image.open(uploaded_file)

    if img_to_analyze:
        c_img, c_diag = st.columns([1, 2])
        with c_img:
            st.image(img_to_analyze, caption="Processed Image", use_container_width=True)
        with c_diag:
            if st.button(t["scan_btn"], use_container_width=True):
                result = classifier.predict(img_to_analyze)
                st.session_state.latest_disease = result
                log_diagnostic(farmer_name_clean, farmer_location, result["leaf_name"], result["disease"], result["confidence"], result["treatment"])

                st.success(f"🌱 Plant: {result['leaf_name']}")
                st.info(f"🔬 Diagnosis: {result['disease']} ({int(result['confidence']*100)}% Match)")
                st.write(f"🦠 Pathogen: {result['pathogen']}")
                st.write(f"🔍 Symptoms: {result['symptoms']}")
                st.warning(f"💊 Prescription: {result['treatment']}")

# 6. RADAR
with tabs[5]:
    st.subheader(f"{t['radar_title']} ({farmer_location})")
    outbreaks = get_dynamic_community_outbreaks(farmer_location)
    if outbreaks:
        for ob in outbreaks:
            with st.container(border=True):
                st.markdown(f"### 📍 Mandal: {ob['mandal']} | Crop: **{ob['crop']}**")
                st.markdown(f"⚠️ Threat: **{ob['threat']}** (Reported cases: `{ob['reported_cases']}` farmers)")
                st.info(f"Severity: **{ob['severity']}**")
                st.write(f"🛡️ Advisory: {ob['advisory']}")

# 7. IRRIGATION
with tabs[6]:
    st.subheader(t["irrigation_title"])
    c_ir1, c_ir2 = st.columns(2)
    with c_ir1:
        irr_crop = st.selectbox("Crop", ["Tomato", "Groundnut", "Chilli", "Cotton", "Maize", "Rice"])
        acres_in = st.number_input("Area (Acres)", value=farmer_acres, min_value=0.5, step=0.5)
    with c_ir2:
        pump_hp = st.number_input("Pump Power (HP)", value=5.0, min_value=1.0, step=1.0)

    if st.button(t["irrigation_btn"], use_container_width=True):
        irr_res = calculate_irrigation(irr_crop, acres_in, pump_hp, weather_info.get("temperature", 30.0))
        st.success(f"💧 Water Needed Today: {irr_res['liters_per_day']:,} Liters")
        st.info(f"⏱️ Pump Runtime: {irr_res['pump_runtime_hours']} Hours")
        st.write(irr_res['recommendation'])

# 8. SOIL NPK
with tabs[7]:
    st.subheader(t["soil_title"])
    col1, col2 = st.columns(2)
    with col1:
        s_crop = st.selectbox("Crop for Dose", ["Tomato", "Groundnut", "Chilli", "Cotton", "Maize"])
        n_in = st.number_input("Nitrogen (N) kg/ha", value=80.0)
        p_in = st.number_input("Phosphorus (P) kg/ha", value=30.0)
    with col2:
        k_in = st.number_input("Potassium (K) kg/ha", value=35.0)
        ph_in = st.number_input("Soil pH", value=6.5, min_value=1.0, max_value=14.0)

    if st.button(t["soil_btn"]):
        res = analyze_soil_npk(s_crop, n_in, p_in, k_in, ph_in)
        st.session_state.latest_soil = res
        for item in res["recommendations"]:
            st.info(item)

# 9. CALENDAR
with tabs[8]:
    st.subheader(t["calendar_title"])
    cal_crop = st.selectbox("Sown Crop", ["Tomato", "Cotton", "Rice"])
    sow_d = st.date_input("Sowing Date", value=date.today())
    schedule = get_crop_calendar(cal_crop, sow_d)
    for title, dt, desc in schedule:
        with st.expander(f"📍 {dt.strftime('%d %b %Y')} - {title}", expanded=True):
            st.write(desc)

# 10. PROFIT
with tabs[9]:
    st.subheader(t["profit_title"])
    cy1, cy2 = st.columns(2)
    with cy1:
        f_crop = st.selectbox("Forecast Crop", ["Tomato", "Cotton", "Rice", "Wheat", "Maize"])
        f_acres = st.number_input("Area (Acres)", value=farmer_acres, min_value=0.5)
    with cy2:
        f_price = st.number_input("Expected Rate (₹/Quintal)", value=2200.0, step=100.0)

    if st.button(t["profit_btn"]):
        f_res = forecast_yield_and_profit(f_crop, f_acres, f_price)
        st.metric("Expected Yield", f"{f_res['expected_yield_quintals']} Quintals")
        c_m1, c_m2, c_m3 = st.columns(3)
        c_m1.metric("Input Cost", f"₹{f_res['total_cost']:,}")
        c_m2.metric("Gross Sales", f"₹{f_res['gross_revenue']:,}")
        c_m3.metric("Net Profit", f"₹{f_res['net_profit']:,}", delta=f"₹{f_res['net_profit']:,}")

# 11. SCHEMES
with tabs[10]:
    st.subheader(f"{t['schemes_title']} ({farmer_name_clean})")
    matched_schemes = get_dynamic_schemes(farmer_acres)
    for sch in matched_schemes:
        with st.container(border=True):
            st.markdown(f"### 🏷️ {sch['name']}")
            st.write(f"🎁 Benefit: {sch['benefit']}")
            st.caption(f"👤 Eligibility: {sch['eligibility']}")

# 12. PDF
with tabs[11]:
    st.subheader(t["pdf_title"])
    col_pdf1, col_pdf2 = st.columns([1, 2])
    with col_pdf1:
        farmer_n = st.text_input("Farmer Name", value=farmer_name_clean)
        if st.button(t["download_pdf"], use_container_width=True):
            pdf_fp = generate_pdf_health_card(
                farmer_name=farmer_n,
                location=weather_info.get("location", farmer_location),
                disease_data=st.session_state.latest_disease,
                soil_data=st.session_state.latest_soil,
                weather_data=weather_info
            )
            st.download_button(
                label="⬇️ Download PDF Card",
                data=pdf_fp,
                file_name="Kisan_Mitra_Farm_Health_Card.pdf",
                mime="application/pdf",
                use_container_width=True
            )

    with col_pdf2:
        st.markdown("### 🗄️ Past Records")
        history = get_recent_history(10)
        if history:
            for row in history:
                st.write(f"• **{row[0]}** | Farmer: `{row[1]}` ({row[2]}) | Leaf: **{row[3]}** | Result: *{row[4]}* ({int(row[5]*100)}%)")
        else:
            st.info("No scans recorded yet.")
'''

Path("app.py").write_text(full_app_code, encoding="utf-8")
print("✅ Fully translated multilingual app.py (Telugu, Hindi, English) generated successfully!")
'''

Path("update_app_all_lang.py").write_text(full_app_code, encoding="utf-8")
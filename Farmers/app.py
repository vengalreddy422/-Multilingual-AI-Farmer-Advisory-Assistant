# Kisan Mitra Enterprise Agricultural Operating System v2.7
import re
import uuid
import importlib
import streamlit as st
from PIL import Image
from datetime import date
from dotenv import load_dotenv

load_dotenv()

from config.settings import settings
from src.tools.i18n import get_text
from src.database.session_state import init_session

import src.database.db_ledger as db_ledger
importlib.reload(db_ledger)
from src.database.db_ledger import (
    register_user, authenticate_user, save_chat_message, 
    get_user_chat_sessions, load_session_messages, delete_user_session,
    log_diagnostic, get_latest_diagnostic_record
)

import src.tools.email_dispatcher as email_dispatcher_module
importlib.reload(email_dispatcher_module)
from src.tools.email_dispatcher import send_health_card_email, send_welcome_onboarding_email

import src.tools.pdf_generator as pdf_generator_module
importlib.reload(pdf_generator_module)
from src.tools.pdf_generator import generate_pdf_health_card

from src.intelligence.gemini_advisor import GeminiAgriAdvisor
from src.intelligence.guardrails import guardrail_engine
from src.tools.weather import fetch_weather, geocode_location_strict, reverse_geocode_coords
from src.tools.soil_advisor import analyze_soil_npk
from src.tools.dynamic_engine import (
    auto_detect_farmer_location,
    get_location_crop_suitability,
    get_live_dynamic_mandi_rates
)
from src.tools.community_links import get_regional_communities
from src.tools.pest_radar import generate_regional_radar_clusters
from src.tools.offline_sms import process_offline_sms_query, SMS_KEYWORDS
from src.tools.pdf_generator import generate_pdf_health_card
from src.tools.agri_modules import (
    get_crop_calendar, calculate_irrigation, 
    get_regional_crop_cost_benchmarks, forecast_yield_and_profit_advanced,
    get_dynamic_schemes
)
from src.tools.natural_pesticides import (
    NATURAL_FORMULATIONS,
    calculate_scaled_formulation,
    get_recommendations_by_problem
)
from src.vision.disease_classifier import PlantDiseaseClassifier
from src.audio.speech_to_text import transcribe_audio_bytes
from src.audio.text_to_speech import generate_voice_audio

st.set_page_config(
    page_title="Kisan Mitra - AI Agricultural System", 
    page_icon="🌾", 
    layout="wide",
    initial_sidebar_state="expanded"
)
init_session()

# --- HIGH-SPEED IN-MEMORY CACHING PIPELINE ---
@st.cache_resource(show_spinner=False)
def load_vision_classifier():
    return PlantDiseaseClassifier()

@st.cache_resource(show_spinner=False)
def load_gemini_advisor():
    return GeminiAgriAdvisor()

@st.cache_data(ttl=900, show_spinner=False)
def get_cached_weather(city_str, lat=None, lon=None):
    return fetch_weather(city_str, lat=lat, lon=lon)

@st.cache_data(ttl=3600, show_spinner=False)
def get_cached_reverse_geo(lat: float, lon: float):
    return reverse_geocode_coords(lat, lon)

@st.cache_data(ttl=900, show_spinner=False)
def get_cached_crop_intel(location, lat, lon):
    return get_location_crop_suitability(location, lat=lat, lon=lon)

@st.cache_data(ttl=900, show_spinner=False)
def get_cached_mandi(location, lat, lon):
    return get_live_dynamic_mandi_rates(location, lat=lat, lon=lon)

@st.cache_data(ttl=3600, show_spinner=False)
def get_cached_schemes(acres, location):
    return get_dynamic_schemes(acres, state=location)

@st.cache_data(ttl=3600, show_spinner=False)
def get_cached_community(location):
    return get_regional_communities(location)

@st.cache_data(ttl=1800, show_spinner=False)
def get_cached_pest_radar(lat: float, lon: float, location: str):
    return generate_regional_radar_clusters(lat, lon, location)

classifier = load_vision_classifier()
gemini_advisor = load_gemini_advisor()

# State Initializations
if "user" not in st.session_state:
    st.session_state.user = None
if "auth_page" not in st.session_state:
    st.session_state.auth_page = None
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())
if "lang_key" not in st.session_state:
    st.session_state.lang_key = "te"  # Default regional
if "messages" not in st.session_state:
    st.session_state.messages = []
if "latest_disease" not in st.session_state:
    st.session_state.latest_disease = None
if "latest_soil" not in st.session_state:
    st.session_state.latest_soil = None

# Geolocation Initial State
query_params = st.query_params
if query_params.get("lat") and query_params.get("lon"):
    st.session_state.current_lat = float(query_params.get("lat"))
    st.session_state.current_lon = float(query_params.get("lon"))
    st.session_state.active_location_name = get_cached_reverse_geo(st.session_state.current_lat, st.session_state.current_lon)
elif "current_lat" not in st.session_state:
    st.session_state.current_lat = 13.5560
    st.session_state.current_lon = 78.5010
    st.session_state.active_location_name = "Madanapalle, Andhra Pradesh"

LANG_OPTIONS = {
    "తెలుగు (Telugu)": "te",
    "हिन्दी (Hindi)": "hi",
    "English (English)": "en",
    "தமிழ் (Tamil)": "ta",
    "ಕನ್ನಡ (Kannada)": "kn",
    "मराठी (Marathi)": "mr"
}
LANG_KEYS_LIST = list(LANG_OPTIONS.values())
LANG_LABELS_LIST = list(LANG_OPTIONS.keys())

current_lang_idx = LANG_KEYS_LIST.index(st.session_state.lang_key) if st.session_state.lang_key in LANG_KEYS_LIST else 0
t = get_text(st.session_state.lang_key)
auth_t = t.get("auth", {})

# --- INPUT VALIDATION HELPERS ---
def validate_identifier_input(ident_str: str) -> bool:
    clean = str(ident_str).strip()
    if not clean or len(clean) < 3:
        return False
    # If numeric or telephone format:
    phone_clean = re.sub(r'[\s\-\(\)\+]', '', clean)
    if phone_clean.isdigit():
        if phone_clean.startswith("91") and len(phone_clean) == 12:
            phone_clean = phone_clean[2:]
        elif phone_clean.startswith("0") and len(phone_clean) == 11:
            phone_clean = phone_clean[1:]
        return bool(re.match(r'^[6-9]\d{9}$', phone_clean))
    
    # If alphanumeric username (e.g. yaswanth7462, ramesh_kumar)
    return bool(re.match(r'^[a-zA-Z0-9_.-]{3,30}$', clean))

def validate_email_input(email_str: str) -> bool:
    if not email_str or not email_str.strip():
        return True
    return bool(re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email_str.strip()))

# =========================================================
# 🌟 FULL-PAGE AUTHENTICATION SCREEN (MOBILE / EMAIL / USER)
# =========================================================
if st.session_state.auth_page in ["login", "register"]:
    col_l, col_center, col_r = st.columns([1.2, 2.6, 1.2])
    with col_center:
        st.markdown("<br>", unsafe_allow_html=True)
        top_c1, top_c2, top_c3 = st.columns([3, 2, 1.5], vertical_alignment="center")
        with top_c1:
            st.markdown("## 🌾 **Kisan Mitra**")
        with top_c2:
            auth_lang = st.selectbox(
                "Auth Lang",
                LANG_LABELS_LIST,
                index=current_lang_idx,
                key="auth_lang_select",
                label_visibility="collapsed"
            )
            st.session_state.lang_key = LANG_OPTIONS[auth_lang]
            t = get_text(st.session_state.lang_key)
            auth_t = t.get("auth", {})

        with top_c3:
            if st.button(auth_t.get("back_guest", "Back to App"), use_container_width=True):
                st.session_state.auth_page = None
                st.rerun()

        st.markdown("""
        <style>
            .auth-card {
                background: linear-gradient(135deg, #1b5e20, #2e7d32);
                color: white;
                padding: 22px;
                border-radius: 16px;
                margin-bottom: 18px;
                text-align: center;
                box-shadow: 0 4px 15px rgba(0,0,0,0.18);
            }
        </style>
        """, unsafe_allow_html=True)

        if st.session_state.auth_page == "login":
            st.markdown(f"""
            <div class="auth-card">
                <h2 style="color:white; margin:0;">{auth_t.get('login_title', 'Farmer Login')}</h2>
                <p style="color:#e8f5e9; margin:6px 0 0 0;">{auth_t.get('login_sub', 'Access your past agronomy records via Mobile or Email')}</p>
            </div>
            """, unsafe_allow_html=True)

            with st.form("full_login_form"):
                u_name = st.text_input(f"👤 {auth_t.get('username', 'Username / Mobile / Email')}", placeholder="e.g., yaswanth7462 or 9849012345")
                u_pass = st.text_input(f"🔑 {auth_t.get('password', 'Password')}", type="password", placeholder="Enter Password")
                sub_login = st.form_submit_button(auth_t.get("btn_login", "Login"), use_container_width=True)

                if sub_login:
                    if not u_name or not u_pass:
                        st.warning(auth_t.get("fill_all", "⚠️ Please enter your registered username/mobile/email and password."))
                    else:
                        user_data = authenticate_user(u_name, u_pass)
                        if user_data:
                            st.session_state.user = user_data
                            user_sessions = get_user_chat_sessions(user_data["id"])
                            if user_sessions:
                                st.session_state.session_id = user_sessions[0]["session_id"]
                                st.session_state.messages = load_session_messages(user_sessions[0]["session_id"])
                            else:
                                st.session_state.session_id = str(uuid.uuid4())
                                st.session_state.messages = []
                            st.session_state.auth_page = None
                            st.rerun()
                        else:
                            st.error(auth_t.get("invalid_cred", "⚠️ Incorrect Username/Mobile or Password. Please check and try again."))

            st.markdown("<br>", unsafe_allow_html=True)
            if st.button(auth_t.get("go_to_reg", "Register New Account"), use_container_width=True):
                st.session_state.auth_page = "register"
                st.rerun()

        elif st.session_state.auth_page == "register":
            st.markdown(f"""
            <div class="auth-card">
                <h2 style="color:white; margin:0;">{auth_t.get('reg_title', 'Register Account')}</h2>
                <p style="color:#e8f5e9; margin:6px 0 0 0;">{auth_t.get('reg_sub', 'Create a permanent account to sync records')}</p>
            </div>
            """, unsafe_allow_html=True)

            with st.form("full_reg_form"):
                r_full = st.text_input(f"👤 {auth_t.get('full_name', 'Farmer Full Name')}", placeholder="e.g., Yaswanth")
                r_user = st.text_input(f"🆔 {auth_t.get('choose_username', 'Choose Username')}", placeholder="e.g., yaswanth7462")
                r_phone = st.text_input(f"📱 {auth_t.get('mobile_number', 'Mobile Number')}", placeholder="e.g., 9849012345")
                r_email = st.text_input(f"📧 {auth_t.get('email_address', 'Email Address (Optional for PDF Reports)')}", placeholder="e.g., vallemvengalreddy2005@gmail.com")
                r_pass = st.text_input(f"🔑 {auth_t.get('password', 'Password')}", type="password", placeholder="Choose Password (min 4 characters)")
                r_loc = st.text_input(f"📍 {auth_t.get('mandal', 'Village / Mandal')}", value=st.session_state.active_location_name)
                r_acres = st.number_input(f"🌱 {auth_t.get('acres', 'Landholding (Acres)')}", value=2.5, min_value=0.5, step=0.5)

                sub_reg = st.form_submit_button(auth_t.get("btn_register", "Create Account"), use_container_width=True)
                if sub_reg:
                    if not r_user or not r_phone or not r_pass or not r_full:
                        st.warning(auth_t.get("fill_all", "⚠️ Please fill in all required fields (Full Name, Username, Mobile Number, Password)."))
                    elif len(r_user.strip()) < 3:
                        st.error(auth_t.get("choose_username", "⚠️ Username must be at least 3 characters long."))
                    elif not validate_identifier_input(r_phone):
                        st.error(auth_t.get("invalid_phone", "⚠️ Invalid Mobile Number! Please enter a valid 10-digit Indian mobile number (e.g., 9849012345)."))
                    elif r_email and not validate_email_input(r_email):
                        st.error(auth_t.get("invalid_email", "⚠️ Invalid Email Address! Please enter a valid email format (e.g., name@gmail.com)."))
                    elif len(r_pass) < 4:
                        st.error(auth_t.get("pass_short", "⚠️ Password must be at least 4 characters long."))
                    else:
                        if register_user(r_user, r_pass, r_full, r_loc, r_acres, email=r_email, phone=r_phone):
                            if r_email:
                                send_welcome_onboarding_email(r_email, r_full, r_loc, r_acres)
                            st.success(auth_t.get("reg_success", "✅ Account created successfully! Safety policy emailed."))
                            st.session_state.auth_page = "login"
                            st.rerun()
                        else:
                            st.error(auth_t.get("reg_exists", "⚠️ Username, Mobile Number, or Email already registered. Please login."))

            st.markdown("<br>", unsafe_allow_html=True)
            if st.button(auth_t.get("go_to_login", "Go to Login"), use_container_width=True):
                st.session_state.auth_page = "login"
                st.rerun()

    st.stop()

# =========================================================
# 🌾 TOP HEADER BAR
# =========================================================
col_logo, col_lang, col_auth = st.columns([4.5, 2.8, 3.7], vertical_alignment="center")

with col_logo:
    st.markdown("## 🌾 **Kisan Mitra** (AI Agronomist)")

with col_lang:
    selected_lang_label = st.selectbox(
        "Language",
        LANG_LABELS_LIST,
        index=current_lang_idx,
        key="main_lang_selector",
        label_visibility="collapsed"
    )
    new_lang_key = LANG_OPTIONS[selected_lang_label]
    if new_lang_key != st.session_state.lang_key:
        st.session_state.lang_key = new_lang_key
        st.rerun()

lang_key = st.session_state.lang_key
lang_full = selected_lang_label.split(" (")[0]
t = get_text(lang_key)

with col_auth:
    if st.session_state.user:
        ca1, ca2 = st.columns([3, 2])
        ca1.success(f"👤 {st.session_state.user['full_name'][:12]}")
        if ca2.button("🚪 Logout", use_container_width=True):
            st.session_state.user = None
            st.session_state.messages = []
            st.session_state.session_id = str(uuid.uuid4())
            st.rerun()
    else:
        ca_stat, ca_btn1, ca_btn2 = st.columns([1.8, 2, 2], vertical_alignment="center")
        ca_stat.caption("👤 *Guest Mode*")
        if ca_btn1.button("🔓 Login", use_container_width=True):
            st.session_state.auth_page = "login"
            st.rerun()
        if ca_btn2.button("📝 Register", use_container_width=True):
            st.session_state.auth_page = "register"
            st.rerun()

farmer_acres = float(st.session_state.user.get("acres", 2.0)) if st.session_state.user else 2.0
farmer_name_clean = st.session_state.user["full_name"] if st.session_state.user else "Farmer"
farmer_email_clean = st.session_state.user.get("email", "") if st.session_state.user else ""

st.divider()

# =========================================================
# 📍 SIDEBAR: CHAT HISTORY, GPS, WEATHER & PDF/EMAIL
# =========================================================
with st.sidebar:
    st.markdown("### 💬 **Chat History**")
    
    if st.button("➕ **New Advisory Session**", use_container_width=True, key="sidebar_new_chat"):
        st.session_state.session_id = str(uuid.uuid4())
        st.session_state.messages = []
        st.rerun()

    if st.session_state.user:
        user_id = st.session_state.user["id"]
        past_sessions = get_user_chat_sessions(user_id)
        
        if past_sessions:
            for s in past_sessions:
                is_active = (s["session_id"] == st.session_state.session_id)
                btn_cols = st.columns([4, 1])
                with btn_cols[0]:
                    if st.button(
                        f"💬 {s['title']}", 
                        key=f"hist_{s['session_id']}", 
                        use_container_width=True,
                        type="primary" if is_active else "secondary"
                    ):
                        st.session_state.session_id = s["session_id"]
                        st.session_state.messages = load_session_messages(s["session_id"])
                        st.rerun()
                with btn_cols[1]:
                    if st.button("🗑️", key=f"del_{s['session_id']}", help="Delete chat"):
                        delete_user_session(user_id, s["session_id"])
                        if st.session_state.session_id == s["session_id"]:
                            st.session_state.session_id = str(uuid.uuid4())
                            st.session_state.messages = []
                        st.rerun()
        else:
            st.caption("No past chat sessions recorded yet.")
    else:
        st.caption("🔒 *Login to save and revisit your conversations.*")

    st.markdown("---")
    st.markdown(f"### 📍 {t.get('location', 'Current Location')}")

    # 1. Quick Agricultural District Selector
    district_presets = [
        "-- Select / Search District --",
        "Nellore (నెల్లూరు)",
        "Guntur (గుంటూరు)",
        "Madanapalle (మదనపల్లె)",
        "Tirupati (తిరుపతి)",
        "Kurnool (కర్నూలు)",
        "Vijayawada (విజయవాడ)",
        "Anantapur (అనంతపురం)",
        "Kadapa (కడప)",
        "Warangal (వరంగల్)",
        "Karimnagar (కరీంనగర్)",
        "Hyderabad (హైదరాబాద్)",
        "Pune (पुणे)",
        "Nashik (नासिक)",
        "Nagpur (नागपुर)",
        "Coimbatore (கோயம்புத்தூர்)",
        "Belagavi (ಬೆಳಗಾವಿ)",
        "Ludhiana (ਲੁਧਿਆਣਾ)"
    ]
    
    preset_choice = st.selectbox(
        "Quick District Selector",
        district_presets,
        index=0,
        label_visibility="collapsed",
        key="quick_district_select"
    )
    if preset_choice and preset_choice != "-- Select / Search District --":
        clean_selected = preset_choice.split(" ")[0].strip()
        geo_res = geocode_location_strict(clean_selected)
        if geo_res and geo_res["display_name"] != st.session_state.active_location_name:
            st.session_state.current_lat = geo_res["latitude"]
            st.session_state.current_lon = geo_res["longitude"]
            st.session_state.active_location_name = geo_res["display_name"]
            st.rerun()

    # 2. Type Search with Action Button
    c_loc_in, c_loc_btn = st.columns([3, 1])
    with c_loc_in:
        typed_location = st.text_input(
            "Search Village / District",
            value=st.session_state.active_location_name,
            placeholder="e.g. Nellore, నెల్లూరు, Guntur, Pune...",
            label_visibility="collapsed",
            key="custom_loc_input"
        )
    with c_loc_btn:
        set_loc_clicked = st.button("🔍", help="Set Location", use_container_width=True, key="btn_set_loc")

    if set_loc_clicked or (typed_location and typed_location != st.session_state.active_location_name):
        geo_res = geocode_location_strict(typed_location)
        if geo_res:
            st.session_state.current_lat = geo_res["latitude"]
            st.session_state.current_lon = geo_res["longitude"]
            st.session_state.active_location_name = geo_res["display_name"]
            st.rerun()
        else:
            st.warning("⚠️ Location not found. Try entering district name.")

    # 3. GPS Detection Button
    st.components.v1.html("""
    <script>
    function triggerGPS() {
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(
                function(pos) {
                    const url = new URL(window.parent.location.href);
                    url.searchParams.set('lat', pos.coords.latitude.toFixed(4));
                    url.searchParams.set('lon', pos.coords.longitude.toFixed(4));
                    window.parent.location.href = url.href;
                },
                function(err) {
                    console.log("GPS unavailable or denied.");
                },
                { enableHighAccuracy: true, timeout: 8000 }
            );
        }
    }
    </script>
    <button onclick="triggerGPS()" style="
        width: 100%;
        background: linear-gradient(135deg, #2e7d32, #1b5e20);
        color: white;
        padding: 9px;
        border: none;
        border-radius: 8px;
        font-size: 13px;
        font-weight: bold;
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 6px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.2);
    ">
        🎯 Detect Exact GPS Location
    </button>
    """, height=44)

    # 4. Voice Input for Village / Mandal
    st.caption("🎙️ Or Speak Village / District:")
    loc_audio = st.audio_input("Record village", label_visibility="collapsed", key="loc_voice_audio")
    if loc_audio is not None:
        try:
            voice_bytes = loc_audio.read()
            spoken_loc = transcribe_audio_bytes(voice_bytes, lang_code=st.session_state.lang_key)
            if spoken_loc:
                st.success(f"🗣️ {spoken_loc}")
                geo_res = geocode_location_strict(spoken_loc)
                if geo_res:
                    st.session_state.current_lat = geo_res["latitude"]
                    st.session_state.current_lon = geo_res["longitude"]
                    st.session_state.active_location_name = geo_res["display_name"]
                    st.rerun()
                else:
                    st.warning(f"⚠️ Could not find coordinates for: {spoken_loc}")
        except Exception:
            pass

    st.markdown("---")
    st.markdown(f"### 🌦️ {t.get('weather', 'Live Local Weather')}")
    
    farmer_location = st.session_state.active_location_name
    weather_info = get_cached_weather(
        farmer_location, 
        lat=st.session_state.current_lat, 
        lon=st.session_state.current_lon
    )

    is_location_valid = weather_info.get("status") == "success"

    if is_location_valid:
        st.success(f"📍 **{weather_info['location']}**")
        c1, c2 = st.columns(2)
        c1.metric(f"🌡️ {t.get('temp', 'Temperature')}", f"{weather_info['temperature']} °C")
        c2.metric(f"💧 {t.get('humidity', 'Humidity')}", f"{weather_info['humidity']}%")
        
        with st.container(border=True):
            st.write(f"**Condition:** {weather_info['condition']}")
            st.write(f"💨 **Wind:** {weather_info['wind_speed']} km/h")
            st.write(f"🌧️ **Rain Probability:** {weather_info['rain_prob']}%")
            st.caption(weather_info['spray_advisory'])
            
        if weather_info.get("rain_risk"):
            st.warning(f"⚠️ {t.get('rain_alert', 'Rain Alert: Delay spraying')}")
    else:
        st.error("❌ Location not recognized. Please click 'Detect Exact GPS Location'.")

# Pre-fetch cached Data
crop_intel = get_cached_crop_intel(
    farmer_location, 
    st.session_state.current_lat, 
    st.session_state.current_lon
)
live_mandi_data = get_cached_mandi(
    farmer_location, 
    st.session_state.current_lat, 
    st.session_state.current_lon
)
matched_schemes = get_cached_schemes(farmer_acres, farmer_location)

if crop_intel and crop_intel.get("all_crops"):
    area_crop_options = [c["crop"] for c in crop_intel["all_crops"]]
else:
    area_crop_options = ["Paddy / Rice", "Tomato", "Cotton", "Chilli", "Groundnut", "Maize", "Wheat"]

mandi_price_map = {}
for p in live_mandi_data:
    mandi_price_map[p["crop"]] = float(p["modal_price"])

with st.sidebar:
    # 1-Click Master PDF Dossier Export & Automated Email Dispatch
    st.markdown("---")
    st.markdown("### 📜 **Digital Health Dossier & PDF**")
    pdf_fp = generate_pdf_health_card(
        farmer_name=farmer_name_clean,
        location=farmer_location,
        disease_data=st.session_state.latest_disease,
        soil_data=st.session_state.latest_soil,
        weather_data=weather_info if is_location_valid else None,
        crops_data=crop_intel,
        mandi_data=live_mandi_data,
        schemes_data=matched_schemes,
        farmer_acres=farmer_acres
    )
    pdf_raw_bytes = pdf_fp.getvalue()
    
    st.download_button(
        label="📄 Download Farm Dossier (PDF)",
        data=pdf_raw_bytes,
        file_name=f"Kisan_Master_Dossier_{date.today().strftime('%Y%m%d')}.pdf",
        mime="application/pdf",
        use_container_width=True
    )

    with st.expander("📧 **Email PDF to Farmer / Extension Office**", expanded=False):
        dest_email = st.text_input("Destination Email:", value=farmer_email_clean, placeholder="farmer@gmail.com")
        if st.button("🚀 Send PDF via Email", use_container_width=True):
            if not dest_email or not dest_email.strip():
                st.warning("⚠️ Please enter a destination email address.")
            elif not validate_email_input(dest_email):
                st.error("⚠️ Invalid email format! Please enter a valid address (e.g. farmer@gmail.com).")
            else:
                with st.spinner("Dispatching complete Farm Dossier PDF via SMTP..."):
                    mail_res = send_health_card_email(
                        to_email=dest_email.strip(),
                        farmer_name=farmer_name_clean,
                        location=farmer_location,
                        pdf_bytes=pdf_raw_bytes,
                        diagnosis_data=st.session_state.latest_disease
                    )
                    if mail_res["status"] == "success":
                        st.success(mail_res["message"])
                    else:
                        st.error(mail_res["message"])

tab_keys = ["voice", "crops", "mandi", "leaf", "radar", "sms", "water", "soil", "natural", "calendar", "profit", "schemes", "community"]
tab_labels = [t["tabs"].get(k, k.capitalize()) for k in tab_keys]
tabs = st.tabs(tab_labels)

# =========================================================
# 💬 TAB 1: VOICE & CHAT AI ADVISOR (WITH GUARDRAILS)
# =========================================================
with tabs[0]:
    c_head1, c_head2 = st.columns([4, 1])
    with c_head1:
        st.subheader(f"🎙️ {t.get('voice_title', 'Dynamic AI Agronomist')}")
    with c_head2:
        if st.button("➕ New Chat", use_container_width=True, key="main_new_chat"):
            st.session_state.session_id = str(uuid.uuid4())
            st.session_state.messages = []
            st.rerun()

    audio_val = st.audio_input("🎙️ RECORD VOICE QUERY (Click mic to speak in your language)")
    user_query = None

    if audio_val is not None:
        audio_bytes = audio_val.read()
        with st.spinner(t.get("voice_listen", "Listening...")):
            recognized_text = transcribe_audio_bytes(audio_bytes, lang_code=lang_key)
            if recognized_text:
                user_query = recognized_text
                st.success(f"🗣️ {t.get('voice_spoken', 'You Said')}: {recognized_text}")

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            if "⚠️" in msg["content"] and msg["role"] == "assistant":
                st.warning(msg["content"])
            else:
                st.markdown(msg["content"])
            if "badge" in msg and msg["badge"]:
                st.caption(msg["badge"])
            if "audio_bytes" in msg and msg["audio_bytes"]:
                st.audio(msg["audio_bytes"], format="audio/mp3")

    text_input = st.chat_input("Ask any agricultural, pest, fertilizer, or crop question...")
    if text_input:
        user_query = text_input

    if user_query:
        # 1. Security & Prompt Injection Guardrail
        is_query_valid, guardrail_err = guardrail_engine.validate_user_query(user_query)
        
        st.session_state.messages.append({"role": "user", "content": user_query})
        
        current_user_id = st.session_state.user["id"] if st.session_state.user else None
        if current_user_id:
            save_chat_message(current_user_id, st.session_state.session_id, "user", user_query)
        
        with st.chat_message("user"):
            st.markdown(user_query)

        with st.chat_message("assistant"):
            if not is_query_valid:
                st.warning(guardrail_err)
                st.session_state.messages.append({"role": "assistant", "content": guardrail_err})
            else:
                with st.spinner("🌾 Kisan Mitra AI consulting ICAR agronomy standards & CIB&RC guardrails..."):
                    gemini_reply = gemini_advisor.generate_response(
                        query=user_query,
                        language=lang_full,
                        weather_context=weather_info if is_location_valid else None,
                        location=farmer_location if is_location_valid else "India"
                    )

                    # 2. Chemical Safety & Dosage Audit
                    audit = guardrail_engine.audit_ai_response(gemini_reply)
                    
                    if "⚠️" in gemini_reply:
                        st.warning(gemini_reply)
                    else:
                        st.markdown(gemini_reply)
                        st.caption(f"🛡️ **{audit['security_badge']}** | Grounded in ICAR agronomy standards")
                        if audit.get("warnings"):
                            for w in audit["warnings"]:
                                st.warning(w)
                    
                    if current_user_id:
                        save_chat_message(current_user_id, st.session_state.session_id, "assistant", gemini_reply)
                    
                    # Audio generation
                    try:
                        audio_fp = generate_voice_audio(gemini_reply, lang=lang_key)
                        audio_data = audio_fp.getvalue()
                        st.audio(audio_data, format="audio/mp3", autoplay=True)
                        st.session_state.messages.append({
                            "role": "assistant", 
                            "content": gemini_reply, 
                            "audio_bytes": audio_data,
                            "badge": f"🛡️ {audit['security_badge']}"
                        })
                    except Exception:
                        st.session_state.messages.append({
                            "role": "assistant", 
                            "content": gemini_reply,
                            "badge": f"🛡️ {audit['security_badge']}"
                        })
        st.rerun()

# =========================================================
# 🌱 TAB 2: SUITABLE CROPS
# =========================================================
with tabs[1]:
    st.subheader(f"🌱 {t.get('crops_title', 'Suitable Crops')} ({weather_info.get('location', farmer_location)})")
    if crop_intel:
        col_m1, col_m2, col_m3 = st.columns(3)
        col_m1.info(f"🏛️ Zone: **{crop_intel['zone_name']}**")
        col_m2.info(f"🟤 Soil: **{crop_intel['soil_profile']}**")
        col_m3.info(f"🌧️ Climate: **{crop_intel['climate_profile']}**")

        for idx, c in enumerate(crop_intel["all_crops"]):
            with st.container(border=True):
                head_col, score_col = st.columns([3.5, 1.5])
                with head_col:
                    st.markdown(f"### {c['crop']}")
                    st.caption(f"Category: **{c.get('category', 'Cash Crop')}** | Season: **{c.get('season', 'Kharif / Rabi')}**")
                with score_col:
                    st.metric("Suitability", f"{c.get('suitability', 90)}%")

                d_col1, d_col2 = st.columns(2)
                with d_col1:
                    st.write(f"🧬 **Varieties:** `{c.get('varieties', 'Hybrid')}`")
                    st.write(f"💧 **Water Need:** {c.get('water_need', 'Medium')}")
                with d_col2:
                    st.write(f"🔬 **Agro Match:** {c.get('why_suitable', 'Optimal conditions.')}")
                    st.write(f"🚛 **Market Access:** **{c.get('market_link', 'APMC Mandi')}**")

                crop_speech_text = f"{c['crop']}. Season: {c.get('season')}. Varieties: {c.get('varieties')}. Water need: {c.get('water_need')}."
                if st.button(f"{t.get('listen_btn', '🔊 Listen')} - {c['crop']}", key=f"voice_crop_{idx}"):
                    c_audio = generate_voice_audio(crop_speech_text, lang=lang_key)
                    st.audio(c_audio.getvalue(), format="audio/mp3", autoplay=True)

# =========================================================
# 💰 TAB 3: LIVE MANDI RATES
# =========================================================
with tabs[2]:
    st.subheader(f"💰 {t.get('mandi_title', 'Live Mandi Rates')} ({weather_info.get('location', farmer_location)})")
    cols = st.columns(3)
    for idx, p in enumerate(live_mandi_data):
        with cols[idx % 3]:
            with st.container(border=True):
                st.markdown(f"### {p['crop']}")
                st.caption(f"Market: **{p['primary_market']}**")
                st.metric(label=f"Modal Rate: ₹{p['modal_price']:,} / Q", value=f"₹{p['modal_price']:,}", delta=p["trend"])
                st.write(f"Range: ₹{p['min_price']:,} - ₹{p['max_price']:,}")
                st.write(f"Arrivals: **{p['arrivals_tonnes']} Tonnes**")
                st.caption(f"Updated: {p['updated']}")

# =========================================================
# 📷 TAB 4: LEAF DISEASE DOCTOR
# =========================================================
with tabs[3]:
    st.subheader(f"📷 {t.get('leaf_title', 'Universal Crop Leaf Diagnostic Scanner')}")
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
        c_img, c_diag = st.columns([1.2, 2.3])
        with c_img:
            st.image(img_to_analyze, caption="Processed Image", use_container_width=True)
        with c_diag:
            if st.button(t.get("scan_btn", "⚡ Scan & Diagnose Leaf"), use_container_width=True):
                result = classifier.predict(img_to_analyze)
                st.session_state.latest_disease = result
                log_diagnostic(
                    farmer_name_clean, 
                    farmer_location, 
                    result["leaf_name"], 
                    result["disease"], 
                    result["confidence"], 
                    result["treatment"],
                    lat=st.session_state.current_lat,
                    lon=st.session_state.current_lon
                )

                st.success(f"🌱 Plant: **{result['leaf_name']}**")
                st.info(f"🔬 Diagnosis: **{result['disease']}** ({int(result['confidence']*100)}% Match)")
                st.write(f"🦠 **Pathogen:** {result['pathogen']}")
                st.write(f"🔍 **Symptoms:** {result['symptoms']}")
                
                # Dual Prescriptions (ZBNF & Chemical)
                with st.container(border=True):
                    st.markdown("#### 🌿 **Organic / Natural Farming (ZBNF):**")
                    st.write(result.get("organic_treatment", result["treatment"]))
                    
                    st.markdown("#### 🧪 **Integrated Chemical Prescription:**")
                    st.write(result.get("chemical_treatment", result["treatment"]))
                    st.caption(f"⏳ Pre-Harvest Interval (PHI Waiting Period): **{result.get('phi_days', 7)} Days**")

                st.info("📡 **Live Telemetry:** Geotagged scan incident logged to the Community Outbreak Radar.")

                # Automated Background Email Dispatch for Registered Farmers
                if farmer_email_clean and "@" in farmer_email_clean:
                    auto_pdf = generate_pdf_health_card(
                        farmer_name=farmer_name_clean,
                        location=farmer_location,
                        disease_data=result,
                        soil_data=st.session_state.latest_soil,
                        weather_data=weather_info if is_location_valid else None,
                        crops_data=crop_intel,
                        mandi_data=live_mandi_data,
                        schemes_data=matched_schemes,
                        farmer_acres=farmer_acres
                    )
                    send_health_card_email(
                        to_email=farmer_email_clean,
                        farmer_name=farmer_name_clean,
                        location=farmer_location,
                        pdf_bytes=auto_pdf.getvalue(),
                        diagnosis_data=result
                    )
                    st.success(f"📧 **Automated Dispatch:** Complete Digital Health Dossier (PDF) emailed to `{farmer_email_clean}`.")

                diag_speech = f"Diagnosed {result['leaf_name']} with {result['disease']}. {result.get('treatment')}"
                diag_audio = generate_voice_audio(diag_speech, lang=lang_key)
                st.audio(diag_audio.getvalue(), format="audio/mp3", autoplay=True)

# =========================================================
# 🚨 TAB 5: PEST OUTBREAK RADAR (REAL CROWDSOURCED TELEMETRY)
# =========================================================
with tabs[4]:
    st.subheader(f"🚨 {t.get('radar_title', 'Hyperlocal Pest Outbreak Surveillance Radar')}")
    st.caption(f"Real-time epidemiological disease telemetry within 60 km radius of **{farmer_location}**.")

    radar_data = generate_regional_radar_clusters(
        st.session_state.current_lat, 
        st.session_state.current_lon, 
        farmer_location
    )

    if radar_data["map_points"]:
        map_df_data = [{"latitude": p["latitude"], "longitude": p["longitude"]} for p in radar_data["map_points"]]
        st.map(map_df_data, zoom=10)

    st.markdown("### ⚠️ **Active Cluster Outbreak Alerts**")
    for alert in radar_data["alerts"]:
        with st.container(border=True):
            r_c1, r_c2 = st.columns([3, 1])
            with r_c1:
                st.markdown(f"#### {alert['severity']} — {alert['crop']}: {alert['pest']}")
                st.write(f"📢 **Action Advisory:** {alert['advisory']}")
            with r_c2:
                st.metric("Cluster Density", f"{alert['cases']} Farms")
                st.caption(f"📍 {alert['radius']}")

    with st.expander("📋 **View Verified Outbreak Incident Log (SQLite Database)**", expanded=False):
        st.caption("All records are cryptographically timestamped and linked to real field scans:")
        st.dataframe(
            [
                {
                    "Distance (km)": f"{p['distance_km']} km",
                    "Crop": p["crop"],
                    "Diagnosed Pest / Disease": p["pest"],
                    "Risk Level": p["severity"],
                    "Village / Location": p.get("location", "Nearby"),
                    "GPS (Lat, Lon)": f"{p['latitude']:.4f}, {p['longitude']:.4f}"
                }
                for p in radar_data["map_points"]
            ],
            use_container_width=True
        )

# =========================================================
# 📱 TAB 6: RURAL OFFLINE SMS & USSD SIMULATOR
# =========================================================
with tabs[5]:
    st.subheader(f"📱 {t.get('sms_title', 'Rural Offline Feature-Phone SMS & USSD Simulator')}")
    st.info("💡 **Judge Presentation Hook:** Demonstrates how low-bandwidth rural farmers without smartphones receive instant 160-character regional SMS and automated IVR voice calls via standard GSM.")

    with st.form("sms_sim_form"):
        c_sms1, c_sms2 = st.columns([3, 1])
        with c_sms1:
            sms_input = st.text_input(
                "Simulate Inbound SMS / USSD Query to 56161:", 
                value="KISAN PEST TOMATO",
                placeholder="e.g., KISAN PEST TOMATO, KISAN MANDI PADDY, KISAN WEATHER..."
            )
        with c_sms2:
            st.markdown("<br>", unsafe_allow_html=True)
            sms_submit = st.form_submit_button("📩 Send SMS", use_container_width=True)

    if sms_input:
        sms_res = process_offline_sms_query(sms_input, lang_code=lang_key, location=farmer_location.split(',')[0])
        
        c_ph, c_ivr = st.columns(2)
        with c_ph:
            with st.container(border=True):
                st.markdown("### 📟 **Outbound GSM SMS Payload**")
                st.code(sms_res["sms_response"], language="text")
                st.caption(f"Length: **{sms_res['character_count']}/160 Chars** | Valid Single GSM SMS: {'✅ Yes' if sms_res['is_valid_sms'] else '⚠️ Segmented'}")
                st.caption(f"Channel: {sms_res['channel']} | Help: {sms_res['toll_free_help']}")

        with c_ivr:
            with st.container(border=True):
                st.markdown("### 📞 **Automated IVR Voice Callback**")
                st.write(f"🗣️ *\"{sms_res['ivr_audio_transcript']}\"*")
                ivr_audio = generate_voice_audio(sms_res["ivr_audio_transcript"], lang=lang_key)
                st.audio(ivr_audio.getvalue(), format="audio/mp3")

# =========================================================
# 💧 TAB 7: SMART IRRIGATION
# =========================================================
with tabs[6]:
    st.subheader(f"💧 {t.get('irrigation_title', 'Smart Irrigation & Evapotranspiration Engine')}")
    
    with st.form("irrigation_fast_form"):
        c_ir1, c_ir2, c_ir3 = st.columns(3)
        with c_ir1:
            irr_crop = st.selectbox("🌱 Cultivated Crop", area_crop_options)
            acres_in = st.number_input("🚜 Area (Acres)", value=farmer_acres, min_value=0.5, step=0.5)
        
        with c_ir2:
            growth_st = st.selectbox("🌿 Active Growth Stage", ["Seedling Stage", "Vegetative Growth", "Flowering & Fruit Setting", "Maturity & Harvesting"])
            pump_hp = st.number_input("⚡ Motor Pump Power (HP)", value=5.0, min_value=1.0, step=1.0)
        
        with c_ir3:
            irr_method = st.selectbox(
                "🚿 Irrigation Method",
                ["Drip Irrigation (90% Efficiency)", "Sprinkler Irrigation (75% Efficiency)", "Furrow / Flood Irrigation (55% Efficiency)"]
            )
            live_temp = weather_info.get("temperature", 28.5) if is_location_valid else 28.5
            live_humidity = weather_info.get("humidity", 60) if is_location_valid else 60
            st.info(f"⛅ Weather: **{live_temp}°C** | **{live_humidity}% Humidity**")

        submit_irrig = st.form_submit_button(t.get("irrigation_btn", "Calculate Irrigation Needs"), use_container_width=True)

    if submit_irrig:
        irr_res = calculate_irrigation(
            crop=irr_crop,
            growth_stage=growth_st,
            acres=acres_in,
            pump_hp=pump_hp,
            temp_c=live_temp,
            humidity_pct=live_humidity,
            wind_speed_kmh=weather_info.get("wind_speed", 12.0) if is_location_valid else 12.0,
            irrigation_method=irr_method
        )

        st.markdown("---")
        m_col1, m_col2, m_col3, m_col4 = st.columns(4)
        m_col1.metric("💧 Daily Water Requirement", f"{irr_res['liters_per_day']:,} L")
        m_col2.metric("⏱️ Recommended Pump Runtime", irr_res["runtime_formatted"], f"{irr_res['pump_runtime_hours']} Hours")
        m_col3.metric("📐 Reference ET (ET0)", f"{irr_res['et0_mm']} mm/day", f"Crop Kc: {irr_res['kc_value']}")
        m_col4.metric("⚡ Power Consumption", f"{irr_res['power_kwh']} kWh", f"Efficiency: {irr_res['efficiency_pct']}%")

# =========================================================
# 🧪 TAB 8: SOIL HEALTH & NPK
# =========================================================
with tabs[7]:
    st.subheader(f"🧪 {t.get('soil_title', 'Soil Health & NPK Recommendation')}")
    with st.form("soil_fast_form"):
        col1, col2 = st.columns(2)
        with col1:
            s_crop = st.selectbox("Target Crop for Dose", area_crop_options)
            n_in = st.number_input("Nitrogen (N) kg/ha", value=80.0)
            p_in = st.number_input("Phosphorus (P) kg/ha", value=30.0)
        with col2:
            k_in = st.number_input("Potassium (K) kg/ha", value=35.0)
            ph_in = st.number_input("Soil pH", value=6.5, min_value=1.0, max_value=14.0)

        sub_soil = st.form_submit_button(t.get("soil_btn", "Calculate Fertilizer"), use_container_width=True)

    if sub_soil:
        res = analyze_soil_npk(s_crop, n_in, p_in, k_in, ph_in)
        st.session_state.latest_soil = res
        for item in res["recommendations"]:
            st.info(item)

# =========================================================
# 🌿 TAB 9: NATURAL BIO-PESTICIDES & ZBNF BOTANICAL DEFENSE
# =========================================================
with tabs[8]:
    st.subheader(f"🌿 {t.get('natural_title', 'Zero Budget Natural Bio-Pesticide Formulations (ZBNF)')}")
    st.caption("100% Organic, Chemical-Free, ICAR & SPNF Grounded Botanical Recipes tailored to your acreage.")

    col_opt1, col_opt2 = st.columns([1.5, 1])
    with col_opt1:
        form_keys = list(NATURAL_FORMULATIONS.keys())
        form_labels = [NATURAL_FORMULATIONS[k]["name"].get(lang_key, NATURAL_FORMULATIONS[k]["name"]["en"]) for k in form_keys]
        selected_idx = st.selectbox(
            "🌱 Select Natural Bio-Formulation:",
            range(len(form_keys)),
            format_func=lambda i: form_labels[i],
            key="nat_form_select"
        )
        selected_key = form_keys[selected_idx]

    with col_opt2:
        calc_mode = st.radio("📐 Scale Formulation By:", ["Landholding (Acres)", "Knapsack Spray Pumps (15L)"], horizontal=True)

    c_scale1, c_scale2 = st.columns(2)
    with c_scale1:
        if calc_mode == "Landholding (Acres)":
            scale_acres = st.number_input("🚜 Cultivated Area (Acres)", value=float(farmer_acres), min_value=0.25, step=0.25)
            scaled_data = calculate_scaled_formulation(selected_key, acres=scale_acres)
        else:
            scale_pumps = st.number_input("🎒 Number of 15L Knapsack Pumps", value=10, min_value=1, step=1)
            scaled_data = calculate_scaled_formulation(selected_key, knapsack_pumps=scale_pumps)

    with c_scale2:
        st.info(f"🎯 **Formulation Target:** {scaled_data['unit_label']}")
        st.caption(f"🐛 **Controls:** {scaled_data['target_pests']}")
        st.caption(f"🌾 **Ideal for:** {', '.join(scaled_data['target_crops'])}")

    with st.container(border=True):
        st.markdown("### 🧪 **Calculated Raw Ingredients Needed**")
        ing_cols = st.columns(len(scaled_data["scaled_ingredients"]))
        for i_idx, (ing_name, ing_val) in enumerate(scaled_data["scaled_ingredients"].items()):
            with ing_cols[i_idx % len(ing_cols)]:
                st.metric(label=ing_name, value=f"{ing_val['scaled_qty']} {ing_val['unit']}")

        badge_c1, badge_c2, badge_c3 = st.columns(3)
        badge_c1.info(f"⏳ **Fermentation Period:** {scaled_data['fermentation_days']}")
        badge_c2.info(f"📦 **Shelf Life:** {scaled_data['shelf_life']}")
        badge_c3.info(f"🚿 **Application Ratio:** {scaled_data['application_method']}")

    st.markdown("### 📝 **Step-by-Step Preparation & Brewing Guide**")
    for step_num, step_text in enumerate(scaled_data["steps"], 1):
        st.markdown(f"**{step_num}.** {step_text}")

    st.warning(f"📢 **Field Application Schedule:** {scaled_data['spray_schedule']}")

    recipe_speech = f"{scaled_data['name'].get(lang_key, scaled_data['name']['en'])}. Target pests: {scaled_data['target_pests']}. Ingredients needed: " + ", ".join([f"{k} {v['scaled_qty']} {v['unit']}" for k, v in scaled_data['scaled_ingredients'].items()])
    if st.button(f"🔊 {t.get('listen_btn', 'Listen Preparation Guide')}", key=f"audio_nat_{selected_key}"):
        nat_audio = generate_voice_audio(recipe_speech, lang=lang_key)
        st.audio(nat_audio.getvalue(), format="audio/mp3", autoplay=True)

    st.markdown("---")
    with st.expander("🔍 **Find Recommended Natural Solution by Pest / Crop Problem**", expanded=False):
        c_prob1, c_prob2 = st.columns(2)
        with c_prob1:
            filter_crop = st.selectbox("Your Crop", ["All Crops"] + area_crop_options, key="nat_filter_crop")
        with c_prob2:
            filter_prob = st.selectbox(
                "Observed Pest / Disease Category",
                [
                    "All",
                    "Sucking Pests (Aphids, Thrips, Whiteflies)",
                    "Caterpillars & Stem Borers",
                    "Pod Borers & Bollworms",
                    "Fungal Diseases, Blight & Mildew",
                    "Soil Health & Root Vigor Booster"
                ],
                key="nat_filter_prob"
            )

        matched_recs = get_recommendations_by_problem(filter_crop, filter_prob)
        for m_item in matched_recs:
            with st.container(border=True):
                st.markdown(f"#### {m_item['name'].get(lang_key, m_item['name']['en'])}")
                st.write(f"🎯 **Target:** {m_item['target_pests']}")
                st.caption(f"🌾 **Crops:** {', '.join(m_item['target_crops'])} | ⏳ **Fermentation:** {m_item['fermentation_days']}")
                st.write(f"💧 **How to Apply:** {m_item['application_method']}")

# =========================================================
# 📅 TAB 10: CROP ACTIVITY SCHEDULE
# =========================================================
with tabs[9]:
    st.subheader(f"📅 {t.get('calendar_title', 'Crop Activity Schedule')}")
    cal_crop = st.selectbox("Sown Crop", area_crop_options, key="cal_crop_select")
    sow_d = st.date_input("Sowing Date", value=date.today())
    schedule = get_crop_calendar(cal_crop, sow_d)
    for title, dt, desc in schedule:
        with st.expander(f"📍 {dt.strftime('%d %b %Y')} - {title}", expanded=True):
            st.write(desc)

# =========================================================
# 📈 TAB 11: YIELD & PROFIT FORECASTER
# =========================================================
with tabs[10]:
    st.subheader(f"📈 {t.get('profit_title', 'Crop Economics & Profit Forecaster')}")

    with st.form("profit_fast_form"):
        col_p1, col_p2, col_p3 = st.columns(3)
        with col_p1:
            f_crop = st.selectbox("🌱 Forecast Crop", area_crop_options)
            f_acres = st.number_input("🚜 Area (Acres)", value=farmer_acres, min_value=0.5, step=0.5)

        bench = get_regional_crop_cost_benchmarks(f_crop, farmer_location)
        auto_price = mandi_price_map.get(f_crop, 2250.0)

        with col_p2:
            f_price = st.number_input("💰 Expected Mandi Price (₹/Quintal)", value=float(auto_price), step=50.0)
            expected_yield_input = st.number_input("🌾 Expected Yield (Quintals/Acre)", value=float(bench["avg_yield_q"]), min_value=1.0, step=1.0)

        with col_p3:
            st.info(f"📍 Cost Index Context: **{farmer_location.split(',')[0]}**")
            in_seed = st.number_input("🌱 Seeds & Nursery (₹/Acre)", value=float(bench["seed_nursery_cost"]))
            in_machine = st.number_input("🚜 Tractor & Machinery (₹/Acre)", value=float(bench["machinery_plough_cost"]))
            in_fert_pest = st.number_input("🧪 Fertilizers & Pesticides (₹/Acre)", value=float(bench["fertilizer_pesticide_cost"]))
            in_labour = st.number_input("👥 Labour & Harvesting (₹/Acre)", value=float(bench["labour_harvest_cost"]))
            in_misc = st.number_input("🚛 Transport & Misc (₹/Acre)", value=float(bench["irrigation_electricity_cost"] + bench["transport_packaging_cost"]))

        calc_submit = st.form_submit_button(t.get("profit_btn", "Forecast Farm Economics"), use_container_width=True)

    if calc_submit:
        eco_res = forecast_yield_and_profit_advanced(
            crop=f_crop,
            acres=f_acres,
            expected_price_per_q=f_price,
            custom_yield_q_per_acre=expected_yield_input,
            seeds_cost_per_acre=in_seed,
            machinery_cost_per_acre=in_machine,
            fertilizer_pesticides_per_acre=in_fert_pest,
            labour_harvesting_per_acre=in_labour,
            transport_other_per_acre=in_misc,
            state=farmer_location
        )

        st.markdown("---")
        kpi1, kpi2, kpi3, kpi4 = st.columns(4)
        kpi1.metric("🌾 Total Production", f"{eco_res['total_yield_quintals']} Q", f"{eco_res['yield_per_acre']} Q/Acre")
        kpi2.metric("💸 Total Cost (A2+FL)", f"₹{eco_res['total_cost_all_acres']:,}", f"₹{eco_res['total_cost_per_acre']:,} / Acre")
        kpi3.metric("💵 Gross Mandi Revenue", f"₹{eco_res['gross_revenue']:,}")
        
        profit_delta = f"ROI: +{eco_res['roi_percent']}%" if eco_res['net_profit'] >= 0 else f"Loss: {eco_res['roi_percent']}%"
        kpi4.metric("💰 Net Profit", f"₹{eco_res['net_profit']:,}", delta=profit_delta)

# =========================================================
# 🏛️ TAB 12: GOVT SCHEMES
# =========================================================
with tabs[11]:
    st.subheader(f"🏛️ {t.get('schemes_title', 'Government Schemes')} ({farmer_name_clean})")
    matched_schemes = get_cached_schemes(farmer_acres, farmer_location)

    for sch in matched_schemes:
        with st.container(border=True):
            s_head1, s_head2 = st.columns([3, 1])
            with s_head1:
                st.markdown(f"### 🏷️ {sch['name']}")
                st.caption(f"🏛️ **Authority:** {sch['authority']}")
            with s_head2:
                st.link_button("🌐 Apply Portal", sch["portal_url"], use_container_width=True)

            st.success(f"🎁 **Benefit:** {sch['benefit']}")
            st.info(f"👤 **Eligibility:** {sch['eligibility']}")

# =========================================================
# 👥 TAB 13: REGIONAL COMMUNITY
# =========================================================
with tabs[12]:
    st.subheader(f"👥 {t.get('community_title', 'Regional Community')} ({farmer_location})")
    comm_data = get_cached_community(farmer_location)
    c_b1, c_b2 = st.columns([2, 1])
    with c_b1:
        st.info(f"📍 Cluster: **{comm_data['mandal']} / {comm_data['district']}**")
    with c_b2:
        st.link_button(t.get("share_whatsapp", "Share on WhatsApp"), comm_data["share_url"], use_container_width=True)

    st.markdown(f"### {t.get('wa_heading', 'WhatsApp Groups')}")
    cols_w = st.columns(3)
    for idx, grp in enumerate(comm_data["whatsapp_groups"]):
        with cols_w[idx % 3]:
            with st.container(border=True):
                st.markdown(f"#### {grp['name']}")
                st.caption(f"📂 {grp['category']}")
                st.write(f"👥 {grp['members']}")
                st.write(grp["description"])
                st.link_button("Join WhatsApp Group", grp["link"], use_container_width=True)

    st.markdown(f"### {t.get('tg_heading', 'Telegram Channels')}")
    cols_t = st.columns(2)
    for idx, ch in enumerate(comm_data["telegram_channels"]):
        with cols_t[idx % 2]:
            with st.container(border=True):
                st.markdown(f"#### {ch['name']}")
                st.caption(f"📂 {ch['category']}")
                st.write(f"👥 {ch['members']}")
                st.write(ch["description"])
                st.link_button("Join Telegram Channel", ch["link"], use_container_width=True)
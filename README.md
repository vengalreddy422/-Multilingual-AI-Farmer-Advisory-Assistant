# 🌾 Kisan Mitra (किसान मित्र / కిసాన్ మిత్ర)
### **Autonomous Multilingual AI Agricultural Advisory & Crop Defense System**
> **Problem Statement:** `I-NXS-010 — Multilingual AI Farmer Advisory Assistant`  
> **Target Audience:** Smallholder & Marginal Farmers, Agronomists, Gram Panchayat Extension Officers across India.

---

## 🌟 Executive Summary & Hackathon Vision

**Kisan Mitra** is an enterprise-grade, decentralized agricultural operating system designed to bridge the digital divide for over 140 million Indian farmers. Combining **multimodal LLM intelligence (Gemini 2.5 Flash)**, **on-device low-latency neural vision (MobileNetV2 / ONNX)**, **real-time spatial GPS pest telemetry**, and **zero-internet GSM SMS/IVR simulation**, Kisan Mitra provides ICAR & SAU-grounded precision agronomy in **6 Indian languages** (Telugu, Hindi, English, Tamil, Kannada, Marathi).

---

## 🚀 Key First-Prize Highlights & Innovations

```
                                 ┌──────────────────────────────────────────────┐
                                 │       🌾 KISAN MITRA AI CORE PLATFORM        │
                                 └──────────────────────┬───────────────────────┘
                                                        │
         ┌──────────────────────────────┬───────────────┴───────────────┬──────────────────────────────┐
         ▼                              ▼                               ▼                              ▼
  🎙️ Voice-to-Voice AI           📷 Leaf Doctor Vision           🚨 Spatial Pest Radar          📱 Offline GSM SMS / IVR
  • 6 Indian Languages           • <15ms ONNX Inference          • Real GPS Telemetry           • Compact 160-char SMS
  • Gemini Multimodal Audio      • Dual Organic + Chemical       • Haversine Spatial Query      • Automated Audio Callback
  • CIB&RC Safety Guardrails     • Automated Email PDF           • Community Early Warning      • 2G Keypad Phone Support
```

### 1. 🎙️ Multilingual Voice-to-Voice AI Agronomist (Tab 1)
- Speaks and understands natural conversational speech in **Telugu, Hindi, English, Tamil, Kannada, and Marathi**.
- **CIB&RC Chemical Safety & Dosage Defense:** Intercepts banned chemicals (Endosulfan, DDT, Paraquat) and validates concentration thresholds (flags >15 ml/L toxic overdosing).
- **Dual Prescription Strategy:** Generates both **Zero Budget Natural Farming (ZBNF)** biological remedies (Jeevamrutha, Neemastra, Trichoderma) and calibrated chemical formulations with exact Pre-Harvest Intervals (PHI).

### 2. 🌱 Agro-Climatic Crop Matrix & Live Mandi Index (Tabs 2 & 3)
- Dynamic agro-climatic suitability matrix based on soil texture, rainfall, and season (Kharif, Rabi, Zaid).
- Real-time **APMC Mandi Price Index** with modal pricing and market arrival tracking.

### 3. 📷 Universal Leaf Doctor & Automated Zero-Click PDF Dispatch (Tab 4)
- Fast on-device neural vision classifier (<15 ms latency) diagnosing 38+ foliar diseases across Cotton, Paddy, Tomato, Chilli, Wheat, Groundnut, and Maize.
- **Zero-Click Background Email Dispatch:** When a registered farmer scans a leaf, the system automatically emails the complete 2-page Master Farm Dossier PDF via Gmail SMTP.

### 4. 🚨 Real Spatial Pest Outbreak Radar (Tab 5)
- Powered by persistent SQLite GPS telemetry (`farm_ledger.db`).
- Performs real-time **Haversine spatial distance calculations** to alert nearby farmers within a 60 km radius of active pest infestations.

### 5. 📱 Rural Offline GSM SMS & IVR Feature Phone Simulator (Tab 6)
- Designed for rural 2G/keypad phone users without internet access.
- Strictly validates `<= 160 characters` for single-payload GSM SMS and generates interactive voice IVR callback simulations.

### 6. 💧 Smart Evapotranspiration & NPK Calculators (Tabs 7, 8, 9 & 10)
- **FAO-56 Penman-Monteith Evapotranspiration Engine:** Calculates exact daily crop water requirements in liters/acre and irrigation pump runtime.
- **Soil NPK Stoichiometry:** Translates soil test values into tailored Urea, DAP, and MOP bag requirements.
- **Farm Profit Forecaster:** Calculates A2+FL production costs, MSP procurement margins, and net profit per acre.

### 7. 📜 2-Page Master Farm Health Dossier (PDF) & Live SMTP
- Automatically compiles:
  - **Page 1:** Farmer identity, weather suitability, foliar diagnostics, and NPK fertilizer dosage.
  - **Page 2:** Regional crop suitability matrix, APMC mandi rates, matched government welfare schemes (PM-KISAN, PMKSY, PMFBY), and extension contact info.
- Built-in live **Gmail SMTP integration** with real-time dynamic `.env` configuration.

### 8. 🛡️ Dual Gemini API Key Failover Pool
- Built-in automatic API key rotation pool. If Key 1 reaches rate limits or network issues, the system automatically switches to Key 2 with zero user interruption.

---

## 🛠️ Technology Stack

| Layer | Technology |
| :--- | :--- |
| **Frontend UI** | Streamlit, Responsive CSS3 Glassmorphism |
| **Generative AI & LLM** | Google Gemini 2.5 Flash API (`google-genai` SDK) |
| **Edge Vision & Diagnostics** | ONNX Runtime, MobileNetV2, Pillow |
| **Speech Processing** | Edge-TTS, gTTS, SpeechRecognition |
| **PDF Generation** | ReportLab Enterprise PDF Engine |
| **Database & Telemetry** | SQLite3 (`farm_ledger.db`), Spatial Haversine Engine |
| **Email Gateway** | Python SMTP / MIME with SSL/TLS |
| **Localization (i18n)** | Custom 6-Language Localization Matrix (`i18n.py`) |

---

## 📁 Repository Structure

```
Farmers/
├── app.py                     # Main Streamlit Application & Multi-Tab Hub
├── requirements.txt           # Python Dependencies
├── .env.example               # Environment Template
├── .gitignore                 # Git Ignore Configuration
├── README.md                  # Project Documentation
├── config/
│   └── settings.py            # Global Config & Pydantic Settings
├── models/                    # Pretrained Neural Network Weights & ONNX Models
├── data/                      # Reference Agricultural Knowledge Bases
└── src/
    ├── database/
    │   ├── db_ledger.py       # SQLite Telemetry, Users & Diagnostics History
    │   └── session_state.py   # Streamlit Session State Initializer
    ├── intelligence/
    │   ├── gemini_advisor.py  # Gemini Multimodal LLM Advisor & Dual Failover Pool
    │   └── guardrails.py      # CIB&RC Chemical Safety & Toxicity Filter
    └── tools/
        ├── agri_modules.py    # Government Schemes & Crop Calendars
        ├── community_links.py # Regional WhatsApp & Telegram Farmer Groups
        ├── dynamic_engine.py  # Agro-Climatic Suitability & Mandi Data Engine
        ├── email_dispatcher.py# Live SMTP Dispatcher & Welcome Policy Kit
        ├── i18n.py            # 6-Language Localization Matrix
        ├── offline_sms.py     # Dynamic 160-char SMS & Voice IVR Simulator
        ├── pdf_generator.py   # 2-Page Master Farm Health Dossier Generator
        ├── pest_radar.py      # Spatial GPS Pest Surveillance & Proximity Engine
        ├── soil_advisor.py    # NPK Stoichiometric Soil Fertilizer Model
        └── weather.py         # Open-Meteo Geocoding & Spray Feasibility Model
```

---

## ⚡ Installation & Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/farmers-ai.git
cd farmers-ai/Farmers
```

### 2. Create and Activate Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux / macOS
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Copy `.env.example` to `.env` and enter your API keys and SMTP credentials:
```bash
cp .env.example .env
```
Edit `.env`:
```env
GEMINI_API_KEY="your_primary_gemini_api_key"
GEMINI_API_KEY_2="your_secondary_gemini_api_key"

SMTP_SERVER="smtp.gmail.com"
SMTP_PORT=587
SMTP_USER="your_email@gmail.com"
SMTP_PASS="your_16_char_google_app_password"
DEFAULT_SENDER="your_email@gmail.com"
```

### 5. Launch the Application
```bash
streamlit run app.py
```
Open your browser and navigate to: **`http://localhost:8501`**

---

## 🔒 Security & AI Safety Compliance

- **CIB&RC Central Insecticides Board Compliance:** Automated screening of chemical recommendations against banned pesticide registries.
- **Fail-Safe Offline Mode:** If external LLM connectivity drops, the system falls back to on-device expert rules and cached agronomic knowledge.
- **Sanitized Auth & SQL Defense:** Parameterized SQLite queries preventing SQL injection, SHA-256 hashed passwords, and strict RFC email/phone regex filters.

---

## 👥 Contributors & Hackathon Team
- **Project Lead & AI Developer:** Hackathon Innovation Team
- **Built for:** National Agricultural AI Hackathon 2026

⭐ *Empowering smallholder farmers with artificial intelligence from soil to market.*

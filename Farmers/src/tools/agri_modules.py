import math
from datetime import datetime, timedelta
from typing import List, Dict, Any

# --- 1. DYNAMIC STATE & CENTRAL GOVERNMENT SCHEMES ---
def get_dynamic_schemes(acres: float, state: str = "National / State Portal", crop: str = "Tomato") -> List[Dict[str, Any]]:
    """
    Dynamically routes Central and State-specific welfare schemes based on 
    farmer landholding, detected state, and cultivated crop.
    """
    category = "Small & Marginal Farmer (SF/MF, ≤ 5 Acres)" if acres <= 5.0 else "Medium & Large Landholder (> 5 Acres)"
    state_clean = state.lower()
    
    # 1. Universal Central Schemes
    schemes_db = [
        {
            "name": "PM-KISAN (Pradhan Mantri Kisan Samman Nidhi)",
            "authority": "Ministry of Agriculture & Farmers Welfare, Govt of India",
            "benefit": "₹6,000 / year direct income support deposited in 3 equal installments of ₹2,000.",
            "eligibility": f"Eligible: Applicable for your {acres} acre landholding ({category}). Requires active land title (ROR/Patta) and Aadhaar-linked DBT bank account.",
            "step_by_step_process": [
                "Visit the official PM-KISAN portal (pmkisan.gov.in) or nearest Common Service Center (CSC).",
                "Navigate to 'Farmers Corner' > 'New Farmer Registration' and enter your Aadhaar and mobile number.",
                "Provide land record details (Khata / Survey Number / Area in Acres) and active bank details.",
                "Local Village Revenue Officer / Nodal Officer completes field verification.",
                "Funds are credited directly through the Public Financial Management System (PFMS)."
            ],
            "required_docs": "Aadhaar Card, Land Record Passbook (Pattadar / ROR / 1B), DBT-enabled Bank Account.",
            "portal_url": "https://pmkisan.gov.in"
        },
        {
            "name": "Pradhan Mantri Fasal Bima Yojana (PMFBY Comprehensive Crop Insurance)",
            "authority": "MoA&FW & Empaneled General Insurance Companies",
            "benefit": f"Financial compensation against non-preventable natural risks, drought, floods, and pest epidemics for {crop}.",
            "eligibility": f"Available for all farmers cultivating notified crops ({crop}) in notified areas.",
            "step_by_step_process": [
                "Enroll via the PMFBY portal (pmfby.gov.in), local bank branch, or CSC before the seasonal cut-off date.",
                "Loanee farmers are automatically enrolled through their Kisan Credit Card (KCC) limit.",
                "Submit sowing certificate / crop registration slip along with land ownership / tenancy agreement.",
                "Pay nominal farmer premium (1.5% for Rabi, 2% for Kharif, 5% for commercial/horticultural crops).",
                "In case of localized disaster or pest damage, submit claim notification on the Crop Insurance App within 72 hours."
            ],
            "required_docs": "Land Record / Tenancy Certificate, Sowing Declaration, Bank Passbook, Aadhaar.",
            "portal_url": "https://pmfby.gov.in"
        },
        {
            "name": "Kisan Credit Card (KCC) Subsidized Working Capital Loan",
            "authority": "Reserve Bank of India (RBI) & NABARD",
            "benefit": "Revolving credit limit up to ₹3,00,000 at an effective interest rate of 4% per annum (with prompt 3% subvention).",
            "eligibility": f"All owner-cultivators, tenant farmers, oral lessees, and SHGs cultivating {acres} acres.",
            "step_by_step_process": [
                "Obtain the standard one-page KCC application form from any commercial, rural, or cooperative bank.",
                "Submit land ownership documents showing cultivation area and proposed crop pattern.",
                "Bank assesses credit limit based on the district scale of finance plus 10% for post-harvest / household consumption.",
                "Receive RuPay KCC card to withdraw funds directly at ATMs and input dealer PoS terminals."
            ],
            "required_docs": "Land Title Deeds (Pattadar / 1B / Khasra-Khatauni), Identity Proof (Aadhaar / Voter ID), PAN Card.",
            "portal_url": "https://www.nabard.org"
        },
        {
            "name": "PM Krishi Sinchayee Yojana (PMKSY - Per Drop More Crop)",
            "authority": "Central & State Horticulture / Agriculture Departments",
            "benefit": f"{'Up to 90% direct subsidy' if acres <= 5.0 else 'Up to 70% direct subsidy'} on inline drip and micro-sprinkler irrigation systems.",
            "eligibility": f"Applicable for {acres} acres having an operational borewell, open well, or canal lift irrigation source.",
            "step_by_step_process": [
                "Register online on the State Micro Irrigation Project portal or at the District Horticulture Office.",
                "Field technical officer conducts GPS survey of the plot and generates a CAD water-discharge design.",
                "Deposit the non-subsidized farmer share (10% to 30%) via online treasury challan / DD.",
                "Empaneled manufacturer executes installation with warranty and agronomic training."
            ],
            "required_docs": "Land Passbook, Water Source Certificate / Electricity Bill, Aadhaar, Passport Photograph.",
            "portal_url": "https://pmksy.gov.in"
        }
    ]

    # 2. State-Specific Custom Routing
    if any(k in state_clean for k in ["andhra", "ap"]):
        schemes_db.insert(1, {
            "name": "YSR Rythu Bharosa / AP Input Assistance",
            "authority": "Department of Agriculture, Govt of Andhra Pradesh",
            "benefit": "₹13,500 / year financial aid for quality seeds, fertilizers, and farm operations (in 3 seasonal tranches).",
            "eligibility": f"All landholding farmers and eligible ROFR / CCRC tenant farmers in Andhra Pradesh.",
            "step_by_step_process": [
                "Complete seasonal crop booking via e-Crop (e-Panta) digital survey through your local Rythu Bharosa Kendra (RBK).",
                "Verify inclusion in the social audit beneficiary list published at the Village Secretariat.",
                "Funds are credited directly to Aadhaar-seeded accounts via DBT."
            ],
            "required_docs": "Aadhaar Card, e-Crop Acknowledgment, Land Pattadar Passbook / CCRC Card.",
            "portal_url": "https://ysrrythubharosa.ap.gov.in"
        })
    elif any(k in state_clean for k in ["telangana", "ts"]):
        schemes_db.insert(1, {
            "name": "Rythu Bandhu & Rythu Bima Direct Support",
            "authority": "Department of Agriculture, Govt of Telangana",
            "benefit": "₹10,000 / acre / year input investment support + ₹5.00 Lakh comprehensive farmer life insurance.",
            "eligibility": "All pattadar farmers registered on the Dharani Integrated Land Records Management Portal.",
            "step_by_step_process": [
                "Ensure land passbook data is verified and updated on the Dharani portal.",
                "Submit bank account linking confirmation to the local Agriculture Extension Officer (AEO).",
                "Financial assistance is deposited before the onset of Vanakalam and Yasangi seasons."
            ],
            "required_docs": "Dharani Pattadar Passbook, Aadhaar Card, Bank Passbook.",
            "portal_url": "https://dharani.telangana.gov.in"
        })
    elif any(k in state_clean for k in ["maharashtra", "mh"]):
        schemes_db.insert(1, {
            "name": "Namo Shetkari Mahasanman Nidhi Yojana",
            "authority": "Department of Agriculture, Govt of Maharashtra",
            "benefit": "Additional ₹6,000 / year state cash incentive (combined total of ₹12,000 with PM-KISAN).",
            "eligibility": "All farmers in Maharashtra registered and verified under the PM-KISAN database.",
            "step_by_step_process": [
                "Ensure active e-KYC status and land record seeding on the MahaDBT farmer portal.",
                "State installments are disbursed automatically matching PM-KISAN installment schedules."
            ],
            "required_docs": "Aadhaar Card, 7/12 & 8A Land Extracts, Linked Bank Account.",
            "portal_url": "https://mahadbt.maharashtra.gov.in"
        })
    elif any(k in state_clean for k in ["karnataka", "ka"]):
        schemes_db.insert(1, {
            "name": "Krishi Bhagya Scheme (Farm Ponds & Polyhouses)",
            "authority": "Department of Agriculture, Govt of Karnataka",
            "benefit": "Up to 80%-90% financial subsidy for farm ponds, diesel/solar pump sets, and shade nets.",
            "eligibility": "Dryland and rainfed farmers across all agro-climatic zones in Karnataka.",
            "step_by_step_process": [
                "Submit application via the Karnataka FRUITS (Farmer Registration & Unified Beneficiary Information System) portal.",
                "Assistant Director of Agriculture (ADA) verifies land feasibility and sanctions work order."
            ],
            "required_docs": "FRUITS ID, Land RTC / Pahani, Aadhaar Card, Bank Account Details.",
            "portal_url": "https://fruits.karnataka.gov.in"
        })
    elif any(k in state_clean for k in ["punjab", "pb", "haryana", "hr"]):
        schemes_db.insert(1, {
            "name": "Crop Residue Management (CRM) Machinery Subsidy",
            "authority": "Department of Agriculture & Farmers Welfare (Punjab / Haryana)",
            "benefit": "50% individual subsidy (80% for Custom Hiring Centers) on Happy Seeders, Super Seeders, and Mulchers.",
            "eligibility": "All landholders and farmer producer organizations (FPOs).",
            "step_by_step_process": [
                "Apply online on the State Agricultural Mechanization Portal (agrimachinerypb.com / agriharyana.gov.in).",
                "Purchase approved implements from registered manufacturers post-sanction."
            ],
            "required_docs": "Aadhaar Card, Land Records (Jamabandi / Khasra), Tractor RC, Bank Passbook.",
            "portal_url": "https://agrimachinery.nic.in"
        })

    return schemes_db


# --- 2. MULTI-CROP GROWTH & CROP ACTIVITY CALENDAR ---
def get_crop_calendar(crop: str, sowing_date):
    """
    Generates dynamic stage-by-stage agronomic management schedules 
    based on the specified sowing date across all major crops.
    """
    crop_k = crop.lower().split()[0]
    s_date = datetime.combine(sowing_date, datetime.min.time()) if hasattr(sowing_date, "strftime") else datetime.now()
    
    stages_db = {
        "tomato": [
            ("Basal Land Preparation & Bed Formation", s_date, "Apply FYM 10t/ha + SSP 150kg/ha + Chlorpyrifos dust against cutworms."),
            ("Seedling Transplanting & Staking", s_date + timedelta(days=22), "Transplant 25-day healthy seedlings; erect support stakes and install drip lines."),
            ("Vegetative Top-Dressing & Weeding", s_date + timedelta(days=40), "Apply Urea @ 30kg/acre + Boron foliar spray (1g/L) for vegetative vigor."),
            ("Flowering & Fruit Setting Phase", s_date + timedelta(days=60), "Spray Planofix @ 0.25ml/L to arrest flower drop; apply 13-0-45 potassium nitrate."),
            ("First Harvesting Pick", s_date + timedelta(days=80), "Harvest at breaker/pink stage for commercial mandi logistics.")
        ],
        "rice": [
            ("Nursery Sowing & Seed Treatment", s_date, "Treat seeds with Carbendazim 2g/kg; maintain 2cm shallow water depth."),
            ("Main Field Transplanting", s_date + timedelta(days=25), "Plant 2-3 seedlings/hill; apply basal DAP 50kg + MOP 20kg/acre."),
            ("Active Tillering & Weed Management", s_date + timedelta(days=45), "Apply top-dressing Urea @ 35kg/acre; maintain intermittent field wetting."),
            ("Panicle Initiation & Booting", s_date + timedelta(days=70), "Apply balance Potash @ 20kg/acre; prophylactic Tricyclazole spray against blast."),
            ("Physiological Maturity & Harvest", s_date + timedelta(days=115), "Drain standing water 10 days prior; harvest when 85% grains turn golden.")
        ],
        "wheat": [
            ("Field Preparation & Sowing (CRI Stage)", s_date, "Sow certified seed with Seed-cum-Fertilizer drill; basal DAP 50kg + Urea 25kg/acre."),
            ("Crown Root Initiation (1st Irrigation)", s_date + timedelta(days=21), "Critical irrigation window; apply top-dressing Urea @ 40kg/acre."),
            ("Tillering & Jointing Phase", s_date + timedelta(days=45), "Execute broadleaf weed control with 2,4-D or Metsulfuron methyl."),
            ("Flowering & Heading Stage", s_date + timedelta(days=75), "Light irrigation; spray Propiconazole @ 1ml/L if yellow rust symptoms appear."),
            ("Dough Stage & Grain Ripening", s_date + timedelta(days=110), "Terminal maturity; harvest with combine harvester when moisture drops below 14%.")
        ],
        "cotton": [
            ("Sowing & Seed Treatment", s_date, "Seed treatment with Imidacloprid 5g/kg; basal DAP 50kg + MOP 25kg/acre."),
            ("Gap Filling & Square Initiation", s_date + timedelta(days=35), "Thin seedlings to 1 plant/hill; top-dress Urea 35kg/acre."),
            ("Peak Flowering & Boll Setting", s_date + timedelta(days=70), "Install pheromone traps (5/acre); foliar spray of 19:19:19 + Boron 1g/L."),
            ("Boll Development & Protection", s_date + timedelta(days=105), "Monitor for Pink Bollworm; spray Emamectin Benzoate 5% SG @ 0.5g/L."),
            ("Boll Bursting & First Picking", s_date + timedelta(days=135), "Pick clean dry bolls during sunny morning hours.")
        ],
        "chilli": [
            ("Nursery Transplanting", s_date, "Transplant 35-day seedlings on raised beds; apply basal FYM + DAP 50kg/acre."),
            ("Vegetative Branching", s_date + timedelta(days=30), "Top-dress Urea 25kg + MOP 15kg/acre; install blue/yellow sticky traps."),
            ("Flowering & Fruit Induction", s_date + timedelta(days=60), "Spray Micronutrient mixture (Multiplex @ 2.5ml/L) + Planofix @ 0.2ml/L."),
            ("Pod Elongation & Sucking Pest Care", s_date + timedelta(days=90), "Spray Spiromesifen 22.9 SC @ 1ml/L for mite control; maintain moist root zone."),
            ("Multi-Pick Harvesting", s_date + timedelta(days=120), "Periodic picking of green/red ripe chillies every 15 days.")
        ],
        "groundnut": [
            ("Sowing & Rhizobium Inoculation", s_date, "Treat seed with Rhizobium + Trichoderma; apply Gypsum @ 100kg/acre as basal."),
            ("Vegetative Weeding & Intercultivation", s_date + timedelta(days=25), "Light hoeing; avoid soil disturbance once pegging commences."),
            ("Peak Flowering & Pegging Stage", s_date + timedelta(days=50), "Apply 2nd dose of Gypsum @ 100kg/acre around root zone for pod development."),
            ("Pod Filling Phase", s_date + timedelta(days=80), "Ensure adequate soil moisture; monitor for leaf spot / Tikka disease."),
            ("Pod Maturity & Harvesting", s_date + timedelta(days=105), "Pull out vines when inner shell turns blackish-brown; dry pods to 8% moisture.")
        ],
        "maize": [
            ("Sowing & Basal Nutrients", s_date, "Sow seeds at 60x20cm spacing; basal DAP 50kg + Zinc Sulphate 10kg/acre."),
            ("Knee-High Stage (V6)", s_date + timedelta(days=30), "Top-dress Urea @ 35kg/acre; monitor for Fall Armyworm (FAW) in leaf whorls."),
            ("Tasseling & Silking Stage", s_date + timedelta(days=55), "Critical water stage; avoid moisture stress; spray Emamectin if FAW persists."),
            ("Grain Filling & Dough Stage", s_date + timedelta(days=80), "Top-dress MOP 15kg/acre; maintain soil moisture for cob weight."),
            ("Cob Maturity & Harvesting", s_date + timedelta(days=105), "Harvest when husk leaves turn straw yellow and grain black layer forms.")
        ]
    }
    
    return stages_db.get(crop_k, [
        ("Land Preparation & Basal Sowing", s_date, "Apply recommended basal NPK fertilizer mix + organic compost."),
        ("Vegetative Growth & Weeding", s_date + timedelta(days=30), "Timely weeding, intercultivation, and nitrogen top-dressing."),
        ("Flowering / Reproductive Window", s_date + timedelta(days=60), "Maintain moisture balance; apply protective foliar micronutrients."),
        ("Harvesting & Post-Harvest Handling", s_date + timedelta(days=95), "Harvest at physiological crop maturity; sun-dry to safe storage moisture.")
    ])


# --- 3. FAO-56 SMART IRRIGATION & PUMP RUNTIME ENGINE ---
def calculate_irrigation(
    crop: str, 
    growth_stage: str = "Vegetative Growth", 
    acres: float = 2.0, 
    pump_hp: float = 5.0, 
    temp_c: float = 30.0, 
    humidity_pct: float = 55.0, 
    wind_speed_kmh: float = 12.0, 
    rain_mm_forecast: float = 0.0, 
    irrigation_method: str = "Drip Irrigation (90% Efficiency)"
) -> Dict[str, Any]:
    """
    Computes precise daily crop water requirement and motor runtime 
    following FAO-56 Penman-Monteith Evapotranspiration standards.
    """
    # 1. FAO-56 Reference Evapotranspiration (ET0) approximation
    et0_daily = 0.0023 * (temp_c + 17.8) * math.sqrt(max(temp_c - 18.0, 4.0)) * (1.0 + (wind_speed_kmh / 120.0) - (humidity_pct / 220.0))
    et0_daily = max(2.5, min(et0_daily, 8.5))
    
    # 2. Stage-Specific Crop Coefficients (Kc)
    kc_table = {
        "tomato": {"Seedling / Nursery (0-20d)": 0.60, "Vegetative Growth (20-45d)": 0.85, "Flowering & Fruit Setting (45-75d)": 1.15, "Maturity & Harvesting (75-110d)": 0.80},
        "groundnut": {"Seedling / Emergence (0-20d)": 0.40, "Vegetative Growth (20-45d)": 0.80, "Flowering & Pegging (45-70d)": 1.10, "Maturity & Pod Fill (70-105d)": 0.65},
        "chilli": {"Seedling / Nursery (0-25d)": 0.60, "Vegetative Growth (25-50d)": 0.85, "Flowering & Fruit Setting (50-80d)": 1.10, "Maturity & Picking (80-120d)": 0.85},
        "cotton": {"Seedling / Emergence (0-25d)": 0.45, "Vegetative Growth (25-55d)": 0.75, "Square & Boll Formation (55-100d)": 1.20, "Boll Bursting / Picking (100-150d)": 0.65},
        "maize": {"Seedling / Emergence (0-20d)": 0.50, "Vegetative Growth (20-50d)": 0.85, "Tasseling & Silking (50-75d)": 1.20, "Maturity / Grain Fill (75-105d)": 0.75},
        "rice": {"Seedling / Nursery (0-25d)": 1.10, "Tillering Stage (25-50d)": 1.15, "Panicle & Flowering (50-80d)": 1.30, "Maturity & Grain Fill (80-115d)": 0.95},
        "wheat": {"CRI & Seedling (0-25d)": 0.45, "Tillering & Jointing (25-60d)": 0.85, "Flowering & Heading (60-85d)": 1.15, "Grain Ripening (85-115d)": 0.65}
    }
    
    crop_k = crop.lower().split()[0]
    stages = kc_table.get(crop_k, {"Seedling": 0.5, "Vegetative Growth": 0.85, "Flowering": 1.15, "Maturity": 0.75})
    kc = stages.get(growth_stage, 0.90)
    
    # 3. Crop Evapotranspiration (ETc = ET0 * Kc)
    etc_mm_day = et0_daily * kc
    
    # 4. Effective Rainfall Credit
    effective_rain_mm = rain_mm_forecast * 0.75
    net_depth_mm = max(0.0, etc_mm_day - effective_rain_mm)
    
    # 5. Application Efficiency
    eff_map = {
        "Drip Irrigation (90% Efficiency)": 0.90,
        "Sprinkler Irrigation (75% Efficiency)": 0.75,
        "Furrow / Flood Irrigation (55% Efficiency)": 0.55
    }
    efficiency = eff_map.get(irrigation_method, 0.90)
    gross_depth_mm = net_depth_mm / efficiency
    
    # 6. Physical Water Volume & Pump Hours
    liters_per_day = int(gross_depth_mm * 4046.86 * acres)
    pump_discharge_lph = max(pump_hp, 1.0) * 12000.0
    runtime_hours = round(liters_per_day / pump_discharge_lph, 2)
    runtime_mins = int(runtime_hours * 60)
    
    hrs_disp = runtime_mins // 60
    mins_disp = runtime_mins % 60
    kwh_power = round(pump_hp * 0.746 * runtime_hours, 2)
    
    return {
        "et0_mm": round(et0_daily, 2),
        "kc_value": kc,
        "etc_mm": round(etc_mm_day, 2),
        "net_depth_mm": round(net_depth_mm, 2),
        "liters_per_day": liters_per_day,
        "liters_per_acre": int(liters_per_day / max(acres, 0.1)),
        "pump_runtime_hours": runtime_hours,
        "runtime_formatted": f"{hrs_disp} hrs {mins_disp} mins",
        "power_kwh": kwh_power,
        "efficiency_pct": int(efficiency * 100),
        "rain_deduction_mm": round(effective_rain_mm, 1),
        "recommendation": f"Operate your {pump_hp} HP pump for {hrs_disp}h {mins_disp}m today during early morning or evening."
    }


# --- 4. COMPREHENSIVE COST OF CULTIVATION & PROFIT ENGINE (CACP STANDARD) ---
def get_regional_crop_cost_benchmarks(crop: str, state: str = "Andhra Pradesh") -> Dict[str, Any]:
    """
    Returns itemized baseline cost benchmarks per acre (₹/acre) and typical yield ranges (Quintals/acre).
    Adjusts labor and machinery rates based on regional wage indices.
    """
    # Wage factor based on region
    wage_mult = 1.15 if any(s in state.lower() for s in ["kerala", "punjab", "haryana"]) else (0.90 if any(s in state.lower() for s in ["bihar", "odisha", "up", "uttar"]) else 1.0)
    
    benchmarks = {
        "tomato": {
            "avg_yield_q": 160.0,
            "yield_range": (120, 220),
            "seed_nursery_cost": 6500,
            "machinery_plough_cost": int(5500 * wage_mult),
            "fertilizer_pesticide_cost": 14000,
            "labour_harvest_cost": int(15000 * wage_mult),
            "irrigation_electricity_cost": 2500,
            "transport_packaging_cost": 4500
        },
        "paddy / rice": {
            "avg_yield_q": 25.0,
            "yield_range": (20, 32),
            "seed_nursery_cost": 2200,
            "machinery_plough_cost": int(6000 * wage_mult),
            "fertilizer_pesticide_cost": 6500,
            "labour_harvest_cost": int(8500 * wage_mult),
            "irrigation_electricity_cost": 1800,
            "transport_packaging_cost": 2000
        },
        "cotton": {
            "avg_yield_q": 12.0,
            "yield_range": (8, 16),
            "seed_nursery_cost": 3800,
            "machinery_plough_cost": int(5000 * wage_mult),
            "fertilizer_pesticide_cost": 8500,
            "labour_harvest_cost": int(11000 * wage_mult),
            "irrigation_electricity_cost": 1500,
            "transport_packaging_cost": 1800
        },
        "chilli": {
            "avg_yield_q": 18.0,
            "yield_range": (12, 24),
            "seed_nursery_cost": 8000,
            "machinery_plough_cost": int(6000 * wage_mult),
            "fertilizer_pesticide_cost": 18000,
            "labour_harvest_cost": int(19000 * wage_mult),
            "irrigation_electricity_cost": 2800,
            "transport_packaging_cost": 3500
        },
        "groundnut": {
            "avg_yield_q": 14.0,
            "yield_range": (10, 18),
            "seed_nursery_cost": 5500,
            "machinery_plough_cost": int(4500 * wage_mult),
            "fertilizer_pesticide_cost": 4800,
            "labour_harvest_cost": int(7200 * wage_mult),
            "irrigation_electricity_cost": 1500,
            "transport_packaging_cost": 1500
        },
        "maize": {
            "avg_yield_q": 28.0,
            "yield_range": (22, 35),
            "seed_nursery_cost": 3200,
            "machinery_plough_cost": int(4800 * wage_mult),
            "fertilizer_pesticide_cost": 6200,
            "labour_harvest_cost": int(5500 * wage_mult),
            "irrigation_electricity_cost": 1500,
            "transport_packaging_cost": 1800
        },
        "wheat": {
            "avg_yield_q": 20.0,
            "yield_range": (16, 26),
            "seed_nursery_cost": 2400,
            "machinery_plough_cost": int(4500 * wage_mult),
            "fertilizer_pesticide_cost": 4500,
            "labour_harvest_cost": int(5000 * wage_mult),
            "irrigation_electricity_cost": 1400,
            "transport_packaging_cost": 1500
        }
    }

    # Match key
    crop_clean = crop.lower()
    for k, v in benchmarks.items():
        if k in crop_clean or crop_clean.split()[0] in k:
            return v

    return benchmarks["tomato"]

def forecast_yield_and_profit_advanced(
    crop: str, 
    acres: float, 
    expected_price_per_q: float,
    custom_yield_q_per_acre: float = None,
    seeds_cost_per_acre: float = None,
    machinery_cost_per_acre: float = None,
    fertilizer_pesticides_per_acre: float = None,
    labour_harvesting_per_acre: float = None,
    transport_other_per_acre: float = None,
    state: str = "Andhra Pradesh"
) -> Dict[str, Any]:
    """
    Computes itemized Cost of Cultivation (A2 + FL), Gross Revenue, Net Profit,
    Production Cost per Quintal, and Return on Investment (ROI %).
    """
    defaults = get_regional_crop_cost_benchmarks(crop, state)
    
    yield_per_acre = custom_yield_q_per_acre if custom_yield_q_per_acre is not None else defaults["avg_yield_q"]
    c_seed = seeds_cost_per_acre if seeds_cost_per_acre is not None else defaults["seed_nursery_cost"]
    c_machine = machinery_cost_per_acre if machinery_cost_per_acre is not None else defaults["machinery_plough_cost"]
    c_fert_pest = fertilizer_pesticides_per_acre if fertilizer_pesticides_per_acre is not None else defaults["fertilizer_pesticide_cost"]
    c_labour = labour_harvesting_per_acre if labour_harvesting_per_acre is not None else defaults["labour_harvest_cost"]
    c_misc = transport_other_per_acre if transport_other_per_acre is not None else (defaults["irrigation_electricity_cost"] + defaults["transport_packaging_cost"])
    
    cost_per_acre_total = c_seed + c_machine + c_fert_pest + c_labour + c_misc
    total_cost = int(cost_per_acre_total * acres)
    
    total_yield_quintals = round(yield_per_acre * acres, 1)
    gross_revenue = int(total_yield_quintals * expected_price_per_q)
    net_profit = gross_revenue - total_cost
    
    cost_per_quintal = round(total_cost / max(total_yield_quintals, 0.1), 1)
    roi_percent = round((net_profit / max(total_cost, 1)) * 100, 1)
    benefit_cost_ratio = round(gross_revenue / max(total_cost, 1), 2)
    
    return {
        "crop": crop,
        "acres": acres,
        "total_yield_quintals": total_yield_quintals,
        "yield_per_acre": yield_per_acre,
        "cost_breakdown_per_acre": {
            "seeds_nursery": int(c_seed),
            "machinery_ploughing": int(c_machine),
            "fertilizers_chemicals": int(c_fert_pest),
            "human_labour": int(c_labour),
            "irrigation_transport_misc": int(c_misc)
        },
        "total_cost_per_acre": int(cost_per_acre_total),
        "total_cost_all_acres": total_cost,
        "gross_revenue": gross_revenue,
        "net_profit": net_profit,
        "cost_of_production_per_q": cost_per_quintal,
        "roi_percent": roi_percent,
        "bcr": benefit_cost_ratio
    }

def forecast_yield_and_profit(crop: str, acres: float, expected_price_per_q: float):
    """Backward-compatible wrapper."""
    res = forecast_yield_and_profit_advanced(crop, acres, expected_price_per_q)
    return {
        "expected_yield_quintals": res["total_yield_quintals"],
        "total_cost": res["total_cost_all_acres"],
        "gross_revenue": res["gross_revenue"],
        "net_profit": res["net_profit"]
    }


# --- 5. DYNAMIC GEOCODED SERVICE LOCATOR ---
def get_dynamic_service_centers(lat: float = None, lon: float = None, village_name: str = "Regional Hub"):
    """
    Dynamically routes farmers to local extension centers and national support helplines.
    """
    v_clean = village_name.split(",")[0].strip()
    return [
        {
            "name": f"{v_clean} Rythu Bharosa / Farmer Service Hub",
            "type": "Primary Agriculture Service Hub",
            "distance": "Local Village / Block Level",
            "contact": "Kisan Toll-Free Helpline: 1800-180-1551",
            "services": "Subsidized certified seeds, fertilizer e-PoS booking, soil testing collection, e-Crop registration"
        },
        {
            "name": f"Krishi Vigyan Kendra (KVK - ICAR Hub)",
            "type": "Agricultural Research & Extension Center",
            "distance": "District Headquarters",
            "contact": "Toll Free: 155251",
            "services": "On-call plant pathologist consultation, soil health card verification, bio-fertilizer distribution"
        },
        {
            "name": f"{v_clean} Custom Hiring Center (CHC)",
            "type": "Farm Mechanization & Machinery Rental",
            "distance": "Block Command Area",
            "contact": "Direct Block Agri Officer / CHC App",
            "services": "Tractor rotavators, laser land levelers, multi-crop threshers, and agricultural drone spraying services"
        }
    ]
"""
Kisan Mitra - Natural Bio-Pesticides & ZBNF Formulation Engine
Grounded in ICAR & Subhash Palekar Natural Farming (SPNF/ZBNF) agronomic standards.
"""

from typing import Dict, List, Any

NATURAL_FORMULATIONS: Dict[str, Dict[str, Any]] = {
    "neemastra": {
        "id": "neemastra",
        "name": {
            "en": "🍃 Neemastra (Neem Extract Formulation)",
            "te": "🍃 నీమాస్త్రం (రసం పీల్చే పురుగుల నివారణ)",
            "hi": "🍃 नीमास्त्र (रस चूसक कीट नियंत्रक)",
            "ta": "🍃 வேப்ப அஸ்திரம் (சாறு உறிஞ்சும் பூச்சிகள்)",
            "kn": "🍃 ನೀಮಾಸ್ತ್ರ (ರಸ ಹೀರುವ ಕೀಟಗಳ ನಿಯಂತ್ರಣ)",
            "mr": "🍃 निमास्त्र (रस शोषक कीड नियंत्रक)"
        },
        "target_pests": "Sucking pests, Aphids, Jassids, Whiteflies, Thrips, Mites, Small caterpillars.",
        "target_crops": ["Cotton", "Chilli", "Tomato", "Paddy / Rice", "Groundnut", "Pulses", "Vegetables"],
        "base_unit": "1 Acre (200 Litres Spray Solution)",
        "base_ingredients": {
            "Water": {"qty": 200.0, "unit": "Litres"},
            "Desi Cow Urine (Gomutra)": {"qty": 5.0, "unit": "Litres"},
            "Fresh Desi Cow Dung": {"qty": 5.0, "unit": "kg"},
            "Crushed Neem Leaves / Pulp": {"qty": 5.0, "unit": "kg"}
        },
        "fermentation_days": "48 Hours (2 Days)",
        "shelf_life": "6 Months (keep covered in shade)",
        "application_method": "Filter with fine cotton cloth and spray directly without additional dilution.",
        "steps": [
            "Take 200 Litres of clean water in a plastic drum / barrel.",
            "Add 5 kg of fresh Desi cow dung and 5 Litres of cow urine, mixing thoroughly with a wooden stick.",
            "Crush 5 kg of fresh neem leaves into a fine paste and add to the barrel.",
            "Stir the mixture clockwise for 2-3 minutes.",
            "Cover the barrel with a breathable jute bag and store in shade for 48 hours.",
            "Stir twice daily (morning & evening) during fermentation.",
            "Filter thoroughly using a double-layered cotton cloth before filling your knapsack sprayer."
        ],
        "spray_schedule": "Preventive spray every 12-15 days during vegetative and flowering stages."
    },
    "agniastra": {
        "id": "agniastra",
        "name": {
            "en": "🔥 Agniastra (Caterpillar & Stem Borer Formula)",
            "te": "🔥 అగ్నిఅస్త్రం (కాండం తొలిచే పురుగు & లద్దెపురుగు)",
            "hi": "🔥 आग्नेयास्त्र (तना छेदक व इल्ली नाशक)",
            "ta": "🔥 அக்னி அஸ்திரம் (தண்டு துளைப்பான் & புழுக்கள்)",
            "kn": "🔥 ಅಗ್ನಿಯಾಸ್ತ್ರ (ಕಾಂಡ ಕೊರೆಯುವ ಕೀಟ & ಹುಳು)",
            "mr": "🔥 आग्नेयास्त्र (खोडकिडा व अळी नियंत्रक)"
        },
        "target_pests": "Stem Borer, Leaf Folder, Armyworm, Spodoptera, Green caterpillars.",
        "target_crops": ["Paddy / Rice", "Cotton", "Maize", "Chilli", "Tomato", "Brinjal", "Cabbage"],
        "base_unit": "1 Acre Spray Solution (Extract diluted in 100-150L water)",
        "base_ingredients": {
            "Desi Cow Urine": {"qty": 20.0, "unit": "Litres"},
            "Crushed Neem Leaves Paste": {"qty": 5.0, "unit": "kg"},
            "Spicy Green Chilli Paste": {"qty": 0.5, "unit": "kg (500g)"},
            "Crushed Garlic Paste": {"qty": 0.5, "unit": "kg (500g)"},
            "Native Tobacco Powder / Paste": {"qty": 0.25, "unit": "kg (250g)"}
        },
        "fermentation_days": "Simmer boil + 48 Hours Fermentation",
        "shelf_life": "3 Months in a cool shaded area",
        "application_method": "Mix 2 to 3 Litres of concentrated Agniastra extract in 100 Litres of clean water (20-30 ml/L).",
        "steps": [
            "In an earthen pot or stainless steel container, pour 20 Litres of desi cow urine.",
            "Add crushed neem paste (5kg), spicy green chilli paste (500g), crushed garlic (500g), and tobacco leaf paste (250g).",
            "Simmer on a slow flame until it comes to 4-5 gentle boils.",
            "Remove from heat and let it cool in the shade for 48 hours.",
            "Stir the solution twice daily with a wooden stick.",
            "Filter the concentrated decoction through a fine cloth.",
            "Dilute 2.5 Litres in 100 Litres water per acre for spraying."
        ],
        "spray_schedule": "Apply upon first sighting of leaf fold or borer holes; repeat after 7 days if required."
    },
    "brahmastra": {
        "id": "brahmastra",
        "name": {
            "en": "⚡ Brahmastra (Pod Borer & Bollworm Formula)",
            "te": "⚡ బ్రహ్మాస్త్రం (కాయ తొలిచే పురుగు & శనగపచ్చ పురుగు)",
            "hi": "⚡ ब्रह्मास्त्र (फली छेदक व इल्ली नियंत्रक)",
            "ta": "⚡ பிரம்மாஸ்திரம் (காய் துளைப்பான் & புழுக்கள்)",
            "kn": "⚡ ಬ್ರಹ್ಮಾಸ್ತ್ರ (ಕಾಯಿ ಕೊರೆಯುವ ಹುಳು)",
            "mr": "⚡ ब्रह्मास्त्र (बोंडअळी व शेंग पोखरणारी अळी)"
        },
        "target_pests": "Helicoverpa armigera (Gram pod borer), Pink Bollworm, Fruit borers in Tomato & Brinjal.",
        "target_crops": ["Pulses (Tur/Chana)", "Cotton", "Tomato", "Chilli", "Okra (Bhindi)"],
        "base_unit": "1 Acre Spray Solution (Extract diluted in 100L water)",
        "base_ingredients": {
            "Desi Cow Urine": {"qty": 10.0, "unit": "Litres"},
            "Crushed Neem Leaves": {"qty": 3.0, "unit": "kg"},
            "Custard Apple (Sitaphal) Leaves": {"qty": 2.0, "unit": "kg"},
            "Papaya Leaves": {"qty": 2.0, "unit": "kg"},
            "Pongamia (Karanja / Kanuga) Leaves": {"qty": 2.0, "unit": "kg"},
            "Castor or Guava Leaves": {"qty": 2.0, "unit": "kg"}
        },
        "fermentation_days": "Boil + 48 Hours Fermentation",
        "shelf_life": "6 Months",
        "application_method": "Mix 2 to 2.5 Litres of Brahmastra extract in 100 Litres of clean water per acre.",
        "steps": [
            "Collect leaves from 5 plants that cattle avoid (Neem, Custard apple, Papaya, Karanja, Castor/Guava).",
            "Crush each leaf variety into a rough pulp.",
            "Mix all leaf pastes into 10 Litres of cow urine in an earthen/steel pot.",
            "Boil gently on a slow fire until the solution reduces by approximately 20-25%.",
            "Cool and let it ferment in shade for 48 hours with daily stirring.",
            "Filter through fine mesh and store in airtight containers.",
            "Spray at 20-25 ml per Litre of water (2 to 2.5 L/acre)."
        ],
        "spray_schedule": "Apply at bud initiation and pod/fruit formation stage."
    },
    "dashaparni": {
        "id": "dashaparni",
        "name": {
            "en": "🧪 Dashaparni Kashayam (10-Leaf Broad Spectrum)",
            "te": "🧪 దశపర్ణి కషాయం (సర్వ తెగుళ్ల నివారిణి)",
            "hi": "🧪 दशपर्णी काढ़ा (सर्व रोग एवं कीट निवारक)",
            "ta": "🧪 தசபர்ணி கஷாயம் (அனைத்து பூச்சி தடுப்பு)",
            "kn": "🧪 ದಶಪರ್ಣಿ ಕಷಾಯ (ಸರ್ವ ಕೀಟ ನಾಶಕ)",
            "mr": "🧪 दशपर्णी काढा (सर्वंकष कीड व रोग नियंत्रक)"
        },
        "target_pests": "Broad-spectrum: Blight, Fungal spots, Thrips, Aphids, Mites, Caterpillar outbreaks.",
        "target_crops": ["All Crops", "Paddy / Rice", "Cotton", "Chilli", "Tomato", "Horticulture"],
        "base_unit": "1 Acre Spray Solution (Extract diluted in 200L water)",
        "base_ingredients": {
            "Water": {"qty": 200.0, "unit": "Litres"},
            "Desi Cow Urine": {"qty": 20.0, "unit": "Litres"},
            "Fresh Cow Dung": {"qty": 2.0, "unit": "kg"},
            "10 Types Bitter Leaves (2kg each)": {"qty": 20.0, "unit": "kg total"},
            "Crushed Green Chilli": {"qty": 0.5, "unit": "kg"},
            "Crushed Garlic": {"qty": 0.5, "unit": "kg"},
            "Turmeric Powder": {"qty": 0.5, "unit": "kg"}
        },
        "fermentation_days": "30 to 45 Days Cold Fermentation",
        "shelf_life": "6 Months",
        "application_method": "Dilute 5 to 6 Litres of Dashaparni extract in 200 Litres water per acre.",
        "steps": [
            "In a 200L plastic drum, mix 200L water, 20L cow urine, and 2kg fresh cow dung.",
            "Add crushed leaves of 10 medicinal plants (Neem, Karanja, Custard apple, Papaya, Marigold, Castor, Tulsi, Mango, Calotropis, Guava).",
            "Add crushed chilli, garlic, and turmeric powder.",
            "Cover with a jute bag in shade and let ferment for 30 to 45 days.",
            "Stir clockwise once daily.",
            "Filter the rich herbal liquor and apply at 30 ml per Litre of water."
        ],
        "spray_schedule": "Apply every 20 days as a systemic plant immunity and repellent barrier."
    },
    "sour_buttermilk": {
        "id": "sour_buttermilk",
        "name": {
            "en": "🥛 Sour Buttermilk + Asafoetida (Fungal & Mildew Defense)",
            "te": "🥛 పుల్లటి మజ్జిగ + ఇంగువ (బూడిద తెగులు & శిలీంధ్ర నివారణ)",
            "hi": "🥛 खट्टी छाछ व हींग (फफूंद व पाउडरी मिल्ड्यू नाशक)",
            "ta": "🥛 புளித்த மோர் + பெருங்காயம் (சாம்பல் நோய்)",
            "kn": "🥛 ಹುಳಿ ಮಜ್ಜಿಗೆ + ಇಂಗು (ಶಿಲೀಂಧ್ರ ರೋಗ ನಿಯಂತ್ರಣ)",
            "mr": "🥛 आंबट ताक व हिंग (बुरशी व भुरी रोग नियंत्रक)"
        },
        "target_pests": "Powdery Mildew, Downy Mildew, Leaf Blight, Rust, Damping-off fungal spores.",
        "target_crops": ["Chilli", "Tomato", "Grapes", "Cucurbits", "Paddy / Rice", "Wheat"],
        "base_unit": "1 Acre (150-200 Litres water)",
        "base_ingredients": {
            "Fermented Sour Buttermilk (5-7 days old)": {"qty": 5.0, "unit": "Litres"},
            "Asafoetida (Hing) Powder": {"qty": 0.05, "unit": "kg (50g)"},
            "Clean Water": {"qty": 150.0, "unit": "Litres"}
        },
        "fermentation_days": "5 to 7 Days (for buttermilk souring in earthen/copper pot)",
        "shelf_life": "Use within 2 days after souring",
        "application_method": "Mix 5 Litres sour buttermilk + 50g dissolved Hing in 150 Litres of water and spray.",
        "steps": [
            "Store fresh buttermilk in an earthen pot (optionally insert a clean copper wire/plate) for 5-7 days until it turns very sour and greenish.",
            "Dissolve 50g of pure Hing (asafoetida) powder in 1 litre of warm water.",
            "Mix the sour buttermilk and Hing water into 150 Litres of spraying water.",
            "Filter through a fine cloth and spray on both upper and lower leaf surfaces."
        ],
        "spray_schedule": "Spray at first sign of white powdery patches or yellow blight spots. Repeat after 5 days."
    },
    "jeevamrutha": {
        "id": "jeevamrutha",
        "name": {
            "en": "🌱 Liquid Jeevamrutha (Soil Biology & Plant Booster)",
            "te": "🌱 ద్రవ జీవామృతం (నేల సూక్ష్మజీవుల వర్ధనం & రోగనిరోధక శక్తి)",
            "hi": "🌱 तरल जीवामृत (मृदा जीवाणु व पोषण संवर्धक)",
            "ta": "🌱 திரவ ஜீவாமிர்தம் (மண் நுண்ணுயிர் பெருக்கி)",
            "kn": "🌱 ದ್ರವ ಜೀವಾಮೃತ (ಮಣ್ಣಿನ ಜೀವಾಣು ಉತ್ತೇಜಕ)",
            "mr": "🌱 द्रवरूप जीवामृत (जमीन सुपीकता व सूक्ष्मजीव संवर्धक)"
        },
        "target_pests": "Soil pathogens, Root rot, Nematodes, Poor nutrient uptake, Weak root vigor.",
        "target_crops": ["All Crops", "Paddy / Rice", "Cotton", "Groundnut", "Chilli", "Tomato", "Sugarcane"],
        "base_unit": "1 Acre (200 Litres via Drip or Flood Irrigation / Foliar 10%)",
        "base_ingredients": {
            "Water": {"qty": 200.0, "unit": "Litres"},
            "Fresh Desi Cow Dung": {"qty": 10.0, "unit": "kg"},
            "Desi Cow Urine": {"qty": 5.0, "unit": "Litres"},
            "Organic Jaggery / Cane Juice": {"qty": 1.0, "unit": "kg"},
            "Pulse Flour (Besan / Gram Flour)": {"qty": 1.0, "unit": "kg"},
            "Virgin Forest / Bund Soil": {"qty": 0.1, "unit": "kg (Handful)"}
        },
        "fermentation_days": "48 to 72 Hours (2-3 Days)",
        "shelf_life": "Use within 7 to 10 days of fermentation",
        "application_method": "Apply 200 Litres per acre along with irrigation water, or filter and spray at 10% concentration (100 ml/L).",
        "steps": [
            "Fill a 200L barrel with 200 Litres of fresh water.",
            "Add 10 kg cow dung and 5 Litres cow urine, stirring with a wooden pole.",
            "Dissolve 1 kg jaggery in water and add to barrel (food for aerobic microbes).",
            "Add 1 kg pulse flour (protein source) and a handful of fertile chemical-free bund soil (microbial inoculant).",
            "Stir clockwise for 5 minutes twice a day.",
            "Keep covered under shade for 48-72 hours until a pleasant fermentation aroma develops.",
            "Apply directly through irrigation canal, venturi drip, or as a 10% foliar tonic."
        ],
        "spray_schedule": "Apply every 15-21 days throughout the crop life cycle."
    }
}


def calculate_scaled_formulation(formulation_key: str, acres: float = 1.0, knapsack_pumps: int = None) -> Dict[str, Any]:
    """
    Dynamically scales natural bio-pesticide ingredients based on either 
    farmer acreage or number of 15-litre knapsack spray pumps.
    """
    if formulation_key not in NATURAL_FORMULATIONS:
        formulation_key = "neemastra"
        
    base = NATURAL_FORMULATIONS[formulation_key]
    
    # Scaling factor (default to acreage)
    if knapsack_pumps and knapsack_pumps > 0:
        # Standard: 1 acre requires ~13-14 knapsack pumps of 15L (200L total)
        multiplier = (knapsack_pumps * 15.0) / 200.0
        unit_label = f"{knapsack_pumps} Knapsack Pumps (15L each = {knapsack_pumps*15}L Solution)"
    else:
        multiplier = max(0.25, acres)
        unit_label = f"{acres} Acre(s) Landholding"
        
    scaled_ingredients = {}
    for ing_name, ing_data in base["base_ingredients"].items():
        qty_val = round(ing_data["qty"] * multiplier, 2)
        # Clean display formatting
        if qty_val.is_integer():
            qty_str = f"{int(qty_val)}"
        else:
            qty_str = f"{qty_val}"
            
        scaled_ingredients[ing_name] = {
            "scaled_qty": qty_str,
            "unit": ing_data["unit"]
        }
        
    return {
        "id": base["id"],
        "name": base["name"],
        "unit_label": unit_label,
        "scaled_ingredients": scaled_ingredients,
        "target_pests": base["target_pests"],
        "target_crops": base["target_crops"],
        "fermentation_days": base["fermentation_days"],
        "shelf_life": base["shelf_life"],
        "application_method": base["application_method"],
        "steps": base["steps"],
        "spray_schedule": base["spray_schedule"]
    }


def get_recommendations_by_problem(crop: str = "All Crops", problem_category: str = "All") -> List[Dict[str, Any]]:
    """
    Filters and ranks natural bio-pesticides based on farmer's crop and pest problem.
    """
    matched = []
    
    for key, data in NATURAL_FORMULATIONS.items():
        crop_match = (
            crop == "All Crops" or 
            "All Crops" in data["target_crops"] or 
            any(crop.lower() in c.lower() for c in data["target_crops"])
        )
        
        prob_match = True
        if problem_category == "Sucking Pests (Aphids, Thrips, Whiteflies)":
            prob_match = key in ["neemastra", "dashaparni"]
        elif problem_category == "Caterpillars & Stem Borers":
            prob_match = key in ["agniastra", "dashaparni"]
        elif problem_category == "Pod Borers & Bollworms":
            prob_match = key in ["brahmastra", "agniastra"]
        elif problem_category == "Fungal Diseases, Blight & Mildew":
            prob_match = key in ["sour_buttermilk", "dashaparni"]
        elif problem_category == "Soil Health & Root Vigor Booster":
            prob_match = key in ["jeevamrutha"]
            
        if crop_match and prob_match:
            matched.append(data)
            
    if not matched:
        matched = list(NATURAL_FORMULATIONS.values())
        
    return matched

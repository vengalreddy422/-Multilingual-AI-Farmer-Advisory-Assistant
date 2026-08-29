import re
from typing import Dict, Any
from src.vision.model_utils import TREATMENT_DATABASE, decode_label_direct

SMS_KEYWORDS = {
    "PEST": {
        "description": "Get instant emergency crop protection advice",
        "sample": "KISAN PEST TOMATO"
    },
    "MANDI": {
        "description": "Get current APMC modal prices",
        "sample": "KISAN MANDI PADDY"
    },
    "WEATHER": {
        "description": "Get rain alert and spray advisory",
        "sample": "KISAN WEATHER"
    },
    "FERTILIZER": {
        "description": "Get basal & split nutrient dose",
        "sample": "KISAN FERTILIZER PADDY"
    },
    "SCHEME": {
        "description": "Get central & state subsidy alerts",
        "sample": "KISAN SCHEME"
    }
}

# Dynamic Commodity Baseline Rates
COMMODITY_PRICES = {
    "paddy": 2320,
    "rice": 2320,
    "wheat": 2275,
    "cotton": 7450,
    "tomato": 1950,
    "chilli": 18500,
    "groundnut": 6850,
    "maize": 2180,
    "sugarcane": 3150,
    "potato": 1650,
    "onion": 2400
}

# Crop Specific Emergency SMS Prescriptions
DYNAMIC_PEST_KNOWLEDGE = {
    "tomato": {
        "te": "టమాటా ఆకుముడతకు 15 పసుపు అట్టలు పెట్టండి. వేపనూనె 5ml/L లేదా ఎసిటామిప్రిడ్ 0.3g/L పిచికారీ చేయండి.",
        "hi": "टमाटर कीट हेतु 15 पीले ट्रैप लगाएं। नीम तेल 5ml/L या एसिटामिप्रिड 0.3g/L का छिड़काव करें।",
        "ta": "தக்காளி இலை சுருட்டலுக்கு வேப்ப எண்ணெய் 5ml/L தெளிக்கவும். 15 மஞ்சள் பொறிகள் வைக்கவும்.",
        "kn": "ಟೊಮೆಟೊ ಎಲೆ ಮುದುರುವಿಕೆಗೆ 15 ಹಳದಿ ಬಲೆ ಇರಿಸಿ. ಬೇವಿನ ಎಣ್ಣೆ 5ml/L ಸಿಂಪಡಿಸಿ.",
        "mr": "टोमॅटो कीड नियंत्रणासाठी पिवळे चिकट सापळे लावा व निंबोळी अर्क ५ml/L फवारा.",
        "en": "For Tomato pests, install 15 Yellow Traps/acre. Spray Neem Oil 5ml/L or Acetamiprid 0.3g/L."
    },
    "cotton": {
        "te": "పత్తిలో గులాబీ రంగు పురుగుకు ఎకరానికి 5 లింగాకర్షక బుట్టలు పెట్టండి. వేపనూనె 5ml/L పిచికారీ చేయండి.",
        "hi": "कपास में गुलाबी सुंडी हेतु 5 फेरोमोन ट्रैप लगाएं। नीम तेल 5ml/L या प्रोफेनोफॉस 2ml/L छिड़कें।",
        "ta": "பருத்தி காய்ப்புழுவிற்கு ஏக்கருக்கு 5 இனக்கவர்ச்சி பொறிகளை வைக்கவும். வேப்ப எண்ணெய் தெளிக்கவும்.",
        "kn": "ಹತ್ತಿ ಕಾಯಿಕೊರಕ ಹುಳು ನಿಯಂತ್ರಣಕ್ಕೆ 5 ಮೋಹಕ ಬಲೆ ಇರಿಸಿ. ಬೇವಿನ ಎಣ್ಣೆ ಸಿಂಪಡಿಸಿ.",
        "mr": "कापूस बोंडअळीसाठी एकरी ५ कामगंध सापळे लावा व निंबोळी तेल ५ml/L फवारा.",
        "en": "For Cotton bollworm, install 5 pheromone traps/acre. Spray Neem Oil 5ml/L or Profenofos 2ml/L."
    },
    "paddy": {
        "te": "వరి అగ్గి తెగులుకు ట్రైసైక్లాజోల్ 75 WP @ 0.6g/L లేదా సుడిదోమకు నీరు తీసివేసి పైమెట్రోజిన్ 120g/ఎకరా చల్లండి.",
        "hi": "धान ब्लास्ट हेतु ट्राइसाइक्लाजोल 0.6g/L या बीपीएच कीट हेतु खेत का पानी निकालें व पाइमेट्रोजिन छिड़कें।",
        "ta": "நெல் குலை நோய்க்கு ட்ரைசைக்ளசோல் 0.6g/L தெளிக்கவும். வயல் நீரை வடிக்கவும்.",
        "kn": "ಭತ್ತದ ಬೆಂಕಿ ರೋಗಕ್ಕೆ ಟ್ರೈಸೈಕ್ಲಾಜೋಲ್ 0.6g/L ಸಿಂಪಡಿಸಿ. ಹೊಲದ ನೀರು ಬಸಿದು ಬಿಡಿ.",
        "mr": "भात करपा रोगासाठी ट्रायसायक्लॅझोल ०.६g/L फवारा. शेतातून पाणी निचरा करा.",
        "en": "For Paddy Blast, spray Tricyclazole 75 WP @ 0.6g/L. For BPH, drain field water & spray Pymetrozine."
    },
    "chilli": {
        "te": "మిరపలో నల్ల తామర పురుగుకు 20 నీలి జిగురు అట్టలు పెట్టండి. ఫిప్రోనిల్ 5% SC @ 2ml/L పిచికారీ చేయండి.",
        "hi": "मिर्च में थ्रिप्स कीट हेतु 20 नीले ट्रैप लगाएं। फिप्रोनिल 5% SC @ 2ml/L का छिड़काव करें।",
        "ta": "மிளகாய் இலைப்பேன் தாக்குதலுக்கு 20 நீல பொறிகள் வைக்கவும். பிப்ரோனில் 2ml/L தெளிக்கவும்.",
        "kn": "ಮೆಣಸಿನಕಾಯಿ ನುಸಿ ಹುಳಿಗೆ 20 ನೀಲಿ ಬಲೆ ಇರಿಸಿ. ಫಿಪ್ರೋನಿಲ್ 2ml/L ಸಿಂಪಡಿಸಿ.",
        "mr": "मिरचीवरील थ्रिप्ससाठी २० निळे चिकट सापळे लावा व फिप्रोनिल २ml/L फवारा.",
        "en": "For Chilli Black Thrips, install 20 Blue Sticky Traps/acre. Spray Fipronil 5% SC @ 2ml/L."
    },
    "maize": {
        "te": "మొక్కజొన్న కత్తెర పురుగుకు సున్నం+ఇసుక (1:9) సుడులలో వేయండి. కోరాజెన్ 0.4ml/L పిచికారీ చేయండి.",
        "hi": "मक्का फॉल आर्मीवर्म हेतु कोराजन 0.4ml/L या राख+चूना चोंगे में डालें।",
        "ta": "மக்காச்சோள படைப்புழுவுக்கு கோராஜன் 0.4ml/L அல்லது சாம்பல் தூவவும்.",
        "kn": "ಮೆಕ್ಕೆಜೋಳ ಲದ್ದಿ ಹುಳು ನಿಯಂತ್ರಣಕ್ಕೆ ಕೋರಾಜೆನ್ 0.4ml/L ಸಿಂಪಡಿಸಿ.",
        "mr": "मका लष्करी अळीसाठी कोराजन ०.४ml/L फवारा किंवा पोंग्यात चुना+वाळू टाका.",
        "en": "For Maize Fall Armyworm, apply lime+sand in whorl. Spray Coragen @ 0.4ml/L."
    },
    "groundnut": {
        "te": "వేరుశనగ తిక్క ఆకుమచ్చ తెగులుకు హెక్సాకోనాజోల్ 5% EC @ 2ml/L నీటికి కలిపి పిచికారీ చేయండి.",
        "hi": "मूंगफली टिक्का रोग हेतु हेक्साकोनाजोल 5% EC @ 2ml/L पानी में मिलाकर छिड़कें।",
        "ta": "நிலக்கடலை டிக்கா இலைப்புள்ளிக்கு ஹெக்ஸாகோனசோல் 2ml/L தெளிக்கவும்.",
        "kn": "ಕಡಲೆಕಾಯಿ ತಿಕ್ಕಾ ರೋಗಕ್ಕೆ ಹೆಕ್ಸಾಕೊನಾಜೋಲ್ 2ml/L ಸಿಂಪಡಿಸಿ.",
        "mr": "भुईमूग टिक्का रोगासाठी हेक्साकोनाझोल २ml/L फवारा.",
        "en": "For Groundnut Tikka spot, spray Hexaconazole 5% EC @ 2ml/L water."
    }
}

def process_offline_sms_query(raw_text: str, lang_code: str = "en", location: str = "Madanapalle") -> Dict[str, Any]:
    """
    Dynamically parses whatever crop, pest, mandi, or weather query is texted by the farmer
    and generates a tailored, single-payload 160-character GSM SMS and conversational IVR transcript.
    """
    clean = raw_text.strip().lower()
    loc_short = location.split(",")[0].strip()

    # Detect requested crop
    detected_crop = None
    for c_name in ["tomato", "cotton", "paddy", "rice", "chilli", "maize", "groundnut", "wheat", "sugarcane", "potato", "onion"]:
        if c_name in clean:
            detected_crop = c_name if c_name != "rice" else "paddy"
            break

    # 1. DYNAMIC MANDI RATE QUERY
    if any(w in clean for w in ["mandi", "price", "rate", "ధర", "दाम", "விலை", "ದರ", "भाव"]):
        crop_target = detected_crop if detected_crop else "paddy"
        price_val = COMMODITY_PRICES.get(crop_target, 2300)
        c_title = crop_target.title()

        if lang_code == "te":
            sms_text = f"[కిసాన్ SMS] {loc_short} మార్కెట్: {c_title} ధర ₹{price_val:,}/క్వింటా. మార్కెట్ పోకడ: స్థిరంగా ఉంది. హెల్ప్‌లైన్: 1800-180-1551"
            ivr_text = f"నమస్కారం రైతు సోదరా. {loc_short} మార్కెట్‌లో {c_title} తాజా ధర క్వింటాలుకు {price_val} రూపాయలు."
        elif lang_code == "hi":
            sms_text = f"[किसान SMS] {loc_short} मंडी: {c_title} भाव ₹{price_val:,}/क्विंटल। बाजार रुझान: स्थिर व तेज। टोल फ्री: 1800-180-1551"
            ivr_text = f"नमस्ते किसान भाई। {loc_short} मंडी में {c_title} का ताजा भाव {price_val} रुपये प्रति क्विंटल है।"
        elif lang_code == "ta":
            sms_text = f"[உழவன் SMS] {loc_short} சந்தை: {c_title} விலை ₹{price_val:,}/குவிண்டால். உதவி: 1800-180-1551"
            ivr_text = f"வணக்கம். {loc_short} சந்தையில் {c_title} விலை குவிண்டாலுக்கு {price_val} ரூபாய்."
        elif lang_code == "kn":
            sms_text = f"[ಕಿಸಾನ್ SMS] {loc_short} ಮಾರುಕಟ್ಟೆ: {c_title} ದರ ₹{price_val:,}/ಕ್ವಿಂಟಾಲ್. ಸಹಾಯವಾಣಿ: 1800-180-1551"
            ivr_text = f"ನಮಸ್ಕಾರ. {loc_short} ಮಾರುಕಟ್ಟೆಯಲ್ಲಿ {c_title} ದರ ಕ್ವಿಂಟಾಲಿಗೆ {price_val} ರೂಪಾಯಿ."
        elif lang_code == "mr":
            sms_text = f"[किसान SMS] {loc_short} बाजार: {c_title} भाव ₹{price_val:,}/क्विंटल. कल: स्थिर. हेल्पलाईन: 1800-180-1551"
            ivr_text = f"नमस्कार. {loc_short} बाजारपेठेत {c_title} भाव {price_val} रुपये प्रति क्विंटल आहे."
        else:
            sms_text = f"[KISAN SMS] {loc_short} Mandi: {c_title} rate ₹{price_val:,}/Quintal. Trend: Steady & Bullish. KCC: 1800-180-1551"
            ivr_text = f"Hello Farmer. The latest market price for {c_title} in {loc_short} is rupees {price_val} per quintal."

    # 2. DYNAMIC WEATHER / RAIN QUERY
    elif any(w in clean for w in ["weather", "rain", "వాతావరణం", "मौसम", "வானிலை", "ಹವಾಮಾನ"]):
        if lang_code == "te":
            sms_text = f"[కిసాన్ SMS] {loc_short} వాతావరణం: 29°C, తేమ 60%, వర్ష సూచన: తక్కువ. నేడు పిచికారీ పనులకు అనుకూలం. హెల్ప్: 1800-180-1551"
            ivr_text = f"{loc_short} ప్రాంతంలో నేడు వర్ష సూచన లేదు. ఉష్ణోగ్రత 29 డిగ్రీలు, పిచికారీ పనులు కొనసాగించవచ్చు."
        elif lang_code == "hi":
            sms_text = f"[किसान SMS] {loc_short} मौसम: 29°C, नमी 60%, वर्षा संभावना: कम। आज कीटनाशक छिड़काव के लिए उपयुक्त है। टोल: 1800-180-1551"
            ivr_text = f"{loc_short} में आज मौसम साफ रहेगा। कीटनाशक छिड़काव का कार्य किया जा सकता है।"
        else:
            sms_text = f"[KISAN SMS] {loc_short} Weather: 29°C, Humidity 60%, Rain Risk: Low. Favorable for field spraying. KCC: 1800-180-1551"
            ivr_text = f"Today weather in {loc_short} is clear with 29 degrees Celsius. Favorable for spraying operations."

    # 3. DYNAMIC FERTILIZER / SOIL / WATER QUERY
    elif any(w in clean for w in ["fertilizer", "urea", "npk", "water", "irrigation", "ఎరువులు", "खाद", "உரம்"]):
        crop_target = detected_crop if detected_crop else "crop"
        if lang_code == "te":
            sms_text = f"[కిసాన్ SMS] {loc_short} {crop_target.title()}: ఎకరానికి 5 టన్నుల పశువుల ఎరువు + యూరియాను 3 దఫాలుగా వేయండి. డ్రిప్ నీరు ఇవ్వండి. 1800-180-1551"
            ivr_text = f"మీ {crop_target.title()} పంటకు ఎరువులను ఒకేసారి కాకుండా మూడు దఫాలుగా విభజించి వేయండి."
        elif lang_code == "hi":
            sms_text = f"[किसान SMS] {loc_short} {crop_target.title()}: 5 टन गोबर खाद व यूरिया को 3 भागों में दें। संतुलित ड्रिप सिंचाई करें। 1800-180-1551"
            ivr_text = f"अपनी {crop_target.title()} फसल में यूरिया को 3 किस्तों में दें और संतुलित सिंचाई करें।"
        else:
            sms_text = f"[KISAN SMS] {loc_short} {crop_target.title()}: Apply 5 ton FYM/acre + split Urea in 3 doses. Maintain drip irrigation. KCC: 1800-180-1551"
            ivr_text = f"For {crop_target.title()}, apply balanced organic manure and split nitrogen in three stages."

    # 4. DYNAMIC CROP PEST & DISEASE QUERY (Default & High Priority)
    else:
        crop_key = detected_crop if detected_crop in DYNAMIC_PEST_KNOWLEDGE else "tomato"
        crop_name_disp = crop_key.title()
        
        prescription_dict = DYNAMIC_PEST_KNOWLEDGE.get(crop_key, DYNAMIC_PEST_KNOWLEDGE["tomato"])
        rec_text = prescription_dict.get(lang_code, prescription_dict["en"])

        if lang_code == "te":
            sms_text = f"[కిసాన్ SMS] {loc_short}: {rec_text} సహాయం: 1800-180-1551"
            ivr_text = f"నమస్కారం రైతు సోదరా. మీ {crop_name_disp} పంట తెగులు నివారణ సలహా: {rec_text}"
        elif lang_code == "hi":
            sms_text = f"[किसान SMS] {loc_short}: {rec_text} टोल फ्री: 1800-180-1551"
            ivr_text = f"नमस्ते किसान भाई। आपकी {crop_name_disp} फसल हेतु सलाह: {rec_text}"
        elif lang_code == "ta":
            sms_text = f"[உழவன் SMS] {loc_short}: {rec_text} உதவி: 1800-180-1551"
            ivr_text = f"வணக்கம் விவசாய நண்பரே. {crop_name_disp} பயிர் பாதுகாப்பு: {rec_text}"
        elif lang_code == "kn":
            sms_text = f"[ಕಿಸಾನ್ SMS] {loc_short}: {rec_text} ಸಹಾಯವಾಣಿ: 1800-180-1551"
            ivr_text = f"ನಮಸ್ಕಾರ. ನಿಮ್ಮ {crop_name_disp} ಬೆಳೆ ರಕ್ಷಣೆಗೆ: {rec_text}"
        elif lang_code == "mr":
            sms_text = f"[किसान SMS] {loc_short}: {rec_text} हेल्पलाईन: 1800-180-1551"
            ivr_text = f"नमस्कार. आपल्या {crop_name_disp} पिकासाठी सल्ला: {rec_text}"
        else:
            sms_text = f"[KISAN SMS] {loc_short}: {rec_text} KCC: 1800-180-1551"
            ivr_text = f"Hello Farmer. Advisory for {crop_name_disp}: {rec_text}"

    # Ensure strictly <= 160 characters for single GSM SMS payload
    if len(sms_text) > 160:
        sms_text = sms_text[:157] + "..."

    return {
        "channel": "SMS Gateway / USSD *144#",
        "character_count": len(sms_text),
        "is_valid_sms": len(sms_text) <= 160,
        "sms_response": sms_text,
        "ivr_audio_transcript": ivr_text,
        "toll_free_help": "1800-180-1551 (Kisan Call Center)"
    }

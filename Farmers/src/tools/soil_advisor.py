from typing import Dict, Any

CROP_IDEAL_NPK = {
    "rice": {"N": 100, "P": 40, "K": 40, "pH_range": (5.5, 7.0), "fym_ton": 5.0},
    "paddy": {"N": 100, "P": 40, "K": 40, "pH_range": (5.5, 7.0), "fym_ton": 5.0},
    "wheat": {"N": 120, "P": 60, "K": 40, "pH_range": (6.0, 7.5), "fym_ton": 4.0},
    "maize": {"N": 120, "P": 60, "K": 50, "pH_range": (5.8, 7.0), "fym_ton": 5.0},
    "cotton": {"N": 120, "P": 60, "K": 60, "pH_range": (6.0, 8.0), "fym_ton": 4.0},
    "tomato": {"N": 150, "P": 100, "K": 120, "pH_range": (6.0, 6.8), "fym_ton": 8.0},
    "chilli": {"N": 120, "P": 60, "K": 80, "pH_range": (6.0, 7.5), "fym_ton": 6.0},
    "groundnut": {"N": 25, "P": 50, "K": 40, "pH_range": (6.0, 7.2), "fym_ton": 3.5},
    "sugarcane": {"N": 200, "P": 80, "K": 120, "pH_range": (6.5, 7.8), "fym_ton": 10.0},
    "potato": {"N": 150, "P": 100, "K": 120, "pH_range": (5.2, 6.8), "fym_ton": 8.0},
    "soybean": {"N": 30, "P": 60, "K": 40, "pH_range": (6.0, 7.5), "fym_ton": 4.0}
}

def analyze_soil_npk(crop: str, n: float, p: float, k: float, ph: float) -> Dict[str, Any]:
    crop_lower = crop.strip().lower()
    
    # Fuzzy matching for composite crop names like "Paddy / Rice (వరి / धान)"
    target = None
    for k_key, v in CROP_IDEAL_NPK.items():
        if k_key in crop_lower:
            target = v
            break
            
    if not target:
        target = {"N": 100, "P": 50, "K": 50, "pH_range": (6.0, 7.5), "fym_ton": 5.0}

    advice = []
    
    # Basal Organic Manure Advice
    advice.append(f"🌿 **Organic Base:** Incorporate well-decomposed Farm Yard Manure (FYM) @ {target.get('fym_ton', 5.0)} tons/acre during final land ploughing.")

    # 1. Nitrogen (N)
    if n < target["N"] - 15:
        urea_kg = int(round((target['N'] - n) * 2.17))
        advice.append(f"🌱 **Nitrogen Deficient:** Apply **Urea @ {urea_kg} kg/acre** in 2-3 split doses (50% basal, 25% vegetative, 25% pre-flowering).")
    elif n > target["N"] + 20:
        advice.append("⚠️ **Nitrogen is High:** Reduce synthetic urea to prevent excessive succulent growth and pest flare-ups.")
    else:
        advice.append("✅ **Nitrogen is in the Optimal Range.** Apply standard maintenance top-dressing.")

    # 2. Phosphorus (P)
    if p < target["P"] - 10:
        ssp_kg = int(round((target['P'] - p) * 6.25))
        dap_kg = int(round((target['P'] - p) * 2.17))
        advice.append(f"🧪 **Phosphorus Deficient:** Apply **Single Super Phosphate (SSP) @ {ssp_kg} kg/acre** (or DAP @ {dap_kg} kg/acre) strictly as basal dose at root depth.")
    else:
        advice.append("✅ **Phosphorus Level is Optimal.**")

    # 3. Potassium (K)
    if k < target["K"] - 10:
        mop_kg = int(round((target['K'] - k) * 1.67))
        advice.append(f"🔋 **Potassium Low:** Apply **Muriate of Potash (MOP) @ {mop_kg} kg/acre** in 2 splits to enhance disease resistance and grain/fruit sizing.")
    else:
        advice.append("✅ **Potassium Level is Optimal.**")

    # 4. pH Correction
    ph_min, ph_max = target["pH_range"]
    if ph < ph_min:
        advice.append(f"⚠️ **Acidic Soil (pH {ph:.1f}):** Apply **Agricultural Lime (CaCO3) @ 200-300 kg/acre** 3 weeks prior to sowing.")
    elif ph > ph_max:
        advice.append(f"⚠️ **Alkaline Soil (pH {ph:.1f}):** Apply **Agricultural Gypsum @ 250 kg/acre** along with green manuring (Dhaincha/Sunhemp).")
    else:
        advice.append(f"✅ **Soil pH ({ph:.1f}) is Healthy & Optimal** for {crop}.")

    return {
        "crop": crop, 
        "recommendations": advice, 
        "target": target,
        "n_status": "Deficient" if n < target["N"] - 15 else ("High" if n > target["N"] + 20 else "Optimal"),
        "p_status": "Deficient" if p < target["P"] - 10 else "Optimal",
        "k_status": "Deficient" if k < target["K"] - 10 else "Optimal",
        "ph_status": "Acidic" if ph < ph_min else ("Alkaline" if ph > ph_max else "Optimal")
    }

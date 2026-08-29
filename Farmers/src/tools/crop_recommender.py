from typing import List, Dict, Any

CROP_AGRO_DATABASE = [
    {
        "crop": "Paddy / Rice (వరి / धान)",
        "optimal_n": (80, 140),
        "optimal_p": (30, 60),
        "optimal_k": (30, 60),
        "optimal_ph": (5.5, 7.2),
        "min_rain_mm": 900,
        "soil_types": ["Clayey", "Clay Loam", "Alluvial", "Black Soil"],
        "season": "Kharif & Rabi",
        "duration_days": "120-145 Days",
        "avg_yield_q": 28
    },
    {
        "crop": "Wheat (గోధుమ / गेहूं)",
        "optimal_n": (100, 150),
        "optimal_p": (40, 70),
        "optimal_k": (30, 50),
        "optimal_ph": (6.0, 7.8),
        "min_rain_mm": 350,
        "soil_types": ["Well-Drained Loam", "Clay Loam", "Alluvial"],
        "season": "Rabi (Winter)",
        "duration_days": "115-130 Days",
        "avg_yield_q": 22
    },
    {
        "crop": "Cotton (పత్తి / कपास)",
        "optimal_n": (90, 160),
        "optimal_p": (40, 75),
        "optimal_k": (40, 80),
        "optimal_ph": (6.2, 8.2),
        "min_rain_mm": 500,
        "soil_types": ["Deep Black Cotton Soil (Vertisol)", "Medium Black", "Sandy Loam"],
        "season": "Kharif (Monsoon)",
        "duration_days": "150-180 Days",
        "avg_yield_q": 14
    },
    {
        "crop": "Tomato (టమాటా / टमाटर)",
        "optimal_n": (120, 180),
        "optimal_p": (60, 120),
        "optimal_k": (80, 160),
        "optimal_ph": (6.0, 7.0),
        "min_rain_mm": 400,
        "soil_types": ["Red Sandy Loam", "Rich Friable Loam", "Black Loam"],
        "season": "Year-round (Kharif, Rabi, Summer)",
        "duration_days": "90-110 Days",
        "avg_yield_q": 180
    },
    {
        "crop": "Chilli (మిరప / मिर्च)",
        "optimal_n": (100, 160),
        "optimal_p": (50, 90),
        "optimal_k": (60, 120),
        "optimal_ph": (6.0, 7.5),
        "min_rain_mm": 450,
        "soil_types": ["Well-Drained Black Loam", "Red Sandy Loam", "Alluvial"],
        "season": "Kharif - Rabi",
        "duration_days": "140-160 Days",
        "avg_yield_q": 25
    },
    {
        "crop": "Maize (మొక్కజొన్న / मक्का)",
        "optimal_n": (100, 150),
        "optimal_p": (45, 75),
        "optimal_k": (35, 60),
        "optimal_ph": (5.8, 7.5),
        "min_rain_mm": 450,
        "soil_types": ["Deep Fertile Loam", "Red Sandy Loam", "Alluvial"],
        "season": "Kharif, Rabi & Spring",
        "duration_days": "95-115 Days",
        "avg_yield_q": 32
    },
    {
        "crop": "Groundnut (వేరుశనగ / मूंगफली)",
        "optimal_n": (20, 40),
        "optimal_p": (40, 80),
        "optimal_k": (30, 60),
        "optimal_ph": (6.0, 7.2),
        "min_rain_mm": 350,
        "soil_types": ["Light Sandy Loam", "Red Sandy", "Friable Alluvial"],
        "season": "Kharif (Rainfed) & Rabi (Irrigated)",
        "duration_days": "105-120 Days",
        "avg_yield_q": 12
    },
    {
        "crop": "Sugarcane (చెరకు / गन्ना)",
        "optimal_n": (150, 250),
        "optimal_p": (60, 100),
        "optimal_k": (80, 150),
        "optimal_ph": (6.5, 7.8),
        "min_rain_mm": 1200,
        "soil_types": ["Deep Heavy Loam", "Alluvial Clay", "Black Soils"],
        "season": "Annual (10-12 Months)",
        "duration_days": "300-360 Days",
        "avg_yield_q": 450
    }
]

def recommend_best_crops(n: float, p: float, k: float, ph: float, rainfall_mm: float = 600, soil_type: str = "Loam") -> List[Dict[str, Any]]:
    """
    Ranks agricultural crops based on multi-variate suitability matching with NPK, pH, and soil conditions.
    """
    ranked = []
    for c in CROP_AGRO_DATABASE:
        score = 100.0
        
        # NPK Match
        n_min, n_max = c["optimal_n"]
        p_min, p_max = c["optimal_p"]
        k_min, k_max = c["optimal_k"]
        ph_min, ph_max = c["optimal_ph"]
        
        if n < n_min: score -= min(25, (n_min - n) * 0.3)
        if p < p_min: score -= min(20, (p_min - p) * 0.3)
        if k < k_min: score -= min(20, (k_min - k) * 0.3)
        
        # pH Penalty
        if ph < ph_min or ph > ph_max:
            dist = min(abs(ph - ph_min), abs(ph - ph_max))
            score -= min(25, dist * 15)

        # Soil type bonus
        if any(s.lower() in soil_type.lower() for s in c["soil_types"]):
            score += 5

        suitability = max(50, min(99, int(round(score))))
        
        ranked.append({
            "crop": c["crop"],
            "suitability_score": suitability,
            "season": c["season"],
            "duration": c["duration_days"],
            "expected_yield_q": c["avg_yield_q"],
            "soil_fit": "Optimal Match" if suitability >= 85 else "Moderate Match"
        })

    ranked.sort(key=lambda x: x["suitability_score"], reverse=True)
    return ranked

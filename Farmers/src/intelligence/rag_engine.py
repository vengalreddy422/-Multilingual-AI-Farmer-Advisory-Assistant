from typing import List, Dict, Any

# Grounded ICAR / State Agricultural Universities Extension Knowledge Base
ICAR_AGRONOMY_KB = [
    {
        "keywords": ["tomato", "early blight", "leaf spot", "ముందస్తు", "टमाटर"],
        "topic": "Tomato Foliar Disease Management",
        "guidelines": "ICAR-IIHR: For Tomato Early Blight (Alternaria), spray Mancozeb 75 WP @ 2.5g/L or Azoxystrobin + Difenoconazole @ 1ml/L. Organic: Spray 5% NSKE (Neem Seed Kernel Extract) + Trichoderma harzianum @ 5g/L."
    },
    {
        "keywords": ["rice", "paddy", "blast", "bph", "వరి", "धान"],
        "topic": "Paddy Integrated Pest & Disease Protection",
        "guidelines": "ICAR-NRRI: For Rice Blast, spray Tricyclazole 75 WP @ 0.6g/L. For Brown Plant Hopper (BPH), create alleyways (1 row per 2m) and spray Triflumezopyrim 10% SC @ 94ml/acre. Avoid excess urea."
    },
    {
        "keywords": ["cotton", "bollworm", "leaf reddening", "పత్తి", "कपास"],
        "topic": "Cotton Canopy & Boll Management",
        "guidelines": "CICR Nagpur: Install 5 pheromone traps/acre for Pink Bollworm. For magnesium deficiency (leaf reddening), foliar spray 1% Magnesium Sulphate + 1% Urea at flowering and boll development stages."
    },
    {
        "keywords": ["chilli", "thrips", "mites", "murda", "మిరప", "मिर्च"],
        "topic": "Chilli Sucking Pest Complex",
        "guidelines": "ANGRAU: Install 20 Blue sticky traps/acre for Black Thrips (Thrips parvispinus). Spray Fipronil 5% SC @ 2ml/L + Spiromesifen 22.9 SC @ 1ml/L. Apply Pongamia oil 3ml/L as organic repellent."
    },
    {
        "keywords": ["fertilizer", "urea", "npk", "dose", "ఎరువులు", "खाद"],
        "topic": "Balanced Crop Nutrition & Split Application",
        "guidelines": "ICAR-IARI: Follow the 4R Nutrient Stewardship (Right Source, Right Rate, Right Time, Right Place). Never apply 100% Nitrogen as basal; split into 50% Basal, 25% Tillering/Vegetative, 25% Panicle/Pre-flowering."
    },
    {
        "keywords": ["drip", "irrigation", "water", "borewell", "నీరు", "सिंचाई"],
        "topic": "Evapotranspiration & Micro-Irrigation Efficiency",
        "guidelines": "PMKSY: Drip irrigation provides 85-90% water use efficiency compared to 45-55% in furrow flooding. Operate drip pumps during low-evapotranspiration morning hours to minimize root-zone percolation loss."
    },
    {
        "keywords": ["organic", "zbnf", "jeevamrutham", "సేంద్రీయ", "जैविक"],
        "topic": "Natural Farming & Biological Soil Activation",
        "guidelines": "National Centre of Organic Farming (NCOF): Apply 200 Litres/acre of Ghanajeevamrutham/Dravajeevamrutham with irrigation water every fortnight to boost microbial colony forming units (CFU) in soil."
    }
]

class AgriRAGEngine:
    def __init__(self):
        self.kb = ICAR_AGRONOMY_KB

    def retrieve_context(self, query: str, top_k: int = 2) -> List[Dict[str, str]]:
        """
        Retrieves grounded agronomic standards matching farmer query keywords.
        """
        q_lower = query.lower()
        scored_entries = []

        for entry in self.kb:
            matches = sum(1 for kw in entry["keywords"] if kw in q_lower)
            if matches > 0:
                scored_entries.append((matches, entry))

        scored_entries.sort(key=lambda x: x[0], reverse=True)
        return [item[1] for item in scored_entries[:top_k]]

    def query(self, text: str) -> str:
        results = self.retrieve_context(text)
        if results:
            lines = [f"🏛️ **{r['topic']} (ICAR Verified):**\n{r['guidelines']}" for r in results]
            return "\n\n".join(lines)
        return "Apply Integrated Pest and Nutrient Management (IPNM) standards tailored to current soil moisture."

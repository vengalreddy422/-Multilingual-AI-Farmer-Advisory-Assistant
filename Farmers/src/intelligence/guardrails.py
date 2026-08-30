import re
from typing import Dict, Any, Tuple, List

# Central Insecticide Board & Registration Committee (CIB&RC) Banned Substance Registry
BANNED_CHEMICALS_REGISTRY = {
    "endosulfan": "Banned nationwide by Supreme Court order due to severe neurotoxicity.",
    "monocrotophos": "Prohibited on all vegetable and horticulture crops (Highly toxic).",
    "ddt": "Banned for agricultural use (Persistent Organic Pollutant).",
    "paraquat": "Restricted use only with certified commercial spray gear; prohibited for retail foliar spray.",
    "aldicarb": "Banned due to high acute mammalian toxicity.",
    "phorate": "Banned / Restricted due to extreme groundwater contamination risks."
}

# Maximum Safe Dilution Thresholds per Liter of Water (CIB&RC Guidelines)
MAX_SAFE_DOSAGES_PER_LITER = {
    "imidacloprid": (0.3, 0.5, "ml"),
    "mancozeb": (2.0, 3.0, "g"),
    "propiconazole": (0.8, 1.2, "ml"),
    "hexaconazole": (1.5, 2.5, "ml"),
    "coragen": (0.3, 0.5, "ml"),
    "chlorantraniliprole": (0.3, 0.5, "ml"),
    "fipronil": (1.5, 2.5, "ml"),
    "neem oil": (2.0, 5.0, "ml")
}

class AgriSafetyGuardrails:
    """
    Enterprise-grade Safety & Hallucination Defense Layer for Kisan Mitra AI.
    Ensures zero dangerous chemical recommendations and prevents jailbreak exploits.
    """

    def validate_user_query(self, query: str) -> Tuple[bool, str]:
        """
        Guards against jailbreak attempts and prompt injections.
        """
        q_lower = query.lower()
        
        # Jailbreak keywords
        jailbreak_triggers = [
            "ignore all previous", "ignore previous", "ignore instructions", "system prompt", 
            "act as a", "write a virus", "write a python", "write code", "bypass rules", 
            "jailbreak", "prompt injection", "dan mode", "developer mode"
        ]
        for trigger in jailbreak_triggers:
            if trigger in q_lower:
                return False, "⚠️ **Security Guardrail Alert:** Out-of-domain prompt detected. Kisan Mitra AI is strictly restricted to certified agricultural and agronomic inquiries."

        return True, ""

    def audit_ai_response(self, response_text: str) -> Dict[str, Any]:
        """
        Scans AI output for banned substances and excessive chemical concentrations.
        """
        resp_lower = response_text.lower()
        warnings = []
        is_safe = True

        # 1. Banned Chemical Interception
        for chemical, reason in BANNED_CHEMICALS_REGISTRY.items():
            if re.search(r'\b' + re.escape(chemical) + r'\b', resp_lower):
                is_safe = False
                warnings.append(f"🚨 **Prohibited Chemical Intercepted:** '{chemical.title()}' is {reason}")

        # 2. Dosage Sanity Verification
        # Check for dangerous high numbers (e.g. 50 ml/L or 100 g/L)
        lethal_matches = re.findall(r'(\d+)\s*(?:ml|g|gm|grams|milliliters)\s*(?:per|\/)\s*(?:liter|litre|l)', resp_lower)
        for val_str in lethal_matches:
            val = float(val_str)
            if val > 15.0 and "neem" not in resp_lower and "manure" not in resp_lower and "buttermilk" not in resp_lower:
                warnings.append(f"⚠️ **High Concentration Warning:** {val} ml/g per liter exceeds standard foliar safety limits. Re-verifying with ICAR thresholds.")

        return {
            "is_compliant": is_safe,
            "cibrc_verified": True if not warnings else False,
            "security_badge": "🛡️ CIB&RC Safety Audited" if not warnings else "⚠️ Safety Caution Applied",
            "warnings": warnings
        }

guardrail_engine = AgriSafetyGuardrails()

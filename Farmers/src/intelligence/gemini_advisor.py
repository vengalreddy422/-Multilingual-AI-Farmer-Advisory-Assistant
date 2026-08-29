import os
from typing import List
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

class GeminiAgriAdvisor:
    def __init__(self):
        # Gather all configured Gemini API keys
        raw_keys = [
            os.getenv("GEMINI_API_KEY", ""),
            os.getenv("GEMINI_API_KEY_2", ""),
            os.getenv("GEMINI_API_KEY_SECONDARY", "")
        ]
        
        # Also support comma-separated list in GEMINI_API_KEYS if present
        extra_keys = os.getenv("GEMINI_API_KEYS", "").split(",")
        raw_keys.extend(extra_keys)

        # Deduplicate while preserving order
        self.api_keys = []
        for k in raw_keys:
            clean_k = k.strip().strip('"').strip("'")
            if clean_k and clean_k not in self.api_keys:
                self.api_keys.append(clean_k)

        self.clients = []
        for k in self.api_keys:
            try:
                c = genai.Client(api_key=k)
                self.clients.append(c)
            except Exception:
                pass

        self.current_key_idx = 0

    def generate_response(self, query: str, language: str = "English", weather_context: dict = None, location: str = "India") -> str:
        weather_str = "Not available"
        if weather_context and weather_context.get("status") == "success":
            weather_str = (
                f"Temp: {weather_context.get('temperature')}°C, "
                f"Humidity: {weather_context.get('humidity')}%, "
                f"Condition: {weather_context.get('condition')}, "
                f"Rain Risk: {weather_context.get('rain_risk')}"
            )

        system_prompt = f"""You are Kisan Mitra, a top agricultural scientist and agronomist for Indian farmers.
Target Language: {language} (Respond directly and fluently in {language}).
Farmer Location: {location}
Live Weather Condition: {weather_str}

Guidelines:
1. Provide accurate, practical farming advice grounded in ICAR and State Agricultural University standards.
2. Structure your advice into:
   - 🌾 **Direct Answer & Diagnostic Insight**
   - 🌿 **Organic / Natural Solution (ZBNF):** (e.g. Neem oil, Jeevamrutham, Trichoderma)
   - 🧪 **Recommended Integrated Treatment:** (Active ingredient, dilution per acre/liter, dosage)
   - ⚠️ **Safety & Weather Precaution:** (Mention spraying precautions if rain or wind is high)
3. Keep the tone respectful, clear, and easy for farmers to understand.
4. Keep the output concisely formatted in clean Markdown with emojis."""

        # Multi-Key Failover Loop
        total_clients = len(self.clients)
        if total_clients > 0:
            for attempt in range(total_clients):
                client_idx = (self.current_key_idx + attempt) % total_clients
                client = self.clients[client_idx]
                
                try:
                    response = client.models.generate_content(
                        model="gemini-2.5-flash",
                        contents=query,
                        config=types.GenerateContentConfig(
                            system_instruction=system_prompt,
                            temperature=0.3,
                            max_output_tokens=800
                        )
                    )
                    if response and response.text:
                        # Success with this key: update active index
                        self.current_key_idx = client_idx
                        return response.text.strip()

                except Exception as e:
                    err_str = str(e).lower()
                    # Check for rate limit / quota exhaustion / quota exceeded
                    if "429" in err_str or "quota" in err_str or "resource_exhausted" in err_str:
                        # Switch to the next key automatically
                        next_idx = (client_idx + 1) % total_clients
                        self.current_key_idx = next_idx
                        continue
                    else:
                        # Other transient exception: try next key
                        continue

        # 2. Resilient Rule-Based Agronomy Fallback (If all keys exhausted)
        return self._generate_rule_based_fallback(query, language, weather_context, location)

    def _get_rate_limit_msg(self, language: str) -> str:
        lang_lower = language.lower()
        if "telugu" in lang_lower or "te" in lang_lower:
            return "⚠️ **సర్వర్ రద్దీగా ఉంది:** ఉచిత వినియోగ పరిమితి దాటింది. దయచేసి 20-30 సెకన్ల తర్వాత మళ్లీ అడగండి."
        elif "hindi" in lang_lower or "hi" in lang_lower:
            return "⚠️ **सर्वर व्यस्त है:** दैनिक अनुरोध सीमा समाप्त हो गई है। कृपया कुछ देर बाद पुन: प्रयास करें।"
        elif "tamil" in lang_lower or "ta" in lang_lower:
            return "⚠️ **சேவையகம் பிஸியாக உள்ளது:** சிறிது நேரம் கழித்து மீண்டும் முயற்சிக்கவும்."
        elif "kannada" in lang_lower or "kn" in lang_lower:
            return "⚠️ **ಸರ್ವರ್ ಬ್ಯುಸಿಯಾಗಿದೆ:** ದಯವಿಟ್ಟು ಸ್ವಲ್ಪ ಸಮಯದ ನಂತರ ಮತ್ತೆ ಪ್ರಯತ್ನಿಸಿ."
        elif "marathi" in lang_lower or "mr" in lang_lower:
            return "⚠️ **सर्व्हर व्यस्त आहे:** कृपया काही वेळाने पुन्हा प्रयत्न करा."
        return "⚠️ **AI Assistant is Busy:** Rate limit reached on the free tier. Please wait 20 seconds and ask again."

    def _generate_rule_based_fallback(self, query: str, language: str, weather_context: dict, location: str) -> str:
        q = query.lower()
        lang = language.lower()

        rain_warning = ""
        if weather_context and weather_context.get("rain_risk"):
            rain_warning = "\n- ⚠️ **Weather Alert:** Rain probability is high today. Postpone foliar spraying and top-dressing by 24-48 hours."

        if "telugu" in lang:
            if "tomato" in q or "టమాటా" in q or "leaf" in q or "ఆకు" in q:
                return f"""### 🌾 కిసాన్ మిత్ర నిపుణుల సలహా ({location})
**సమస్య పరిశీలన:** టమాటా మరియు కూరగాయల పంటలలో రసం పీల్చే పురుగులు లేదా ఆకు మచ్చ తెగులు లక్షణాలు.

🌿 **సేంద్రీయ పరిష్కారం:**
- 5 మి.లీ వేప నూనె (10,000 PPM) + 1 లీటరు నీటికి కలిపి పిచికారీ చేయండి.
- జీవామృతం లేదా పులిసిన మజ్జిగ ద్రావణం పిచికారీ చేయడం ద్వారా తెగుళ్ల వ్యాప్తి తగ్గుతుంది.

🧪 **రసాయన నివారణ:**
- ఇమిడాక్లోప్రిడ్ 17.8% SL (0.5 మి.లీ / లీటరు) లేదా మాంకోజెబ్ 75% WP (2.5 గ్రా / లీటరు).{rain_warning}

📌 **జాగ్రత్త:** పిచికారీ చేసేటప్పుడు రక్షణ మాస్క్ ధరించండి."""

            return f"""### 🌾 కిసాన్ మిత్ర వ్యవసాయ సలహా ({location})
**మీ ప్రశ్న:** {query}

- 🌿 **సాధారణ సిఫార్సు:** పంట ఎదుగుదలకు తగినంత సమతుల్య పోషకాలు (NPK) అందించండి.
- 💧 **నీటి యాజమాన్యం:** మట్టి తేమను బట్టి డ్రిప్ ద్వారా నీరు అందించండి.{rain_warning}
- 🏛️ **సహాయం:** సమీప కృషి విజ్ఞాన కేంద్రం (KVK) లేదా రైతు భరోసా కేంద్రాన్ని సంప్రదించండి."""

        elif "hindi" in lang:
            return f"""### 🌾 किसान मित्र कृषि परामर्श ({location})
**प्रश्न:** {query}

🌿 **जैविक उपाय:**
- 5 मिली नीम का तेल (Neem Oil) प्रति लीटर पानी में मिलाकर छिड़काव करें।
- ट्राइकोडर्मा विरिडी (Trichoderma viride) 5 ग्राम प्रति लीटर जड़ के पास दें।

🧪 **उन्नत प्रबंधन:**
- एनपीके (19:19:19) घुलनशील खाद का 5 ग्राम/लीटर के हिसाब से छिड़काव करें।{rain_warning}

📌 **सुझाव:** स्थानीय कृषि विज्ञान केंद्र (KVK) से मृदा स्वास्थ्य कार्ड की जांच अवश्य कराएं।"""

        # English Default
        return f"""### 🌾 Kisan Mitra Agronomy Expert Advice ({location})
**Query:** {query}

🌿 **Organic Remedy (ZBNF):**
- Spray 5ml Neem Oil (10,000 PPM) + 1ml liquid soap per liter of water.
- Apply Jeevamrutham or Trichoderma viride for soil root zone vigor.

🧪 **Integrated Crop Management:**
- Balance macro-nutrients (NPK) according to soil test values.
- For sucking pests: Imidacloprid 17.8% SL @ 0.5 ml/L of clean water.{rain_warning}

📌 **Notice:** Always wear protective gear during application. Maintain optimal soil moisture."""
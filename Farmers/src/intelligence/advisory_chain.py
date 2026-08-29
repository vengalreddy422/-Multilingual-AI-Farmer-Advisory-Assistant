from config.settings import settings

class AdvisoryOrchestrator:
    def generate_advisory(self, query: str, language: str, weather_info: dict = None, disease_data: dict = None, soil_data: dict = None) -> str:
        # Check if user has OpenAI API key configured
        if settings.OPENAI_API_KEY and settings.OPENAI_API_KEY.startswith("sk-"):
            try:
                from openai import OpenAI
                client = OpenAI(api_key=settings.OPENAI_API_KEY)
                prompt = f"""You are Kisan Mitra, an agronomy AI. Provide advice for: '{query}' in language: {language}.
Weather: {weather_info}
Leaf Diagnostics: {disease_data}
Soil: {soil_data}"""
                res = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=400
                )
                return res.choices[0].message.content
            except Exception:
                pass

        # Built-in rule-based expert advisor engine
        response_lines = [
            f"### 🌾 Kisan Mitra Agronomy Advice ({language})",
            f"**Query:** {query}\n"
        ]

        if disease_data:
            response_lines.append(f"**Diagnostic Result:** {disease_data['disease']} ({int(disease_data['confidence']*100)}% Match)")
            response_lines.append(f"- **Pathogen:** {disease_data['pathogen']}")
            response_lines.append(f"- **Prescription:** {disease_data['treatment']}\n")

        if weather_info and weather_info.get("status") == "success":
            response_lines.append(f"**Weather Advisory ({weather_info['condition']}):**")
            if weather_info.get("rain_risk"):
                response_lines.append("- ⚠️ Rain forecast detected: Postpone chemical spraying and top-dressing by 24-48 hours.")
            else:
                response_lines.append(f"- Weather is favorable for field operations (Temp: {weather_info['temperature']}°C, Wind: {weather_info['wind_speed']} m/s).")
            response_lines.append("")

        if soil_data:
            response_lines.append(f"**Soil Health Strategy for {soil_data['crop']}:**")
            for rec in soil_data["recommendations"]:
                response_lines.append(f"- {rec}")
            response_lines.append("")

        response_lines.append("**Key Recommendation:** Maintain clean bunds, inspect the crop weekly for pest threshold levels, and consult your local KVK center for customized seed varieties.")
        return "\n".join(response_lines)

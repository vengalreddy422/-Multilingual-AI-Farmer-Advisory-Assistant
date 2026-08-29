import re
import io
import functools
from gtts import gTTS

def clean_text_for_speech(raw_text: str) -> str:
    """
    Cleans markdown formatting and emojis while strictly preserving
    all Indic languages (Telugu, Hindi, Tamil, Kannada, Marathi, Bengali, etc.).
    """
    if not raw_text:
        return ""
    
    # Strip markdown headers, bold, italics, links, tables
    text = re.sub(r'#+', '', raw_text)
    text = re.sub(r'[*`~_]', '', text)
    text = re.sub(r'\|', ' ', text)
    text = re.sub(r'-{2,}', ' ', text)
    text = re.sub(r'http\S+|www\.\S+', '', text)
    
    # Remove emojis and unwanted ASCII symbols, but PRESERVE Indic unicode ranges:
    # \u0900-\u097F : Devanagari (Hindi, Marathi)
    # \u0980-\u09FF : Bengali
    # \u0A00-\u0A7F : Gurmukhi (Punjabi)
    # \u0A80-\u0AFF : Gujarati
    # \u0B80-\u0BFF : Tamil
    # \u0C00-\u0C7F : Telugu
    # \u0C80-\u0CFF : Kannada
    # \u0D00-\u0D7F : Malayalam
    indic_safe_pattern = r'[^\w\s.,?!:;\u0900-\u097F\u0980-\u09FF\u0A00-\u0A7F\u0A80-\u0AFF\u0B80-\u0BFF\u0C00-\u0C7F\u0C80-\u0CFF\u0D00-\u0D7F]'
    text = re.sub(indic_safe_pattern, ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

@functools.lru_cache(maxsize=64)
def _synthesize_cached(clean_text: str, selected_lang: str) -> bytes:
    fp = io.BytesIO()
    tts = gTTS(text=clean_text, lang=selected_lang, slow=False)
    tts.write_to_fp(fp)
    return fp.getvalue()

def generate_voice_audio(text: str, lang: str = "en") -> io.BytesIO:
    """
    Generates voice byte stream in the requested Indian language.
    """
    clean_text = clean_text_for_speech(text)
    if not clean_text or len(clean_text) < 2:
        clean_text = "Here is your agricultural advisory report."

    # Truncate text for speech if extremely long to maintain snappy response
    if len(clean_text) > 400:
        clean_text = clean_text[:400] + "..."

    lang_map = {
        "te": "te",
        "hi": "hi",
        "ta": "ta",
        "kn": "kn",
        "mr": "mr",
        "bn": "bn",
        "gu": "gu",
        "en": "en"
    }
    selected_lang = lang_map.get(lang.lower(), "en")

    try:
        audio_bytes = _synthesize_cached(clean_text, selected_lang)
        return io.BytesIO(audio_bytes)
    except Exception:
        # Fallback to English TTS if regional speech fails
        try:
            audio_bytes = _synthesize_cached(clean_text, "en")
            return io.BytesIO(audio_bytes)
        except Exception:
            return io.BytesIO()

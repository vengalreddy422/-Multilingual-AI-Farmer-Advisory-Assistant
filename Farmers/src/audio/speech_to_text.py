import io
import speech_recognition as sr
from config.settings import settings

def transcribe_audio_bytes(audio_bytes: bytes, lang_code: str = "en") -> str:
    """
    Transcribes audio bytes recorded directly from the browser microphone.
    Supports free Google Speech API & OpenAI Whisper fallback.
    """
    # Map app language code to speech recognition locale
    locale_map = {
        "en": "en-IN",
        "hi": "hi-IN",
        "te": "te-IN",
        "ta": "ta-IN",
        "kn": "kn-IN",
        "mr": "mr-IN",
        "pa": "pa-IN",
        "bn": "bn-IN"
    }
    target_locale = locale_map.get(lang_code, "en-IN")

    # 1. Try local / free Google Speech Recognition
    recognizer = sr.Recognizer()
    try:
        audio_file = io.BytesIO(audio_bytes)
        with sr.AudioFile(audio_file) as source:
            recognizer.adjust_for_ambient_noise(source, duration=0.2)
            audio_data = recognizer.record(source)
            text = recognizer.recognize_google(audio_data, language=target_locale)
            if text:
                return text
    except Exception:
        pass

    # 2. Fallback to OpenAI Whisper if API key is provided
    if settings.OPENAI_API_KEY and settings.OPENAI_API_KEY.startswith("sk-"):
        try:
            from openai import OpenAI
            client = OpenAI(api_key=settings.OPENAI_API_KEY)
            audio_file = io.BytesIO(audio_bytes)
            audio_file.name = "recording.wav"
            transcription = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                language=lang_code if lang_code != "en" else None
            )
            return transcription.text
        except Exception:
            pass

    return ""

import os
from pathlib import Path
from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).resolve().parent.parent

class Settings(BaseSettings):
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    OPENWEATHERMAP_API_KEY: str = os.getenv("OPENWEATHERMAP_API_KEY", "")
    DATA_GOV_IN_API_KEY: str = os.getenv("DATA_GOV_IN_API_KEY", "")

    MODEL_PATH: Path = BASE_DIR / "models" / "plant_disease_model.onnx"
    VECTOR_STORE_DIR: Path = BASE_DIR / "src" / "database" / "vector_store"

    SUPPORTED_LANGUAGES: dict = {
        "en": "English",
        "hi": "Hindi",
        "te": "Telugu",
        "ta": "Tamil",
        "kn": "Kannada",
        "mr": "Marathi",
        "pa": "Punjabi",
        "bn": "Bengali"
    }

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()

from functools import lru_cache
from pathlib import Path
import os

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parents[1]
load_dotenv(BASE_DIR / ".env")


class Settings:
    """Application settings loaded from environment variables."""

    app_name: str
    company_name: str
    gemini_api_key: str
    gemini_model: str
    ai_mode: str
    backend_url: str
    frontend_url: str
    logo_path: Path

    def __init__(self) -> None:
        self.app_name = os.getenv("APP_NAME", "LegalEase")
        self.company_name = os.getenv("COMPANY_NAME", "LegalEase")
        self.gemini_api_key = os.getenv("GEMINI_API_KEY", "").strip()
        self.gemini_model = os.getenv("GEMINI_MODEL", "gemini-3.8-flash").strip()
        self.ai_mode = os.getenv("AI_MODE", "gemini").strip().lower()
        self.backend_url = os.getenv("BACKEND_URL", "http://127.0.0.1:8000").rstrip("/")
        self.frontend_url = os.getenv("FRONTEND_URL", "http://127.0.0.1:8501").rstrip("/")
        self.logo_path = BASE_DIR / "assets" / "logo.png"

    @property
    def use_mock_ai(self) -> bool:
        return self.ai_mode == "mock" or not self.gemini_api_key


@lru_cache

def get_settings() -> Settings:
    return Settings()

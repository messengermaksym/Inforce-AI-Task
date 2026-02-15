"""
Конфігурація додатку з змінних середовища (.env).
"""
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

# Корінь проєкту (каталог, де лежать .env та app/)
PROJECT_ROOT = Path(__file__).resolve().parent.parent
ENV_FILE = PROJECT_ROOT / ".env"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=str(ENV_FILE) if ENV_FILE.exists() else None,
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # Gemini API
    GEMINI_API_KEY: str = ""
    GEMINI_MODEL_ID: str = "gemini-2.5-flash"
    GEMINI_INPUT_PRICE_PER_MILLION: float = 0.30
    GEMINI_OUTPUT_PRICE_PER_MILLION: float = 2.50

    # Database
    DATABASE_URL: str = "sqlite:///./sql_app.db"


settings = Settings()

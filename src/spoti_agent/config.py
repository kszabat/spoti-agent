from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

_PROJECT_ROOT = Path(__file__).resolve().parents[2]

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=_PROJECT_ROOT / ".env", extra="ignore", env_file_encoding="utf-8"
    )

    spotify_client_id: str
    spotify_client_secret: str
    spotify_redirect_uri: str = "http://127.0.0.1:8888/callback"

    model: str = "gemini-3-flash-preview"
    api_key: str


@lru_cache
def get_settings() -> Settings:
    return Settings()

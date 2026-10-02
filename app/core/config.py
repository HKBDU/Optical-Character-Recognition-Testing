from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_env: str = "development"
    ocr_host: str = "0.0.0.0"
    ocr_port: int = 8000
    max_file_size_mb: int = 20
    ocr_high_confidence: float = 0.90
    ocr_medium_confidence: float = 0.75
    ocr_lang: str = "en"
    ocr_use_gpu: bool = False
    ocr_max_pdf_pages: int = 30
    model_config = SettingsConfigDict(env_file=".env", extra="ignore", case_sensitive=False)

@lru_cache
def get_settings() -> Settings:
    return Settings()


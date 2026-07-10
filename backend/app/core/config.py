from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    APP_NAME: str = "KnowledgeFlow AI"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True

    # Database
    DATABASE_URL: str = "postgresql://user:password@localhost:5432/knowledgeflow"

    # Storage
    STORAGE_TYPE: str = "local"
    LOCAL_STORAGE_PATH: str = "./storage"

    # AI
    GEMINI_API_KEY: str = ""

    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    return Settings()

"""
Application Configuration
Reads from .env via pydantic-settings
"""

from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # IBM WatsonX / Granite
    IBM_WATSONX_API_KEY: str = ""
    IBM_WATSONX_PROJECT_ID: str = ""
    IBM_WATSONX_URL: str = "https://us-south.ml.cloud.ibm.com"
    IBM_GRANITE_MODEL_ID: str = "ibm/granite-3-8b-instruct"
    IBM_CLOUD_API_KEY: str = ""
    IBM_IAM_URL: str = "https://iam.cloud.ibm.com/identity/token"

    # App
    APP_HOST: str = "0.0.0.0"
    APP_PORT: int = 8000
    APP_DEBUG: bool = True
    SECRET_KEY: str = "change-me-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440

    # Database
    DATABASE_URL: str = "sqlite:///./career_counselor.db"

    # CORS
    CORS_ORIGINS: str = "http://localhost:3000,http://localhost:5173"

    # External APIs
    RAPID_API_KEY: Optional[str] = None
    JSEARCH_API_HOST: str = "jsearch.p.rapidapi.com"

    # Limits
    MAX_REQUESTS_PER_MINUTE: int = 30

    # Logging
    LOG_LEVEL: str = "INFO"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"


settings = Settings()

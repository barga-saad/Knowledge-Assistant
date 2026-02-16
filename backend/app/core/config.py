"""
Core configuration module
Manages all environment variables and app settings
"""

from pydantic_settings import BaseSettings
from typing import Optional
import os


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    
    This uses Pydantic V2's BaseSettings which automatically
    loads from environment variables matching the field names.
    """
    
    # ========================
    # Database Configuration
    # ========================
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str
    
    @property
    def DATABASE_URL(self) -> str:
        """Construct PostgreSQL connection string"""
        return (
            f"postgresql+psycopg://{self.POSTGRES_USER}:"
            f"{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:"
            f"{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )
    
    # ========================
    # Backend Configuration
    # ========================
    BACKEND_ENV: str = "development"
    SECRET_KEY: str  # Must be at least 32 characters
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # ========================
    # Keycloak Configuration
    # ========================
    KEYCLOAK_URL: str = "http://localhost:8080"
    KEYCLOAK_REALM: str = "knowledge-assistant"
    KEYCLOAK_CLIENT_ID: str
    KEYCLOAK_CLIENT_SECRET: str
    
    # ========================
    # AI Service Configuration
    # ========================
    AI_SERVICE_URL: str = "http://localhost:8001"
    
    # ========================
    # Redis Configuration
    # ========================
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    
    @property
    def REDIS_URL(self) -> str:
        """Construct Redis connection string"""
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"
    
    # ========================
    # File Storage Configuration
    # ========================
    DOCUMENTS_DIR: str = "./documents"
    MAX_FILE_SIZE: int = 52428800  # 50MB in bytes
    ALLOWED_EXTENSIONS: list = ["pdf", "txt"]
    
    # ========================
    # Logging Configuration
    # ========================
    LOG_LEVEL: str = "INFO"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Singleton settings instance
settings = Settings()

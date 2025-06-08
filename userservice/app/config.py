"""Environment configuration for the application."""

import os
from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings."""
    
    # Database settings
    DATABASE_URL: str = "sqlite+aiosqlite:///./test.db"  # Updated for SQLite
    DATABASE_ECHO: bool = False
    
    # JWT settings
    JWT_SECRET_KEY: str = "your-super-secret-jwt-key-change-in-production"
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    JWT_REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # Password settings
    PASSWORD_MIN_LENGTH: int = 8
    PASSWORD_HASH_ROUNDS: int = 12
    
    # Email settings
    SMTP_SERVER: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USERNAME: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    SMTP_FROM_EMAIL: str = "noreply@sicora.sena.edu.co"
    SMTP_FROM_NAME: str = "SICORA - AsisTE App"
    
    # Application settings
    APP_NAME: str = "SICORA UserService"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    LOG_LEVEL: str = "INFO"
    
    # CORS settings
    CORS_ORIGINS: list[str] = ["*"]  # En producción, especificar dominios exactos
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# Global settings instance
settings = Settings()

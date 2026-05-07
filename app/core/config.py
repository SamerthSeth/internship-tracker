"""Configuration management using Pydantic settings."""

import json
import os
from typing import List

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application configuration settings."""

    # App settings
    APP_NAME: str = "Smart Internship & Certificate Tracker"
    DEBUG: bool = False
    ENVIRONMENT: str = "development"

    # Database
    DATABASE_URL: str = (
        os.getenv("DATABASE_URL")
        or os.getenv("POSTGRES_URL")
        or (
            "sqlite+aiosqlite:////tmp/tracker.db"
            if os.getenv("VERCEL") == "1"
            else "sqlite+aiosqlite:///./tracker.db"
        )
    )

    # JWT Settings
    SECRET_KEY: str = (
        "dev-secret-key-not-for-production-change-this-in-production-must-be-32-chars-minimum"
    )
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # File Upload
    MAX_FILE_SIZE: int = 10485760  # 10MB
    ALLOWED_FILE_TYPES: str = "pdf,jpg,jpeg,png"
    FILE_UPLOAD_DIRECTORY: str = "/tmp/uploads" if os.getenv("VERCEL") == "1" else "uploads"

    # CORS
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://localhost:8000",
    ]

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
        extra="ignore",
    )

    @field_validator("CORS_ORIGINS", mode="before")
    @classmethod
    def parse_cors_origins(cls, value):
        """Accept JSON arrays or comma-separated strings for CORS origins."""
        if isinstance(value, str):
            trimmed = value.strip()
            if not trimmed:
                return []
            if trimmed.startswith("["):
                return json.loads(trimmed)
            return [origin.strip() for origin in trimmed.split(",") if origin.strip()]
        return value


settings = Settings()

# Normalize DB URLs for async SQLAlchemy on Vercel/managed platforms
if settings.DATABASE_URL.startswith("postgres://"):
    settings.DATABASE_URL = settings.DATABASE_URL.replace(
        "postgres://", "postgresql+asyncpg://", 1
    )
elif settings.DATABASE_URL.startswith("postgresql://") and "+asyncpg" not in settings.DATABASE_URL:
    settings.DATABASE_URL = settings.DATABASE_URL.replace(
        "postgresql://", "postgresql+asyncpg://", 1
    )

# Remote Postgres on serverless commonly requires TLS
if (
    os.getenv("VERCEL") == "1"
    and settings.DATABASE_URL.startswith("postgresql+asyncpg://")
    and "localhost" not in settings.DATABASE_URL
    and "127.0.0.1" not in settings.DATABASE_URL
    and "ssl=" not in settings.DATABASE_URL
    and "sslmode=" not in settings.DATABASE_URL
):
    separator = "&" if "?" in settings.DATABASE_URL else "?"
    settings.DATABASE_URL = f"{settings.DATABASE_URL}{separator}ssl=require"

"""
Configuration management for Verdant AI Integrated Dashboard
"""
import os
from typing import Optional
from pydantic import field_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings with environment variable support"""
    
    # Application
    app_name: str = "Verdant AI Integrated Dashboard"
    environment: str = "development"
    debug: bool = False
    
    # Database
    postgres_user: str = "postgres"
    postgres_password: str = "postgres"
    postgres_host: str = "localhost"
    postgres_port: int = 5432
    postgres_db: str = "verdant_ai"
    
    # Redis
    redis_url: str = "redis://localhost:6379"
    
    # JWT
    jwt_secret_key: str = "your-secret-key-change-in-production"
    jwt_algorithm: str = "HS256"
    jwt_access_token_expire_minutes: int = 30
    
    # AI/ML
    openai_api_key: Optional[str] = None
    huggingface_api_key: Optional[str] = None
    
    # Logging
    log_level: str = "INFO"
    
    @field_validator("debug", mode="before")
    @classmethod
    def set_debug_mode(cls, v, info):
        """Set debug mode based on environment"""
        return info.data.get("environment") == "development"
    
    @property
    def database_url(self) -> str:
        """Construct database URL from components"""
        return (
            f"postgresql://{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )
    
    @property
    def async_database_url(self) -> str:
        """Construct async database URL for SQLAlchemy"""
        return self.database_url.replace("postgresql://", "postgresql+asyncpg://")
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()
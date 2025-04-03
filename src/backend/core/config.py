from pydantic_settings import BaseSettings
from functools import lru_cache
import os

class Settings(BaseSettings):
    """Base settings shared across environments"""
    APP_NAME: str = "FastAPI Backend"
    API_V1_STR: str = "/api/v1"
    
    # Database settings
    DATABASE_URL: str = "sqlite:///./app.db"  # Default to SQLite for starter projects
    
    # Security settings
    SECRET_KEY: str = "development-key-change-in-production"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Metrics settings
    METRICS_PORT: int = 9090
    
    # Environment-specific settings
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    
    # Supabase settings
    SUPABASE_URL: str = None
    SUPABASE_KEY: str = None
    SUPABASE_JWT_SECRET: str = None
    
    # OAuth settings
    OAUTH_REDIRECT_URL: str = "http://localhost:8000/api/v1/auth/callback"
    FRONTEND_URL: str = "http://localhost:5000"
    
    # CORS settings
    CORS_ORIGINS: str = "http://localhost:5000,http://localhost:3000"

    class Config:
        env_file = ".env.local"
        env_file_encoding = "utf-8"

@lru_cache
def get_settings():
    """Load settings based on environment"""
    env = os.getenv("ENVIRONMENT", "development")
    env_file = ".env.local"  # Always use .env.local
    
    # Load environment-specific settings
    settings = Settings(_env_file=env_file)
    
    # Override settings based on environment
    if env.lower() == "development":
        settings.DEBUG = True
    return settings

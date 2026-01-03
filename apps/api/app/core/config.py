from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # App
    APP_NAME: str = "Strava Visualization SaaS"
    DEBUG: bool = True  # Set to True for development
    
    # Database
    DATABASE_URL: str = "sqlite:///./strava_saas.db"
    
    # JWT
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24 hours
    
    # CORS
    CORS_ORIGINS: list[str] = ["http://localhost:3000", "http://localhost:3001"]
    
    # File Storage
    UPLOAD_DIR: str = "./temp/uploads"
    OUTPUT_DIR: str = "./temp/outputs"
    FILE_RETENTION_HOURS: int = 24
    
    # Redis - Use environment variable or default
    # For Windows: try redis://localhost:6379/0 or use Upstash cloud Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # Celery
    CELERY_BROKER_URL: str = "redis://localhost:6379/0"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/0"
    
    # Stripe
    STRIPE_SECRET_KEY: str = ""
    STRIPE_PUBLISHABLE_KEY: str = ""
    STRIPE_WEBHOOK_SECRET: str = ""
    
    # Pricing (in cents)
    PRICE_SINGLE_NO_FILTER: int = 200  # $2.00
    PRICE_SINGLE_WITH_FILTER: int = 300  # $3.00
    PRICE_PACK_ALL: int = 990  # $9.90
    PRICE_PACK_PREMIUM: int = 1990  # $19.90
    
    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True)


settings = Settings()

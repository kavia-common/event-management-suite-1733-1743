from functools import lru_cache
from pydantic import BaseSettings

# PUBLIC_INTERFACE
class Settings(BaseSettings):
    """Application settings loaded from environment variables for DB connection and JWT secret."""
    POSTGRES_URL: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_PORT: str
    JWT_SECRET_KEY: str = "SUPER_SECRET_JWT"  # Should be overridden in env
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION_MINUTES: int = 60 * 24 * 7  # 7 days

    class Config:
        env_file = ".env"

@lru_cache
def get_settings():
    return Settings()

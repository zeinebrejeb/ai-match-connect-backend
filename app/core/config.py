from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional
from functools import lru_cache 

class Settings(BaseSettings):
    PROJECT_NAME: str = "AI Match Connect"
    API_V1_STR: str = "/api/v1"
    DATABASE_URL: str
    SECRET_KEY: str 
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 7 * 24 * 60
    model_config = SettingsConfigDict(env_file=".env", extra="ignore", env_file_encoding='utf-8')

@lru_cache() 
def get_settings():
    return Settings()

settings = get_settings() 

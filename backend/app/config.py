from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Settings for the project"""
    
    FIREBASE_AUTH_URL: str
    FIREBASE_API_KEY: str
    FIREBASE_ADMIN_SDK_KEY: str
    
    model_config = SettingsConfigDict(env_file="app/.env")


settings = Settings()

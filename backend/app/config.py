"""Essential configuration settings for interfacing with Firebase and Semantic Scholar API's.
"""
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
<<<<<<< HEAD
    """Settings for the project"""

=======
    """
    Essential settings to interface with
    Firebase and Semantic Scholar API services.
    
    Attributes:
        FIREBASE_AUTH_URL (str): Firebase authentication URL
        FIREBASE_API_KEY (str): Firebase API key
        FIREBASE_ADMIN_SDK_KEY (str): Firebase admin sdk key
        SEMANTIC_SCHOLAR_API_URL (str): Semantic Scholar authentication URL
    """
    
>>>>>>> 9487df3 (add: added docstrings and static typying)
    FIREBASE_AUTH_URL: str
    FIREBASE_API_KEY: str
    FIREBASE_ADMIN_SDK_KEY: str
    SEMANTIC_SCHOLAR_API_URL: str

    model_config = SettingsConfigDict(env_file="app/.env")


settings = Settings()

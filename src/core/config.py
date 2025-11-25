import os
from typing import Any, Dict, Optional
from pydantic import Field
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    """
    # Database Settings
    SQL_SERVER_CONNECTION_STRING: Optional[str] = Field(None, env="SQL_SERVER_CONN_STR")
    SQL_SERVER_HOST: Optional[str] = Field(None, env="SQL_SERVER_HOST")
    SQL_SERVER_DB: Optional[str] = Field(None, env="SQL_SERVER_DB")
    SQL_SERVER_TRUSTED_CONNECTION: bool = Field(False, env="SQL_SERVER_TRUSTED_CONNECTION")

    POSTGRES_CONNECTION_STRING: Optional[str] = Field(None, env="POSTGRES_CONN_STR")
    
    # Salesforce Settings
    SF_USERNAME: Optional[str] = Field(None, env="SF_USERNAME")
    SF_PASSWORD: Optional[str] = Field(None, env="SF_PASSWORD")
    SF_TOKEN: Optional[str] = Field(None, env="SF_TOKEN")
    
    # App Settings
    LOG_LEVEL: str = Field("INFO", env="LOG_LEVEL")
    ENVIRONMENT: str = Field("development", env="APP_ENV")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()

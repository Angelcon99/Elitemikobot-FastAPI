from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Literal

class Config(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    PROJECT_NAME: str = "ElitemikoBotAPI"
    DEBUG: bool = False
    DATABASE_URL: str
    ENV: Literal["local", "prod"] = "local"

    LOG_LEVEL: str = "INFO"               
    LOG_DIR: str = "./logs" 

config = Config()

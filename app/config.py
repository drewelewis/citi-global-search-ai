from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

# https://docs.pydantic.dev/latest/concepts/pydantic_settings/#dotenv-env-support
class Config(BaseSettings):
    model_config: SettingsConfigDict = {
        "env_file": ".env"#,"extra": "allow"
        
    }
    POSTGRES_CONNECTION_STRING: Optional[str] = None
    DB_FORCE_ROLLBACK: Optional[bool] = False
    OPENAI_API_BASE: Optional[str] = None
    OPENAI_API_KEY: Optional[str] = None
    OPENAI_API_VERSION: Optional[str] = None
    OPENAI_API_MODEL_VERSION: Optional[str] = None 
    OPENAI_API_MODEL_DEPLOYMENT_NAME: Optional[str] = None
    REDIS_HOST: Optional[str] = None
    REDIS_PORT: Optional[str] = None
    REDIS_PASSWORD: Optional[str] = None
    PROJECT_ROOT: Optional[str] = None

config=Config()



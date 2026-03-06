from pydantic_settings import BaseSettings, SettingsConfigDict
from app.configs.configs_agentic import AgenticSettings
from app.configs.vector_store_configs import VectorStoreSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "FastAPI Robust Starter"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # Database
    DATABASE_URL: str = "sqlite:///./sql_app.db"
    
    # Security
    SECRET_KEY: str = "development_secret_key_change_me"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Nested Configs
    agentic: AgenticSettings = AgenticSettings()
    vector_store: VectorStoreSettings = VectorStoreSettings()
    
    
    model_config = SettingsConfigDict(
        env_file=".env", 
        case_sensitive=True,
        extra="ignore"
    )

settings = Settings()

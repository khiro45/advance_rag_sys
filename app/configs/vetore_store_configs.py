from pydantic_settings import BaseSettings, SettingsConfigDict
import os

class VectorStoreSettings(BaseSettings):
    # Vector DB Settings
    VECTOR_DB_PATH: str = os.path.join(os.getcwd(), "vector_db")
    COLLECTION_NAME: str = "main_collection"
    
    # Embedding Model Settings
    EMBEDDING_MODEL_NAME: str = "all-MiniLM-L6-v2"
    DEVICE: str = "cpu" # or "cuda" if available
    
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
        env_prefix="VS_"
    )

vs_settings = VectorStoreSettings()

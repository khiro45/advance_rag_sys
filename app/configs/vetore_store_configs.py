from pydantic_settings import BaseSettings, SettingsConfigDict
import os

class VectorStoreSettings(BaseSettings):
    # Vector DB Settings
    VECTOR_DB_PATH: str = 'app/services/rag_sys/vectore_store/vectore_db'
    COLLECTION_NAME: str = "main_collection"
    
    # Embedding Model Settings
    EMBEDDING_MODEL_NAME: str = "all-MiniLM-L6-v2"
    DEVICE: str = "cpu" # or "cuda" if available
    
    # Cross Encoder Settings
    CROSS_ENCODER_MODEL_NAME: str = "cross-encoder/msmarco-MiniLM-L-6-v2"
    CROSS_ENCODER_MODEL_PATH: str = "app/services/rag_sys/vectore_store/cross_encoder"
    
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
        env_prefix="VS_"
    )

vs_settings = VectorStoreSettings()

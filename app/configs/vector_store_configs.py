from pydantic_settings import BaseSettings, SettingsConfigDict
import os

class VectorStoreSettings(BaseSettings):
    # Vector DB Settings
    VECTOR_DB_PATH: str = 'app/services/rag_sys/vector_store/vector_db'
    COLLECTION_NAME: str = 'rag_docs'
    EMBEDDING_MODEL_NAME: str = "all-MiniLM-L6-v2"
    EMBEDDING_MODEL_PATH: str = "app/services/rag_sys/vector_store/embedding_model"
    CROSS_ENCODER_MODEL_NAME: str = "cross-encoder/ms-marco-MiniLM-L-6-v2"
    CROSS_ENCODER_MODEL_PATH: str = "app/services/rag_sys/vector_store/cross_encoder"
    
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
        env_prefix="VS_"
    )

vs_settings = VectorStoreSettings()

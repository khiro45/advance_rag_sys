from sentence_transformers import SentenceTransformer
from app.configs.vetore_store_configs import vs_settings

class EmbeddingModel:
    def __init__(self):
        self.model = SentenceTransformer(
            vs_settings.EMBEDDING_MODEL_NAME, 
            device=vs_settings.DEVICE
        )

    def encode(self, text: str):
        return self.model.encode(text).tolist()

    def encode_batch(self, texts: list[str]):
        return self.model.encode(texts).tolist()

# Singleton instance
embedding_model = EmbeddingModel()

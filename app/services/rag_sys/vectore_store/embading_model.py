from sentence_transformers import SentenceTransformer
import os
from app.configs.config import settings
class EmbeddingModel:
    def __init__(self, model_name: str, save_path: str=settings.EMBEDDING_MODEL_PATH):
        self.model_name = model_name
        self.save_path = save_path
        self.model = self._load_or_download()

    def _load_or_download(self):
        if os.path.isdir(self.save_path) and os.listdir(self.save_path):
            print(f"Loading model from local path: {self.save_path}")
            return SentenceTransformer(self.save_path)
        
        print(f"Downloading {self.model_name}...")
        model = SentenceTransformer(self.model_name)
        
        os.makedirs(self.save_path, exist_ok=True)
        model.save(self.save_path)
        return model

    def encode(self, text):
        return self.model.encode(text)
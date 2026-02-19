from sentence_transformers import SentenceTransformer, util
from app.configs.config import settings


class Embedding_model():
    def __init__(self):

        self.model = SentenceTransformer(settings.EMBEDDING_MODEL_NAME)
    
    def encode(self, text):
        return self.model.encode(text)

    def init_model(self):
        if os.path.isdir(settings.VECTOR_DB_PATH):
            self.model = SentenceTransformer(settings.EMBEDDING_MODEL_NAME)
        else:
            self.model = SentenceTransformer(settings.EMBEDDING_MODEL_NAME)
            self.model.save(settings.VECTOR_DB_PATH)


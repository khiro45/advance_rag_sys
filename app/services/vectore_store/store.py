import chromadb
from chromadb.config import Settings as ChromaSettings
from app.configs.vetore_store_configs import vs_settings

class LocalVectorStore:
    def __init__(self):
        self.client = chromadb.PersistentClient(path=vs_settings.VECTOR_DB_PATH)
        self.collection = self.client.get_or_create_collection(
            name=vs_settings.COLLECTION_NAME
        )

    def add_documents(self, ids: list[str], documents: list[str], embeddings: list[list[float]], metadatas: list[dict] = None):
        self.collection.add(
            ids=ids,
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas
        )

    def query(self, query_embeddings: list[list[float]], n_results: int = 5):
        return self.collection.query(
            query_embeddings=query_embeddings,
            n_results=n_results
        )
    def conditional_query(self,filter:dict, n_results: int = 5):
        return self.collection.get(
            n_results=n_results , 
            where=dict
            ) 

# Singleton instance
vector_store = LocalVectorStore()

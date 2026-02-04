import uuid
from typing import List, Dict, Optional
from app.services.vectore_store.model import embedding_model
from app.services.vectore_store.store import vector_store

class VectorStoreService:
    @staticmethod
    def get_embeddings(text: str) -> List[float]:
        """Get embeddings for a given string."""
        return embedding_model.encode(text)

    @staticmethod
    def add_data(text: str, metadata: Optional[Dict] = None):
        """Add a single entry to the vector store."""
        embedding = embedding_model.encode(text)
        doc_id = str(uuid.uuid4())
        vector_store.add_documents(
            ids=[doc_id],
            documents=[text],
            embeddings=[embedding],
            metadatas=[metadata] if metadata else None
        )
        return doc_id

    @staticmethod
    def migrate_data(data_list: List[Dict]):
        """
        Migrate a list of data to the vector store.
        Expected format: [{"text": "...", "metadata": {...}}, ...]
        """
        texts = [item["text"] for item in data_list]
        metadatas = [item.get("metadata", {}) for item in data_list]
        ids = [str(uuid.uuid4()) for _ in texts]
        
        embeddings = embedding_model.encode_batch(texts)
        
        vector_store.add_documents(
            ids=ids,
            documents=texts,
            embeddings=embeddings,
            metadatas=metadatas
        )
        return ids

    @staticmethod
    def search(query_text: str, n_results: int = 5):
        """Search the vector store for similar documents."""
        query_embedding = embedding_model.encode(query_text)
        return vector_store.query(
            query_embeddings=[query_embedding],
            n_results=n_results
        )

# Export as a service instance or just the class
vs_service = VectorStoreService()

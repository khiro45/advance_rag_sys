from app.configs.config import settings 
from app.services.rag_sys.vector_store.embedding_model import Embedding_model
from app.services.rag_sys.vector_store.data_processing import ProcessorFactory
from app.services.rag_sys.schemas import BaseMetaData
from fastapi import File, HTTPException
from sentence_transformers import CrossEncoder
import chromadb
import os 
import uuid
from typing import Callable, Any

class VectorStore():
    def __init__(self, embedding_model: Callable[[], Embedding_model], data_processor: ProcessorFactory = None):
        self.init_dirs()
        self.client = chromadb.PersistentClient(path=settings.vector_store.VECTOR_DB_PATH)
        self.embedding_model: Embedding_model = embedding_model()
        self.collection = self.client.get_or_create_collection(name=settings.vector_store.COLLECTION_NAME)
        self.cross_encoder_model = CrossEncoder(
            settings.vector_store.CROSS_ENCODER_MODEL_NAME, 
            cache_folder=settings.vector_store.CROSS_ENCODER_MODEL_PATH
        )

        
    def init_dirs(self):
        os.makedirs(settings.vector_store.VECTOR_DB_PATH, exist_ok=True)
        os.makedirs(settings.vector_store.CROSS_ENCODER_MODEL_PATH, exist_ok=True)

    async def add_document(self, doc: list[str], meta_data: list[BaseMetaData]):
        if doc and meta_data:
            for  i, page in enumerate(doc) :
                embedding = self.embedding_model.encode(page)
                await self.collection.add(
                    documents=[page],
                    embeddings=[embedding],
                    metadatas=[meta_data[i]] if meta_data[i] else None,
                    ids=[str(uuid.uuid4())]
                )
        else :
            raise HTTPException(400 , f"the insertion data are messing doc:{ doc } ,meta data {meta_data}")
        

    # def seed_data(self, docs: list[list[str]], meta_data: list[BaseMetaData]):
    #     if len(docs) == len(meta_data):
    #         print("seeding data start")
    #         print('num of docs : ', len(docs))
            
    #         if not docs:
    #             print("No documents to seed.")
    #             return

    #         # Batch encode all documents for high performance and cast to float lists
    #         embeddings = [self.embedding_model.encode(doc).tolist() for doc in docs]
    #         ids = [str(uuid.uuid4()) for _ in docs]

    #         self.collection.add(
    #             documents=docs,
    #             embeddings=embeddings,
    #             metadatas=meta_data,
    #             ids=ids
    #         )
    #         print("seeding data complete")
    #     else:
    #         raise ValueError("docs and meta_data must be of same length")    
      
    async def get_document(self, query: str, meta_data: BaseMetaData , n_results: int = 20):
        # ChromaDB query will fail if we pass pydantic model where a dict or None is expected
        where_filter = None
        if meta_data:
            if isinstance(meta_data, BaseMetaData):
                # Flatten the BaseMetaData for filtering if possible
                where_filter = {"source": meta_data.source}
            elif isinstance(meta_data, dict):
                where_filter = meta_data
                
        return self.collection.query(
            query_texts=[query],
            n_results=n_results, 
            where=where_filter
        )

    def cross_encoder_reranking(self, query: str, docs: list[dict], n_results: int = 5):       
        if not docs:
            return []
            
        pairs = [[query, doc['doc']] for doc in docs]
        
        # Batch predict all scores at once
        scores = self.cross_encoder_model.predict(pairs)
        
        scored_docs = []
        for doc, score in zip(docs, scores):
            # score is cast to standard float for clean JSON serialization later
            scored_docs.append([doc, float(score)])
        
        # Sort by score in descending order (highest score first)
        sorted_results = sorted(scored_docs, key=lambda x: x[1], reverse=True)
        return sorted_results[:n_results]
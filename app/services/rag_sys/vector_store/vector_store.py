from app.configs.config import settings 
from app.services.rag_sys.vector_store.embedding_model import Embedding_model
from app.services.rag_sys.vector_store.data_processing import ProcessorFactory
from app.services.rag_sys.schemas import BaseMetaData
from sentence_transformers import CrossEncoder
import chromadb
import os 
import uuid


class VectorStore():
    def __init__(self , embedding_model:Embedding_model , data_processor:ProcessorFactory):
        
        self.init_dirs()
        self.client = chromadb.PersistentClient(path=settings.vector_store.VECTOR_DB_PATH)
        self.embedding_model:Embedding_model = embedding_model()
        self.collection = self.client.get_or_create_collection(name=settings.vector_store.COLLECTION_NAME)
        self.data_processor:ProcessorFactory = data_processor
        self.cross_encoder_model=CrossEncoder(settings.vector_store.CROSS_ENCODER_MODEL_NAME , 
                                             cache_folder=settings.vector_store.CROSS_ENCODER_MODEL_PATH )

    def init_dirs(self):
        os.makedirs(settings.vector_store.VECTOR_DB_PATH, exist_ok=True)
        os.makedirs(settings.vector_store.CROSS_ENCODER_MODEL_PATH, exist_ok=True)

    def add_document(self , doc:str , embedding:list , meta_data:dict|None=None):
        ## run the docs processor
        self.collection.add(
            documents=doc,
            embeddings=embedding,
            metadatas=meta_data,
            ids=str(uuid.uuid4())
        )
   

    def seed_data(self ,docs:list[str] , meta_data:list[dict]):
                ## run the docs processor
        if len(docs)==len(meta_data):
            print("seeding data start")
            print('num of docs : ' , len(docs))

            for i, doc in enumerate(docs):
                print("adding doc ::" , i)                
                embedding=self.embedding_model.encode(doc)
                self.add_document(doc , embedding , meta_data[doc])
        else:
            raise ValueError("docs and meta_data must be of same length")    
      
    def get_document(self , query:str , meta_data:BaseMetaData|None=None , n_results:int=20):
        return self.collection.query(
            query_texts=[query],
            n_results=n_results , 
            where=meta_data
        )

  
    def cross_encoder_reranking(self , query:str , docs:list[dict] , n_results:int=5):       
        pairs = [[query, doc['doc']] for doc in docs]
        scored_docs= []
        for doc in docs:
            scored_docs.append([doc , self.cross_encoder_model.predict(pairs)[0]])
        
        scored_docs = list(zip(scored_docs, docs))     
        sorted_results = sorted(scored_docs, key=lambda x: x[0], reverse=True)   
        return sorted_results[:n_results]
 
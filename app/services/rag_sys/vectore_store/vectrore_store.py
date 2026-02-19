from app.configs.config import settings 
from app.services.rag_sys.vectore_store.embading_model import Embedding_model
from app.services.rag_sys.vectore_store.data_processing import Docs_processor
import chromadb
import os 


class Vectore_store():
    def __init__(self):
        self.client = chromadb.Client(path=settings.VECTOR_DB_PATH)
        self.embedding_model = Embedding_model()
        self.collection = self.client.get_or_create_collection(name=settings.COLLECTION_NAME)
        self.data_processor = Docs_processor

    def add_document(slef , doc:str , embading:list , meta_data:dict|None=None):
        self.collection.add(
            documents=doc,
            embeddings=embading,
            metadatas=meta_data,
            ids=str(uuid.uuid4())
        )

    def get_document(self , query:str , meta_data:str|None=None):
        return self.collection.query(
            query_texts=[query],
            n_results=5
        )

    def seed_data(self ,docs:list[str] , meta_data:list[dict]):
        if len(docs)==len(meta_data):
            print("seeding data start")
            print('num of docs : ' , len(docs))

            for i, doc in enumerate(docs):
                print("adding doc ::" , i)
                
                embading=self.embedding_model.encode(doc)
                self.add_document(doc , embading , meta_data[doc])
        else:
            raise ValueError("docs and meta_data must be of same length")    
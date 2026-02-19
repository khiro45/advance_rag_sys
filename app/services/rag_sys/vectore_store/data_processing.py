from abc import ABC, abstractmethod

processors_lits={
    
}

class Docs_processor(ABC):

    def __init__(self):
        pass

    def process_docs(self , docs:list[str] , meta_data:list[dict]):
        pass

    def chunk_docs(self , docs:list[str] , meta_data:list[dict]):
        pass

    def run_processor(self , processor_type:str):
        doc_processor=processors_lits.get(processor_type)
        if doc_processor:
            return doc_processor()
        else:
            raise ValueError("processor type not found")
from abc import ABC, abstractmethod


class BaseDocProcessor(ABC):

    @abstractmethod
    def load_doc(self , docs:str , meta_data:dict):
        """Steps to load docs"""
        pass
    @abstractmethod
    def process_doc(self , docs:str , meta_data:dict):
        """Steps to clean or extract text"""
        pass
    @abstractmethod
    def chunk_docs(self , docs:str , meta_data:str):
        """Steps to chunk docs"""
        pass

    def run_pipline(self, docs: list[str], meta_data: list[dict]):
        processed = self.process_docs(docs, meta_data)
        chunks = self.chunk_docs(processed, meta_data)

class ProcessorFactory:
    _processors = {
        # "pdf": PDFProcessor,
        # "md": MarkdownProcessor,
        # "txt": MarkdownProcessor 
    }

    @staticmethod
    def get_processor(processor_type: str) -> BaseDocProcessor:
        processor_class = ProcessorFactory._processors.get(processor_type.lower())
        if not processor_class:
            raise ValueError(f"No processor found for type: {processor_type}")
        
        return processor_class()
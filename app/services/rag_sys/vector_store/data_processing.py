from app.services.rag_sys.vector_store.base_processor import BaseDocProcessor
from app.services.rag_sys.vector_store.data_processors.general_pdf_processor import GneralPDFProcessor
from pydantic import BaseModel
from enum import Enum



class ProcessorType(str, Enum):
    PDF = "pdf"



class ProcessorFactory:
    _processors = {
        "pdf": GneralPDFProcessor,
    }

    @staticmethod
    def get_processor(processor_type: str) -> BaseDocProcessor:
        processor_class = ProcessorFactory._processors.get(processor_type.lower())
        if not processor_class:
            raise ValueError(f"No processor found for type: {processor_type}")
        
        return processor_class()
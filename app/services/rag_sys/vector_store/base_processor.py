from abc import ABC, abstractmethod
from fastapi import UploadFile
from app.services.rag_sys.schemas import BaseMetaData
from typing import Tuple, List

class BaseDocProcessor(ABC):
    @abstractmethod
    async def load_doc(self, file: UploadFile, meta_data: BaseMetaData) -> Tuple[List[str], BaseMetaData]:
        """Steps to load docs and extract raw text from each page/section."""
        pass

    @abstractmethod
    def process_doc(self, texts: List[str], meta_data: BaseMetaData) -> Tuple[List[str], BaseMetaData]:
        """Steps to clean or normalize extracted text."""
        pass

    @abstractmethod
    def chunk_docs(self, texts: List[str], meta_data: BaseMetaData) -> Tuple[List[str], List[dict]]:
        """Steps to chunk docs and return list of text chunks and list of metadata dicts."""
        pass
   
    @abstractmethod
    async def run_pipeline(self, file: UploadFile, meta_data: BaseMetaData) -> Tuple[List[str], List[dict]]:
        """Runs the complete ingestion pipeline."""
        texts, meta_data = await self.load_doc(file, meta_data)
        cleaned_texts, meta_data = self.process_doc(texts, meta_data)
        return self.chunk_docs(cleaned_texts, meta_data)



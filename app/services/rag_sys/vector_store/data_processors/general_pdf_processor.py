from app.services.rag_sys.vector_store.data_processing import BaseDocProcessor
import pypdf 
from fastapi import File  , HTTPException
from pypdf import PdfReader
import io
from app.services.rag_sys.schemas import BaseMetaData
from typing import Tuple


class GneralPDFProcessor(BaseDocProcessor):
    async def load_doc(self, file:File, meta_data:BaseMetaData)-> Tuple[list[str] ,BaseMetaData] :
        if file.content_type != "application/pdf":
            raise HTTPException(status_code=400, detail=f"The provided file match the curnt  prossorr {file.content_type}")
        
        file_bytes = await file.read()

        pdf_stream = io.BytesIO(file_bytes)
        reader = PdfReader(pdf_stream)
        texts = reader.pages
        meta_data.source = file.filename
        return texts , meta_data



    def run_pipline(self, file:File, meta_data:BaseMetaData):
        return self.load_doc(file  , meta_data)
from pydantic import BaseModel, Field
from typing import List, Optional
from app.services.rag_sys.schemas import BaseMetaData
class RagQueryRequest(BaseModel):
    query: str = Field(..., example="What is the main topic of the documents?")
    n_results: Optional[int] = Field(5, description="Number of documents to retrieve per sub-query")

class RagQueryResponse(BaseModel):
    answer: str

class ChatInput(BaseModel):

    message:str 
    session_id :str

class RagIngestRequest(BaseModel):
    title: Optional[str]
    metadata: BaseMetaData

class RagIngestResponse(BaseModel):
    status: str
    count: int

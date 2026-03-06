from pydantic import BaseModel, Field
from typing import List, Optional

class RagQueryRequest(BaseModel):
    query: str = Field(..., example="What is the main topic of the documents?")
    n_results: Optional[int] = Field(5, description="Number of documents to retrieve per sub-query")

class RagQueryResponse(BaseModel):
    answer: str

class RagIngestRequest(BaseModel):
    documents: List[str]
    metadata: List[dict] = Field(default_factory=list)

class RagIngestResponse(BaseModel):
    status: str
    count: int

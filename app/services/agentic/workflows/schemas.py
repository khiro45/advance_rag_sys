from pydantic import BaseModel
from typing import List, Dict, Any



## schemas 
class SubQuery(BaseModel):
    sub_queries: list[str]
    keywords: list[str]
    tags: list[str]

class SubQueries(BaseModel):
    sub_queries: list[SubQuery]



## tools schemas

class ToolSchemaRetrieveDocuments(BaseModel):
    query: str
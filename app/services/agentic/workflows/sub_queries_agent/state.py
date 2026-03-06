from typing import List, Dict, Any, TypedDict
from app.services.rag_sys.schemas import BaseMetaData
from pydantic import BaseModel

## sub query state

class SubQuery(BaseModel):
    query: str
    meta_data: BaseMetaData

class SubQueryState(TypedDict):
    user_query: str
    sub_queries: list[SubQuery]


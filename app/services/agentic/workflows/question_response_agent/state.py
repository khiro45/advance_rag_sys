from typing import TypedDict, Annotated
from langgraph.graph.message import add_messages
from pydantic import BaseModel
from app.services.rag_sys.schemas import BaseMetaData

class SubQuery(BaseModel):
    query: str
    # meta_data: BaseMetaData

class QuestionResponseState(TypedDict):
    user_query:str
    sub_querys:list[SubQuery]
    message: str
    docs: list[dict]
from typing import List, Dict, Any 
from pydantic import BaseModel


class Sub_query_State():
    query: str
    sub_querys: list[str]
    metadata: Dict[str, Any]



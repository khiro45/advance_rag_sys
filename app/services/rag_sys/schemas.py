from pydantic import BaseModel
from typing import List , Dict , Any
from datetime import datetime


class BaseMetaData(BaseModel):
    source:str
    date:datetime
    title:str
    tags:List[str]
    keywords:list[str]
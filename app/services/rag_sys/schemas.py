from pydantic import BaseModel
from typing import List , Dict , Any
from datetime import datetime


class BaseMetaData(BaseModel):
    processor_type:str
    source:str
    date:datetime
    title:str
    tags:List[str]| None
    keywords:list[str]|None
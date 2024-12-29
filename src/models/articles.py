from pydantic import BaseModel
from typing import Optional,List


class Article(BaseModel): 
    id                : int
    title             : str
    content           : str
    author_id         : str
    publication_id    : str


class Person(BaseModel): 
    id               : int
    name             : str
    writes_about     : List[str]
    bio              : Optional[str] = None


class Publication(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    

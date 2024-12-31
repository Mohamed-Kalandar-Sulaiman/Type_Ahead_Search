from pydantic import BaseModel
from typing import Optional,List


class Article(BaseModel): 
    id                : str
    title             : str
    tags              : List[str]
    created_on        : str
    author_id         : str
    publication_id    : Optional [str]= None
    likes             : int
    dislikes          : int
 

class Person(BaseModel): 
    id               : str
    name             : str
    writes_about     : List[str]
    followers        : int


class Publication(BaseModel): 
    id                    : str
    name                  : str
    tags                  : List[str]
    description           : Optional[str] = None
    subscribers           : int
    authors               : List[str]
      
    
class History(BaseModel): 
    id     : str
    prefix : str
    user_id: str
    date   : str
    
    
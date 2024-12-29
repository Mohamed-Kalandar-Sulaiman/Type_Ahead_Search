from pydantic import BaseModel, Field
from typing import Optional, Dict, List
from fastapi import Request

class Post(BaseModel): 
    id             : str = Field("Elastic serach with python", description="The search term or phrase.")
    title          : Optional[str] = Field(None, description="Configuration options for the search, such as filters or sorting preferences.")
    author         : Optional[str] = Field(None, description="The cursor key for fetching the next set of results.")
    created_on     : Optional[int] = Field(10, ge=1, le=100, description="The number of results to return per page.")

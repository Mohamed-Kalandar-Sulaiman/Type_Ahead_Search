from pydantic import BaseModel, Field
from typing import Optional, Dict, List
from fastapi import Request

class SearchRequest(BaseModel): 
      query                   : str = Field("Elastic serach with python", description="The search term or phrase.")
      config                  : Optional[str] = Field(None, description="Configuration options for the search, such as filters or sorting preferences.")
      page_key                : Optional[str] = Field(None, description="The cursor key for fetching the next set of results.")
      page_size               : Optional[int] = Field(10, ge=1, le=100, description="The number of results to return per page.")






class SearchResponse(BaseModel): 
      history                  : Optional[List[str]] = Field(default=["golang", "python", "docker"], description="Results from search history")
      fuzzy                    : Optional[List[str]] = Field(default=None, description="Fuzzy results based on search query")
      nextPageKey              : Optional[str] = Field(default=None, description="Next page key which has to be used to fetche next set of results")
      
      
class ErrorResponse(BaseModel): 
      errorCode               : int = Field(default=400, description="Status code")
      errorMessage            : str = Field( default="Bad Request Error", description="Errro description")
      
      
      
import ulid 
import time
from fastapi.responses import JSONResponse
from fastapi import Response, Request, HTTPException
from fastapi import Path,Query

from src.schemas.search_schema import ErrorResponse 

from src.schemas.search_schema import SearchRequest

async def staticSearchHandler(request:SearchRequest):
    q = dict(request)
    return JSONResponse(status_code=200, content=q)






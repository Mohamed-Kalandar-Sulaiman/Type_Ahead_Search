import ulid 
import time
from fastapi.responses import JSONResponse
from fastapi import Response, Request, HTTPException
from fastapi import Path,Query

from src.schemas.search_schema import ErrorResponse 
from src.schemas.search_schema import SearchRequest

import ulid
import datetime


from src.database import ElasticsearchClient
from src.repository import *



es_client    = ElasticsearchClient()
history_repo = HistoryRepository(es_client = es_client)


async def LogHistory(request:Request, prefix ):
    '''
    Write entry into search history
    '''
    try:
        id             = ulid.ulid()
        date           = datetime.datetime.now()
        formatted_date = date.strftime("%Y-%m-%dT%H:%M:%S") + 'Z'
        await history_repo.create_new_search_history(id=id, prefix=prefix, date=formatted_date, user_id = request.state.user)
    except Exception as e:
        #! On failure Write into queue
        print(e)
        pass

async def AnalyticsService(prefix):
    pass


async def staticSearchHandler(request:Request):
    #! Rate Limit search requests
    
    #! Validate input args
    request_payload      = await request.json()
    request_query_params = dict(request.query_params)
    prefix               = request_payload.get("prefix")
    
    
    #! Fetch data
    response = history_repo.search_latest_history(userId=None)
    #! Write into history cluster and analytics service topic
    LogHistory(request=request, prefix=prefix)
    AnalyticsService(prefix)
    return JSONResponse(status_code=200,
                        content=response)






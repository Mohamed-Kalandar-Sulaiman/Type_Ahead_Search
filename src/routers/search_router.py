import asyncio
from fastapi import APIRouter
from typing import Optional, Dict, List

from src.handlers.type_ahead_search_handler import typeAheadSearchHandler
from src.handlers.static_search_handler import staticSearchHandler


from fastapi import APIRouter
from fastapi.responses import JSONResponse, HTMLResponse

from src.schemas.search_schema import SearchRequest , SearchResponse

searchRouter = APIRouter(prefix="/search")


searchRouter.add_api_websocket_route(path       = "/typeahead",
                                     endpoint   = typeAheadSearchHandler,
                                     name       = "Get realtime search results and suggestions via Websockets"
                                    )



searchRouter.add_api_route(path              = "/",
                           response_class         = JSONResponse,
                           response_model         = SearchResponse,
                           status_code            = 200,
                           methods                = ["POST"],
                           description            = "REST API endponit to handle detailed search results.",
                           name                   = "Search API",
                           endpoint               = staticSearchHandler
                           )


from fastapi import FastAPI, Depends, APIRouter
from src.repository import *
from src.routers.search_router import searchRouter
from src.middlewares import AuthMiddleware, LoggingMiddleware, CorsMiddleware


app = FastAPI(title="TypeAheadSearch", version="1.0.0")

#! Include API routers
api = APIRouter(prefix="/api/v1", tags=[])

api.include_router(searchRouter, tags=["Search"])
app.include_router(api)

app.add_middleware(CorsMiddleware)
app.add_middleware(LoggingMiddleware)
# app.add_middleware(AuthMiddleware)



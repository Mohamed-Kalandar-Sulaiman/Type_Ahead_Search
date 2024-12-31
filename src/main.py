from fastapi import FastAPI, Depends, APIRouter

from dotenv import load_dotenv

import os
from pathlib import Path

from src.database import ElasticsearchClient

from src.repository import *
from src.routers.search_router import searchRouter
from src.middlewares import AuthMiddleware, LoggingMiddleware, CorsMiddleware

async def lifespan(app: FastAPI):
    ENV_FILE_PATH = Path(__file__).resolve().parent.parent /  ".env"
    print(ENV_FILE_PATH)
    load_dotenv(dotenv_path=ENV_FILE_PATH)
    ES_HOST = os.getenv("ES_HOST")
    ES_PORT = os.getenv("ES_PORT")
    
    print(f"Elasticsearch Host: {ES_HOST} {ES_PORT}")
    es = ElasticsearchClient()
    await es.check_connection()
    yield
    
    print("Shutdown: Cleaning up resources if necessary")
    es.close()


app = FastAPI(title="TypeAheadSearch", version="1.0.0",lifespan=lifespan)

#! Include API routers
api = APIRouter(prefix="/api/v1", tags=[])

api.include_router(searchRouter, tags=["Search"])

app.include_router(api)

app.add_middleware(CorsMiddleware)
app.add_middleware(LoggingMiddleware)
app.add_middleware(AuthMiddleware)



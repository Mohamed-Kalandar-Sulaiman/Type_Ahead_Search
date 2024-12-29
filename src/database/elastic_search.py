from elasticsearch import Elasticsearch
from elasticsearch.exceptions import ConnectionError, NotFoundError
from elasticsearch.client import IndicesClient
import os
import time
from fastapi import HTTPException

ES_HOST     = os.getenv("ES_HOST")
ES_PORT     = os.getenv("ES_PORT")
ES_USER     = os.getenv("ES_USER")
ES_PASSWORD = os.getenv("ES_PASSWORD")


def get_es_client():
    try:
        es_client = Elasticsearch(
                                [f"http://{ES_HOST}:{ES_PORT}"],
                                http_auth        = (ES_USER, ES_PASSWORD) if ES_USER and ES_PASSWORD else None,
                                max_retries      = 3,
                                retry_on_timeout = True,
                                timeout          = 10,                                                          
                            )

        if es_client.ping():
            print("Connected to Elasticsearch")
            return es_client
        else:
            raise HTTPException(status_code=500, detail="Failed to ping Elasticsearch")
    
    except (ConnectionError, Exception) as e:
        raise HTTPException(status_code=500, detail=f"Error connecting to Elasticsearch: {str(e)}")


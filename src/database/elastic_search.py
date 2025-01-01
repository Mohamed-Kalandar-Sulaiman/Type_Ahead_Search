import os
from elasticsearch import AsyncElasticsearch, NotFoundError, ConnectionError as ESConnectionError
from fastapi import HTTPException
from typing import Dict, Any
from src.utilities import Logger
logger = Logger(name=__name__)

class ElasticsearchClient:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
            cls._instance.initialize()
        return cls._instance

    def initialize(self):
        """Initialize Elasticsearch client with environment variables."""
        self.ES_HOST = os.getenv("ES_HOST", "localhost")
        self.ES_PORT = os.getenv("ES_PORT", "9200")
        self.ES_USER = os.getenv("ES_USER")
        self.ES_PASSWORD = os.getenv("ES_PASSWORD")
        self.client = None
        self.connect()

    def connect(self):
        """Establish a connection to Elasticsearch."""
        try:
            self.client = AsyncElasticsearch(
                hosts=[{"host": self.ES_HOST, "port": int(self.ES_PORT), "scheme": "http"}],
                http_auth=(self.ES_USER, self.ES_PASSWORD) if self.ES_USER and self.ES_PASSWORD else None,
                max_retries=3,
                retry_on_timeout=True,
                timeout=10,
            )
            logger.info("Initialized AsyncElasticsearch client.")
        except Exception as e:
            logger.error(f"Error initializing Elasticsearch client: {e}")
            raise HTTPException(status_code=500, detail=f"Error initializing Elasticsearch client: {str(e)}")
    def close(self):
        try:
            self.client.close()
        except Exception as e:
            logger.critical(f"Error occured while closing connection {e}")
            

    async def check_connection(self):
        """Ping the Elasticsearch server to ensure the connection is alive."""
        try:
            if not await self.client.ping():
                raise ESConnectionError("Elasticsearch ping failed.")
            logger.info("Elasticsearch ping successful.")
        except Exception as e:
            logger.critical(f"Error pinging Elasticsearch: {e}")
            raise HTTPException(status_code=500, detail=f"Error pinging Elasticsearch: {str(e)}")

    async def index_document(self, index: str, doc_id: str, document: Dict[str, Any]) -> Dict[str, Any]:
        """Index a document into Elasticsearch."""
        try:
            response = await self.client.index(index=index, id=doc_id, document=document)
            return response
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error indexing document: {str(e)}")

    async def search_documents(self, index: str, query: Dict[str, Any]) -> Any:
        """Search documents in Elasticsearch."""
        try:
            response = await self.client.search(index=index, body=query)
            return [hit["_source"] for hit in response["hits"]["hits"]]
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error searching documents: {str(e)}")

    async def get_document_by_id(self, index: str, doc_id: str) -> Dict[str, Any]:
        """Get a document by its ID."""
        try:
            response = await self.client.get(index=index, id=doc_id)
            return response["_source"]
        except NotFoundError:
            raise HTTPException(status_code=404, detail="Document not found")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error retrieving document: {str(e)}")

    async def delete_document(self, index: str, doc_id: str) -> Dict[str, Any]:
        """Delete a document from Elasticsearch by ID."""
        try:
            response = await self.client.delete(index=index, id=doc_id)
            return response
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error deleting document: {str(e)}")

    async def create_index(self, index: str, settings: Dict[str, Any]) -> Dict[str, Any]:
        """Create an index in Elasticsearch with specific settings."""
        try:
            response = await self.client.indices.create(index=index, body=settings, ignore=400)
            return response
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error creating index: {str(e)}")

    
    
    async def get_suggestions(self, query: Dict[str, Any], index:str) -> Any:
        """Get type-ahead suggestions from Elasticsearch."""
        try:
            # Perform the suggestion query on the 'wugsgsets' index
            response = await self.client.search(index=index, body=query)
            
            # Extract suggestions if the response contains 'suggest'
            if 'suggest' in response:
                suggestions = []
                for suggestion in response['suggest'][index][0]['options']:
                    suggestions.append({
                        'text'  : suggestion['text'],
                        'score' : suggestion['_score'],
                        '_id'   : suggestion['_id']                    })
                return suggestions
            else:
                raise HTTPException(status_code=404, detail="No suggestions found")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error retrieving suggestions: {str(e)}")
    
    


def get_es_client() -> ElasticsearchClient:
    """Get the singleton Elasticsearch client."""
    return ElasticsearchClient()

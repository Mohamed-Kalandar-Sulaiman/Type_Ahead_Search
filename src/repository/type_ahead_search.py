from elasticsearch import Elasticsearch, NotFoundError
from fastapi import HTTPException
from typing import Dict, Any

class ElasticsearchRepository:
    def __init__(self, es_client: Elasticsearch):
        self.es_client = es_client

    def index_document(self, index: str, doc_id: str, document: Dict[str, Any]) -> Dict[str, Any]:
        """Index a document into Elasticsearch."""
        try:
            response = self.es_client.index(index=index, id=doc_id, document=document)
            return response
        except ConnectionError as e:
            raise HTTPException(status_code=500, detail=f"Connection error while indexing: {str(e)}")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error indexing document: {str(e)}")

    def search_documents(self, index: str, query: Dict[str, Any], size: int = 10) -> Any:
        """Search documents in Elasticsearch."""
        try:
            response = self.es_client.search(index=index, body=query, size=size)
            return [hit["_source"] for hit in response["hits"]["hits"]]
        except ConnectionError as e:
            raise HTTPException(status_code=500, detail=f"Connection error while searching: {str(e)}")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error searching documents: {str(e)}")

    def get_document_by_id(self, index: str, doc_id: str) -> Dict[str, Any]:
        """Get a document by its ID."""
        try:
            response = self.es_client.get(index=index, id=doc_id)
            return response["_source"]
        except NotFoundError:
            raise HTTPException(status_code=404, detail="Document not found")
        except ConnectionError as e:
            raise HTTPException(status_code=500, detail=f"Connection error while retrieving document: {str(e)}")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error getting document: {str(e)}")

    def delete_document(self, index: str, doc_id: str) -> Dict[str, Any]:
        """Delete a document from Elasticsearch by ID."""
        try:
            response = self.es_client.delete(index=index, id=doc_id)
            return response
        except ConnectionError as e:
            raise HTTPException(status_code=500, detail=f"Connection error while deleting: {str(e)}")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error deleting document: {str(e)}")

    def create_index(self, index: str, settings: Dict[str, Any]) -> Dict[str, Any]:
        """Create an index in Elasticsearch with specific settings."""
        try:
            response = self.es_client.indices.create(index=index, body=settings, ignore=400)
            return response
        except ConnectionError as e:
            raise HTTPException(status_code=500, detail=f"Connection error while creating index: {str(e)}")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error creating index: {str(e)}")

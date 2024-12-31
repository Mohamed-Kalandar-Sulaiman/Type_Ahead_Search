from elasticsearch import Elasticsearch, NotFoundError
from fastapi import HTTPException
from typing import Dict, Any

from src.utilities import ElasticsearchQueryBuilder
from src.database import ElasticsearchClient


class ArticlesRepository:
    def __init__(self, es_client:ElasticsearchClient):
        self.es_client = es_client
        self.index     = "articles"

    async def search_articles_on_title(self, prefix)->list:
        query   = ElasticsearchQueryBuilder()
        query.add_match(field="title", value=prefix)
        query.add_source(fields=["id", "title", "tags"])
        query.add_size(size=5)
        
        try:
            response =  await self.es_client.search_documents(index=self.index, query=query.query)
            return response
        except Exception as e:
            print(e)
            return []
    
    async def search_articles_by_fuzzy(self,prefix):
        query   = ElasticsearchQueryBuilder()
        query.add_fuzzy(field="title", value=prefix, fuzziness= 0.5)
        query.add_source(fields=["id", "title", "tags"])
        query.add_size(size=5)
        try:
            response =   await self.es_client.search_documents(index=self.index, query=query.query)
            return response
        except Exception as e:
            print(e)
            return []
    
    async def search_articles_by_prefix(self,prefix):
        query   = ElasticsearchQueryBuilder()
        query.add_prefix(field="title", value=prefix)
        query.add_source(fields=["id", "title", "tags"])
        query.add_size(size=5)
        try:
            response =  await self.es_client.search_documents(index=self.index, query=query.query)
            return response
        except Exception as e:
            print(e)
            return []
        
        
    async def search_articles_on_tags(self,prefix):
        query   = ElasticsearchQueryBuilder()
        query.add_term(field="tags", value=prefix)
        query.add_source(fields=["id", "title", "tags"])
        query.add_size(size=5)

        try:
            response =  await self.es_client.search_documents(index=self.index, query=query.query)
            return response
        except Exception as e:
            print(e)
            return []
        
    async def suggestion(self,prefix):
        try:
            query = {
                "suggest":{
                    self.index :{
                        "prefix":prefix,
                        "completion":{
                            "field":"suggest_title",
                            "size":5
                        }
                    }
                }
            }
                    
            response =  await self.es_client.get_suggestions(index=self.index, query=query)
            return response
        except Exception as e:
            print(e)
            return [] 
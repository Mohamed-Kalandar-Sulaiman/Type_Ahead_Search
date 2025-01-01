from fastapi import HTTPException
from typing import Dict, Any
import json
import asyncio

from src.utilities import ElasticsearchQueryBuilder
from src.database import ElasticsearchClient


from .base_repository import BaseRepository


class ArticlesRepository(BaseRepository):
    def __init__(self):
        super().__init__()
        self.es_client    = ElasticsearchClient()
        self.index        = "articles"
        
    
        

    async def search_articles_on_title(self, prefix)->list:
        #! Check from cache
        key = f"{self.index}:search_articles_on_title:{prefix}"
        response ,    isCached = await self.read_from_cache(key=key)
        if isCached:
            return response
        #! Cache miss > Query ES
        query   = ElasticsearchQueryBuilder()
        query.add_match(field="title", value=prefix)
        query.add_source(fields=["id", "title", "tags"])
        query.add_size(size=5)
        
        try:
            response =  await self.es_client.search_documents(index=self.index, query=query.query)
            asyncio.create_task(self.write_back_into_cache(key=key, value=response))
            return response
        except Exception as e:
            print(e)
            return []
    
    
    async def search_articles_by_fuzzy(self,prefix):
        #! Check from cache
        key = f"{self.index}:search_articles_by_fuzzy:{prefix}"
        response ,    isCached = await self.read_from_cache(key=key)
        if isCached:
            return response
        #! Cache miss > Query ES
        query   = ElasticsearchQueryBuilder()
        query.add_fuzzy(field="title", value=prefix, fuzziness= 0.5)
        query.add_source(fields=["id", "title", "tags"])
        query.add_size(size=5)
        try:
            response =   await self.es_client.search_documents(index=self.index, query=query.query)
            asyncio.create_task(self.write_back_into_cache(key=key, value=response))
            return response
        except Exception as e:
            print(e)
            return []
    
    async def search_articles_by_prefix(self,prefix):
        #! Check from cache
        key = f"{self.index}:search_articles_by_prefix:{prefix}"
        response ,    isCached = await self.read_from_cache(key=key)
        if isCached:
            return response
        #! Cache miss > Query ES
        query   = ElasticsearchQueryBuilder()
        query.add_prefix(field="title", value=prefix)
        query.add_source(fields=["id", "title", "tags"])
        query.add_size(size=5)
        try:
            response =  await self.es_client.search_documents(index=self.index, query=query.query)
            asyncio.create_task(self.write_back_into_cache(key=key, value=response))
            return response
        except Exception as e:
            print(e)
            return []
        
        
    async def search_articles_on_tags(self,prefix):
        #! Check from cache
        key = f"{self.index}:search_articles_on_tags:{prefix}"
        response ,    isCached = await self.read_from_cache(key=key)
        if isCached:
            return response
        #! Cache miss > Query ES
        query   = ElasticsearchQueryBuilder()
        query.add_term(field="tags", value=prefix)
        query.add_source(fields=["id", "title", "tags"])
        query.add_size(size=5)

        try:
            response =  await self.es_client.search_documents(index=self.index, query=query.query)
            asyncio.create_task(self.write_back_into_cache(key=key, value=response))
            return response
        except Exception as e:
            print(e)
            return []
        
    async def suggestion(self,prefix):
        #! Check from cache
        key = f"{self.index}:suggestion:{prefix}"
        response ,    isCached = await self.read_from_cache(key=key)
        if isCached:
            return response
        #! Cache miss > Query ES
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
            asyncio.create_task(self.write_back_into_cache(key=key, value=response))
            return response
        except Exception as e:
            print(e)
            return [] 
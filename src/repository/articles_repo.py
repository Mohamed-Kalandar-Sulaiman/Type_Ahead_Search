from fastapi import HTTPException
from typing import Dict, Any
import json
import asyncio

from src.utilities import ElasticsearchQueryBuilder
from src.database import ElasticsearchClient, RedisClient


class ArticlesRepository:
    def __init__(self):
        self.es_client    = ElasticsearchClient()
        self.redis_client = RedisClient()
        self.index        = "articles"
        
    async def read_from_cache(self,key):
        key = self.index + key
        try:
            response = await self.redis_client.get_value(key=key)
            if response is not None: 
                print(f"CACHE HIT {key} ")
                return json.loads(response), True
            else:
                print(f"CACHE MISS {key} ")
                return None, False
        except Exception as e:
            return None , False
        
    async def write_back_into_cache(self,key, value, ttl=None)->None:
        key = self.index + key
        try:
            value    = json.dumps(value)
            await self.redis_client.set_value(key=key, value=value, ttl=60)
            print(f"Wriiten into redis ->  {key}")
        except Exception as e:
            return 
        

    async def search_articles_on_title(self, prefix)->list:
        #! Try getting from redis
        key = f":search_articles_on_title:{prefix}"
        response ,    isCached = await self.read_from_cache(key=key)
        if isCached:
            return response
        
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
        key = f":search_articles_by_fuzzy:{prefix}"
        response ,    isCached = await self.read_from_cache(key=key)
        if isCached:
            return response
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
        key = f":search_articles_by_prefix:{prefix}"
        response ,    isCached = await self.read_from_cache(key=key)
        if isCached:
            return response
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
        key = f":search_articles_on_tags:{prefix}"
        response ,    isCached = await self.read_from_cache(key=key)
        if isCached:
            return response
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
        key = f":suggestion:{prefix}"
        response ,    isCached = await self.read_from_cache(key=key)
        if isCached:
            return response
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
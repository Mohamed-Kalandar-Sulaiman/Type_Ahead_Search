
from src.utilities import ElasticsearchQueryBuilder
from src.database import ElasticsearchClient

import asyncio 

from .base_repository import BaseRepository

class PublicationsRepository(BaseRepository):
    def __init__(self):
        super().__init__()
        self.es_client = ElasticsearchClient()
        self.index     = "publications"

    async def search_publications_by_name(self, prefix)->list:
        #! Check from cache
        key = f"{self.index}:search_publications_by_name:{prefix}"
        response ,    isCached = await self.read_from_cache(key=key)
        if isCached:
            return response
        #! Cache miss > Query ES
        query   = ElasticsearchQueryBuilder()
        query.add_match(field="name", value=prefix)
        query.add_source(fields=["id", "name", "tags"])
        query.add_size(size=5)
        
        try:
            response =  await self.es_client.search_documents(index=self.index, query=query.query)
            asyncio.create_task(self.write_back_into_cache(key=key, value=response))
            return response
        except Exception as e:
            print(e)
            return []
    # publications
    
    
    async def search_publications_by_name_fuzzy(self,prefix):
        #! Check from cache
        key = f"{self.index}:search_publications_by_name_fuzzy:{prefix}"
        response ,    isCached = await self.read_from_cache(key=key)
        if isCached:
            return response
        #! Cache miss > Query ES
        query   = ElasticsearchQueryBuilder()
        query.add_fuzzy(field="name", value=prefix, fuzziness= 0.5)
        query.add_source(fields=["id", "name", "tags"])
        query.add_size(size=5)
        try:
            response =   await self.es_client.search_documents(index=self.index, query=query.query)
            asyncio.create_task(self.write_back_into_cache(key=key, value=response))
            return response
        except Exception as e:
            print(e)
            return []
    
    async def search_publications_by_tags(self,prefix):
        #! Check from cache
        key = f"{self.index}:search_publications_by_tags:{prefix}"
        response ,    isCached = await self.read_from_cache(key=key)
        if isCached:
            return response
        #! Cache miss > Query ES
        query   = ElasticsearchQueryBuilder()
        query.add_prefix(field="tags", value=prefix)
        query.add_source(fields=["id", "name", "tags"])
        query.add_size(size=5)
        try:
            response =  await self.es_client.search_documents(index=self.index, query=query.query)
            asyncio.create_task(self.write_back_into_cache(key=key, value=response))
            return response
        except Exception as e:
            print(e)
            return []
        
     
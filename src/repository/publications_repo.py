
from src.utilities import ElasticsearchQueryBuilder
from src.database import ElasticsearchClient


class PublicationsRepository:
    def __init__(self):
        self.es_client = ElasticsearchClient()
        self.index     = "publications"

    async def search_publications_by_name(self, prefix)->list:
        query   = ElasticsearchQueryBuilder()
        query.add_match(field="name", value=prefix)
        query.add_source(fields=["id", "name", "tags"])
        query.add_size(size=5)
        
        try:
            response =  await self.es_client.search_documents(index=self.index, query=query.query)
            return response
        except Exception as e:
            print(e)
            return []
    # publications
    async def search_publications_by_name_fuzzy(self,prefix):
        query   = ElasticsearchQueryBuilder()
        query.add_fuzzy(field="name", value=prefix, fuzziness= 0.5)
        query.add_source(fields=["id", "name", "tags"])
        query.add_size(size=5)
        try:
            response =   await self.es_client.search_documents(index=self.index, query=query.query)
            return response
        except Exception as e:
            print(e)
            return []
    
    async def search_publications_by_tags(self,prefix):
        query   = ElasticsearchQueryBuilder()
        query.add_prefix(field="tags", value=prefix)
        query.add_source(fields=["id", "name", "tags"])
        query.add_size(size=5)
        try:
            response =  await self.es_client.search_documents(index=self.index, query=query.query)
            return response
        except Exception as e:
            print(e)
            return []
        
     
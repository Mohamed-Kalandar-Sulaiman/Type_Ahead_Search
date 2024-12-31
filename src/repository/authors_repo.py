
from src.utilities import ElasticsearchQueryBuilder
from src.database import ElasticsearchClient


class AuthorsRepository:
    def __init__(self, es_client:ElasticsearchClient):
        self.es_client = es_client
        self.index     = "authors"

    async def search_authors_by_name(self, prefix)->list:
        query   = ElasticsearchQueryBuilder()
        query.add_match(field="name", value=prefix)
        query.add_source(fields=["id", "name", "writes_about"])
        query.add_size(size=5)
        
        try:
            response =  await self.es_client.search_documents(index=self.index, query=query.query)
            return response
        except Exception as e:
            print(e)
            return []
    
    async def search_authors_by_name_fuzzy(self,prefix):
        query   = ElasticsearchQueryBuilder()
        query.add_fuzzy(field="name", value=prefix, fuzziness= 0.5)
        query.add_source(fields=["id", "name", "writes_about"])
        query.add_size(size=5)
        try:
            response =   await self.es_client.search_documents(index=self.index, query=query.query)
            return response
        except Exception as e:
            print(e)
            return []
    
    async def search_articles_by_prefix(self,prefix):
        query   = ElasticsearchQueryBuilder()
        query.add_prefix(field="name", value=prefix)
        query.add_source(fields=["id", "name", "writes_about"])
        query.add_size(size=5)
        try:
            response =  await self.es_client.search_documents(index=self.index, query=query.query)
            return response
        except Exception as e:
            print(e)
            return []
        
        
    async def search_articles_on_writes_about(self,prefix):
        query   = ElasticsearchQueryBuilder()
        query.add_term(field="writes_about", value=prefix)
        query.add_source(fields=["id", "name", "writes_about"])
        query.add_size(size=5)

        try:
            response =  await self.es_client.search_documents(index=self.index, query=query.query)
            return response
        except Exception as e:
            print(e)
            return []
        
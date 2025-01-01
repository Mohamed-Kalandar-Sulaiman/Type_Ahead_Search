
from src.utilities import ElasticsearchQueryBuilder
from src.database import ElasticsearchClient


class HistoryRepository:
    def __init__(self):
        self.es_client = ElasticsearchClient()
        self.index     = "search_history"

    async def search_latest_history(self, userId)->list:
        query   = ElasticsearchQueryBuilder()
        query.add_match(field="user_id", value=userId)
        query.add_sort(field="date", order="desc")
        query.add_source(fields=["id", "date", "prefix"])
        query.add_size(size=5)
        
        
        try:
            response =  await self.es_client.search_documents(index=self.index, query=query.query)
            return response
        except Exception as e:
            print(e)
            return []

    async def create_new_search_history(self,**kwargs)->bool:
        try:
            response = await self.es_client.index_document(
                                                        index    = self.index,
                                                        doc_id   = kwargs.get("id"),
                                                        document = {
                                                                            "id"     : kwargs.get("id"),
                                                                            "date"   : kwargs.get("date"),
                                                                            "prefix" : kwargs.get("prefix"),
                                                                            "user_id": kwargs.get("user_id")
                                                                    })
            if response["result"] == "created":
                return True
        
        except Exception as e:
            print(e)
            return False
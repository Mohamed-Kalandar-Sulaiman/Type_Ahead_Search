import asyncio

from fastapi import WebSocket, WebSocketDisconnect
from fastapi.websockets import WebSocketState
from src.schemas.search_schema import SearchRequest

from src.repository import ArticlesRepository, AuthorsRepository, PublicationsRepository, HistoryRepository
from src.utilities import WebSocketAuthMiddleware



articles_repo    = ArticlesRepository()
authors_repo     = AuthorsRepository()
publictaions_reo = PublicationsRepository()
history_repo     = HistoryRepository()


def flatten_and_clean_data(data):
    flattened_articles     = [article for articles in data['articles'] if articles for article in articles]
    flattened_authors      = [author for authors in data['authors'] if authors for author in authors]
    flattened_publications = [publication for publications in data['publications'] if publications for publication in publications]

    cleaned_data = {
        "articles"    : flattened_articles,
        "authors"     : flattened_authors,
        "publications": flattened_publications,
        "suggestions" : data.get("suggestions")
    }

    return cleaned_data

async def getSearchResults(prefix:str, userId :str)-> dict:
    results = dict()
    if len(prefix) ==0:
        #! Search history if query len(prefix) == 0
        
        results["history"] = await history_repo.search_latest_history(userId=userId)
        return results
    
    suggestions :list[list] = await articles_repo.suggestion(prefix=prefix)
    articles :list[list]    = await asyncio.gather(
                                                articles_repo.search_articles_on_title(prefix=prefix),
                                                articles_repo.search_articles_by_fuzzy(prefix=prefix),
                                                articles_repo.search_articles_by_prefix(prefix=prefix),
                                                articles_repo.search_articles_on_tags(prefix=prefix),
                                            )
   
    #! Search authors
    authors :list[list] = await asyncio.gather(
                                                authors_repo.search_articles_by_prefix(prefix=prefix),
                                                authors_repo.search_articles_on_writes_about(prefix=prefix),
                                                authors_repo.search_authors_by_name(prefix=prefix),
                                                authors_repo.search_authors_by_name_fuzzy(prefix=prefix)
                                            )
    #! Search publications

    publications :list[list] = await asyncio.gather(
                                            publictaions_reo.search_publications_by_name(prefix=prefix),
                                            publictaions_reo.search_publications_by_name_fuzzy(prefix=prefix),
                                            publictaions_reo.search_publications_by_tags(prefix=prefix)
                                            )

    

    #! Remove Duplicates
    results["suggestions"]  = suggestions
    results["articles"]     = articles
    results["authors"]      = authors
    results["publications"] = publications
    
    return flatten_and_clean_data(results)


async def typeAheadSearchHandler(websocket: WebSocket):
    
    """WebSocket endpoint for the game, handling real-time communication."""
    await websocket.accept()
    print(f"New user is connected !!")
    
    #! Autheticate user 
    try:
        userId = await WebSocketAuthMiddleware(websocket=websocket)
        print(f"Authenticated userId: {userId}")
    except WebSocketDisconnect as e:
        await websocket.send_json({"error": str(e)})
        await websocket.close(code=1002, reason=str(e))  
        return
    
    #! Implement authorization
   
    try:
        while True:
            #! Wait for messages from the WebSocket client
            try:
                data   = await websocket.receive_json()
                prefix = data.get("prefix")
                print(f"Search term -  `{prefix}` is recieved from {userId}")
                
                #! Rate limit here and check ES
                
                #! Get search results now
                
                
                response = await getSearchResults(prefix=prefix, userId = userId)
                await websocket.send_json(data = response)
            
            except WebSocketDisconnect:
                print(f"Client disconnected during data reception")
                break
            except Exception as e:
                print(f"Error processing request: {e}")
                if websocket.client_state == WebSocketState.CONNECTED:
                    await websocket.send_json({"error": "Some error occurred. Please try again."})
                
            
    except WebSocketDisconnect:
        print(f"Client disconnected")
        
    finally:
        if websocket.client_state == WebSocketState.CONNECTED:
            await websocket.close()
            print(f"Connection closed for userId: {userId}")



from fastapi import WebSocket, WebSocketDisconnect
from src.schemas.search_schema import SearchRequest


async def typeAheadSearchHandler(websocket: WebSocket):
    
    """WebSocket endpoint for the game, handling real-time communication."""
    await websocket.accept()
    
    #! Autheticate user for gameId
    #! Implement authorization

   
    try:
        while True:
            #! Wait for messages from the WebSocket client
            try:
                data    = await websocket.receive_json()
                request = SearchRequest(**data)
                print(f"Data {data} is recieved from player")
            except Exception as e:
                await websocket.send_json(data={"error":"Request payload doesnt matches with request schema "})
            returnMessage = {
                                "data": "test"
                            }
            await websocket.send_json(data = data)
            
    except WebSocketDisconnect:
        print(f"Client disconnected")



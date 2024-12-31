
from fastapi import WebSocket, WebSocketDisconnect

from jose import jwt, ExpiredSignatureError, JWTError
from starlette.middleware.base import BaseHTTPMiddleware
from pathlib import Path


ALGORITHM = "RS256"
PUBLIC_KEY_PATH = Path(__file__).resolve().parent.parent / "keys" / "public_key.pem"

try:
    with PUBLIC_KEY_PATH.open("r") as file:
        PUBLIC_KEY = file.read()
except FileNotFoundError:
    raise RuntimeError(f"Public key not found at {PUBLIC_KEY_PATH}")


async def WebSocketAuthMiddleware(websocket:WebSocket):
    try:
        token = websocket.headers.get("Authorization")
        if token is None:
            raise WebSocketDisconnect("Authorization token not provided")
        token = token.split(" ")[1] if " " in token else token  # Remove "Bearer" if included in token
        authentication = jwt.decode(
                            token,
                            PUBLIC_KEY,
                            algorithms = [ALGORITHM],
                            options    = {"verify_aud": False, "verify_iss": False}
                        )
        print("Successfully authenticated !!!")
        return authentication.get("sub")
    
    except ExpiredSignatureError:
        raise WebSocketDisconnect("Token has expired")

    except JWTError as e:
        raise WebSocketDisconnect("Invalid auth token")

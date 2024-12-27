# src/middleware/auth_middleware.py
from fastapi import Request, HTTPException
from jose import JWTError, jwt
from starlette.middleware.base import BaseHTTPMiddleware

from pathlib import Path

ALGORITHM = "RS256"

# Load the public key directly within the middleware
PUBLIC_KEY_PATH = Path(__file__).resolve().parent.parent / "keys" / "public_key.pem"

try:
    with PUBLIC_KEY_PATH.open("r") as file:
        PUBLIC_KEY = file.read()
except FileNotFoundError:
    raise RuntimeError(f"Public key not found at {PUBLIC_KEY_PATH}")


class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Skip authentication for docs and redoc
        if request.url.path in ["/docs", "/redoc", "/openapi.json"]:
            return await call_next(request)
        
        token = request.headers.get("Authorization")
        if token is None:
            raise HTTPException(status_code=401, detail="Not authenticated")

        # Extract token from "Bearer <token>"
        token = token.split(" ")[1] if " " in token else token

        try:
            # Decode the token using the RSA public key
            payload = jwt.decode(token, PUBLIC_KEY, algorithms=[ALGORITHM])
            request.state.user = payload  # Store user info in the request state
        except JWTError as e:
            raise HTTPException(status_code=403, detail=f"Could not validate credentials: {str(e)}")

        response = await call_next(request)
        return response

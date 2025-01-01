# src/middleware/auth_middleware.py
from fastapi import Request, HTTPException
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


class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.url.path.startswith("/static") or request.url.path in ["/docs", "/redoc", "/openapi.json", "/"]:
            return await call_next(request)

        token = request.headers.get("Authorization")
        if token is None:
            raise HTTPException(status_code=401, detail="Authorization token not provided")

        token = token.split(" ")[1] if " " in token else token
        try:
            payload = jwt.decode(
                                    token,
                                    PUBLIC_KEY,
                                    algorithms = [ALGORITHM],
                                    options    = {"verify_aud": False, "verify_iss": False}
                                )
            request.state.userId = payload.get("sub")

        except ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token has expired")
        except JWTError as e:
            raise HTTPException(status_code=403, detail=f"Invalid token: {str(e)}")

        response = await call_next(request)
        return response

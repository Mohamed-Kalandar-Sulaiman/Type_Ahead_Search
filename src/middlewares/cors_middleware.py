# src/middleware/cors_middleware.py
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import FastAPI


class CorsMiddleware(BaseHTTPMiddleware):
    def __init__(self,
                 app: FastAPI,
                 allow_origins: list = ["*"],
                 allow_credentials: bool = True,
                 allow_methods: list = ["*"],
                 allow_headers: list = ["*"]):
        super().__init__(app)
        self.allow_origins     = allow_origins
        self.allow_credentials = allow_credentials
        self.allow_methods     = allow_methods
        self.allow_headers     = allow_headers

    async def dispatch(self, request, call_next):
        response = await call_next(request)

        # Set CORS headers
        response.headers["Access-Control-Allow-Origin"]      = ', '.join(self.allow_origins)
        response.headers["Access-Control-Allow-Credentials"] = str(self.allow_credentials).lower()
        response.headers["Access-Control-Allow-Methods"]     = ', '.join(self.allow_methods)
        response.headers["Access-Control-Allow-Headers"]     = ', '.join(self.allow_headers)

        return response

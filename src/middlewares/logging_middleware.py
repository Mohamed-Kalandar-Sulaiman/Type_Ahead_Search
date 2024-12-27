# src/middleware/logging_middleware.py
from fastapi import Request
import logging
from starlette.middleware.base import BaseHTTPMiddleware
import time, uuid

# Configure logging
logging.basicConfig(level=logging.INFO)

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Log request details
        logging.info(f"Request: {request.method} {request.url}")
        start_time = time.perf_counter()

        # Process the request
        response = await call_next(request)
        # Log response details

        process_time = time.perf_counter() - start_time
        response.headers["X-Process-Time"] = str(process_time)
        response.headers['X-Request-Id'] = str(uuid.uuid4())
        logging.info(f"Response: {response.status_code}")
        return response

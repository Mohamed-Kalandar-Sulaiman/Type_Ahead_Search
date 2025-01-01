import os
import aioredis
from fastapi import HTTPException
from typing import Any


class RedisClient:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
            cls._instance.initialize()
        return cls._instance

    def initialize(self):
        """Initialize Redis client with environment variables."""
        self.REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
        self.REDIS_PORT = os.getenv("REDIS_PORT", "6379")
        self.REDIS_DB = os.getenv("REDIS_DB", 0)
        self.client = None

    async def connect(self):
        """Establish a connection to Redis."""
        if self.client is None:
            try:
                # Using from_url method instead of deprecated create_redis_pool
                redis_url = f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"
                self.client = await aioredis.from_url(redis_url)
                print("Initialized Redis client.")
            except Exception as e:
                print(f"Error initializing Redis client: {e}")
                raise HTTPException(status_code=500, detail=f"Error initializing Redis client: {str(e)}")

    async def close(self):
        """Close the Redis connection."""
        if self.client:
            try:
                await self.client.close()  # Close the connection properly
            except Exception as e:
                print(f"Error occurred while closing connection: {e}")

    async def check_connection(self):
        """Ping the Redis server to ensure the connection is alive."""
        if not self.client:
            await self.connect()  # Ensure connection
        try:
            pong = await self.client.ping()
            if not pong:
                raise Exception("Redis ping failed.")
            print("Redis ping successful.")
        except Exception as e:
            print(f"Error pinging Redis: {e}")
            raise HTTPException(status_code=500, detail=f"Error pinging Redis: {str(e)}")

    async def set_value(self, key: str, value: Any, ttl: int = None) -> bool:
        """Set a key-value pair in Redis."""
        if not self.client:
            await self.connect()  # Ensure connection
        try:
            if ttl:
                await self.client.setex(key, ttl, value)
            else:
                await self.client.set(key, value)
            return True
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error setting value in Redis: {str(e)}")

    async def get_value(self, key: str) -> Any:
        """Get a value by key from Redis."""
        if not self.client:
            await self.connect()  # Ensure connection
        try:
            value = await self.client.get(key)
            return value

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error getting value from Redis: {str(e)}")

    async def delete_key(self, key: str) -> bool:
        """Delete a key from Redis."""
        if not self.client:
            await self.connect()  # Ensure connection
        try:
            return await self.client.delete(key) > 0
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error deleting key from Redis: {str(e)}")

    async def set_hash(self, key: str, field: str, value: Any) -> bool:
        """Set a field-value pair in a Redis hash."""
        if not self.client:
            await self.connect()  # Ensure connection
        try:
            await self.client.hset(key, field, value)
            return True
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error setting hash in Redis: {str(e)}")

    async def get_hash(self, key: str, field: str) -> Any:
        """Get a value from a Redis hash."""
        if not self.client:
            await self.connect()  # Ensure connection
        try:
            value = await self.client.hget(key, field)
            if value is None:
                raise HTTPException(status_code=404, detail="Field not found in hash")
            return value
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error getting hash from Redis: {str(e)}")

    async def get_keys(self, pattern: str) -> list:
        """Get keys matching a pattern."""
        if not self.client:
            await self.connect()  # Ensure connection
        try:
            keys = await self.client.keys(pattern)
            return keys
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error getting keys from Redis: {str(e)}")


async def get_redis_client() -> RedisClient:
    """Get the singleton Redis client."""
    return RedisClient()

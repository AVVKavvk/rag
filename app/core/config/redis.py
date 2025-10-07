import asyncio
import json
import os
from typing import Any, Dict, Optional

import redis.asyncio as redis
from redis.exceptions import RedisError
from dotenv import load_dotenv

from app.utils.logger import logger

load_dotenv()

REDIS_URL = os.getenv("REDIS_URL")
if not REDIS_URL:
    raise Exception("REDIS_URL is not set")


class RedisManager:
    def __init__(self, redis_url: str):
        self.redis_url = redis_url
        self.redis_client: Optional[redis.Redis] = None

    async def connect(self):
        """Initialize Redis connection (async client)"""
        if not self.redis_client:
            self.redis_client = redis.from_url(self.redis_url, decode_responses=True)
            if not isinstance(self.redis_client, redis.Redis):
                raise RuntimeError("Invalid Redis client type (must be async Redis).")
            logger.info("Connected to Redis for general use")

    async def disconnect(self):
        """Close Redis connection"""
        if self.redis_client:
            await self.redis_client.close()
            logger.info("Disconnected from Redis")

    async def add_to_list(self, prefix: str, key: str, value: Dict[str, Any], ttl: int = None):
        """Add a value to a Redis list and optionally set TTL"""
        if not self.redis_client:
            raise RuntimeError("Redis client is not connected. Call connect() first.")

        new_key = f"{prefix}:{key}"
        try:
            await self.redis_client.lpush(new_key, json.dumps(value))
            if ttl:
                # expire() is awaitable with async redis
                await self.redis_client.expire(new_key, ttl)
        except RedisError as e:
            logger.error(f"Failed to push to list {new_key}: {e}")
            raise

    async def get_from_list(self, prefix: str, key: str):
        """Get a value from a Redis list"""
        if not self.redis_client:
            raise RuntimeError("Redis client is not connected. Call connect() first.")

        new_key = f"{prefix}:{key}"
        try:
            value = await self.redis_client.lrange(new_key, 0, -1)
            return value
        except RedisError as e:
            logger.error(f"Failed to get from list {new_key}: {e}")
            raise

    async def clear_list(self, prefix: str, key: str, user_id: str):
        """Remove all entries with the given user_id from a Redis list"""
        if not self.redis_client:
            raise RuntimeError("Redis client is not connected. Call connect() first.")

        new_key = f"{prefix}:{key}"
        try:
            values = await self.redis_client.lrange(new_key, 0, -1)
            for v in values:
                try:
                    parsed = json.loads(v)
                except json.JSONDecodeError:
                    continue
                if parsed.get("user_id") == user_id:
                    # Remove all matching occurrences
                    await self.redis_client.lrem(new_key, 0, v)
        except RedisError as e:
            logger.error(f"Failed to remove user {user_id} from list {new_key}: {e}")
            raise


# Singleton instance for app use
redis_manager = RedisManager(REDIS_URL)

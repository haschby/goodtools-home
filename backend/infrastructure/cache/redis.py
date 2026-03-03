from application.ports.cache import CacheInterface
from redis.asyncio import redis
from typing import Any

class RedisCache(CacheInterface):
    
    def __init__(self, client: redis.Redis):
        self.client = client

    def get(self, key: str) -> Any:
        return self.client.get(key)

    def set(self, key: str, value: Any, ttl: int) -> None:
        self.client.set(key, value, ex=ttl)

    def delete(self, key: str) -> None:
        self.client.delete(key)
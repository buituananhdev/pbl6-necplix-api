import redis
from fastapi import FastAPI, Depends
from functools import lru_cache

class RedisService:
    def __init__(self, host: str = "redis", port: int = 6379, db: int = 0):
        self.client = redis.Redis(host=host, port=port, db=db)

    def set(self, key: str, value: str, ttl: int = 3600):
        self.client.set(key, value, ex=ttl) 

    def get(self, key: str):
        return self.client.get(name=key)

    def delete(self, key: str):
        self.client.delete(name=key)

    def exists(self, key: str) -> bool:
        return self.client.exists(key) > 0

@lru_cache()
def get_redis_service() -> RedisService:
    return RedisService()

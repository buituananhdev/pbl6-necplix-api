import redis
from functools import lru_cache
import logging

# Config logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RedisService:
    def __init__(self, host: str = "redis", port: int = 6379, db: int = 0):
        try:
            self.client = redis.Redis(host=host, port=port, db=db)
            self.client.ping()
            logger.info("Connected to Redis server successfully.")
        except redis.ConnectionError:
            self.client = None
            logger.warning("Could not connect to Redis server. Running without cache.")

    def set(self, key: str, value: str, ttl: int = 3600):
        if self.client:
            try:
                self.client.set(key, value, ex=ttl)
            except redis.ConnectionError:
                logger.error("Failed to set key in Redis.")

    def get(self, key: str):
        if self.client:
            try:
                return self.client.get(name=key)
            except redis.ConnectionError:
                logger.error("Failed to get key from Redis.")
        return None

    def delete(self, key: str):
        if self.client:
            try:
                self.client.delete(name=key)
            except redis.ConnectionError:
                logger.error("Failed to delete key from Redis.")

    def exists(self, key: str) -> bool:
        if self.client:
            try:
                return self.client.exists(key) > 0
            except redis.ConnectionError:
                logger.error("Failed to check if key exists in Redis.")
        return False

@lru_cache()
def get_redis_service() -> RedisService:
    return RedisService()

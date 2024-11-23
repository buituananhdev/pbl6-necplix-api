from typing import Optional

from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic_settings import BaseSettings
import models
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Settings(BaseSettings):
    # database configurations
    DATABASE_URL: Optional[str] = None

    # JWT
    secret_key: str = "secret"
    algorithm: str = "HS256"

    # TMDB API key
    TMDB_API_KEY: str
    class Config:
        env_file = ".env.dev"
        from_attributes = True


async def initiate_database():
    try:
        logger.info("Initializing database...")
        client = AsyncIOMotorClient(Settings().DATABASE_URL)
        await init_beanie(
            database=client.get_default_database(), document_models=models.__all__
        )
        logger.info("Database initialized successfully!")
    except Exception as e:
        logger.error(f"Error initializing database: {e}")
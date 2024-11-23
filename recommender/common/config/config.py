from typing import Optional

from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic_settings import BaseSettings
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Settings(BaseSettings):
    # database configurations
    DATABASE_URL: Optional[str] = None

    class Config:
        env_file = ".env.dev"
        from_attributes = True
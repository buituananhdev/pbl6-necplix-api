from pydantic import BaseModel, EmailStr
from typing import Optional, Any
from beanie import PydanticObjectId
from datetime import datetime

class UpdateRatingModel(BaseModel):
    user_id: PydanticObjectId
    movie_id: int
    rating: int
    timestamp: datetime = datetime.now()

    class Collection:
        name = "rating"

    class Config:
        json_schema_extra = {
            "example": {
                "user_id": "60d5ec49f1e7e3a4b8e788a2",
                "movie_id": 123,
                "rating": 4,
                "timestamp": "2024-11-12T12:00:00Z"
            }
        }

class Response(BaseModel):
    user_id: PydanticObjectId
    movie_id: int
    rating: int
    timestamp: datetime = datetime.now()

    class Config:
        json_schema_extra = {
            "example": {
                "user_id": "60d5ec49f1e7e3a4b8e788a2",
                "movie_id": 123,
                "rating": 4,
                "timestamp": "2024-11-12T12:00:00Z"
            }
        }

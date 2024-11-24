from typing import Optional, Any
from models.user import User
from beanie import Document, Link
from pydantic import BaseModel, EmailStr
from datetime import datetime

class Rating(Document):
    user_id: Optional[Link[User]] = None
    movie_id: int
    rating: float
    comment: Optional[str] = None
    timestamp: Optional[datetime] = datetime.now()

    class Config:
        json_schema_extra = {
            "example": {
                "user_id": "60d5ec49f1e7e3a4b8e788a2",
                "movie_id": 123,
                "comment": "This is a great movie",
                "rating": 4,
                "timestamp": "2024-11-12T12:00:00Z"
            }
        }

    class Settings:
        name = "rating"

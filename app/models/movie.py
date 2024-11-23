from typing import List, Optional
from beanie import Document

class Movie(Document):
    movie_id: Optional[int] = None
    title: Optional[str] = None

    class Config:
        arbitrary_types_allowed = True
        json_schema_extra = {
            "example": {
                "movie_id": 912649,
                "title": "Venom: The Last Dance"
            }
        }

    class Settings:
        name = "movie"


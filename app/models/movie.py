from typing import List, Optional
from beanie import Document

class Movie(Document):
    movie_id: Optional[int] = None
    title: Optional[str] = None
    genres: Optional[str] = None
    viewcount: Optional[int] = 0

    class Config:
        arbitrary_types_allowed = True
        json_schema_extra = {
            "example": {
                "movie_id": 912649,
                "title": "Venom: The Last Dance",
                "genres": "Adventure|Animation|Children|Comedy|Fantasy",
                "viewcount": 0
            }
        }

    class Settings:
        name = "collaborative_based_movies"
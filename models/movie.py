from typing import List, Optional
from beanie import Document

class Movie(Document):
    movie_id: Optional[int] = None  # Lưu ID riêng của phim, nếu có
    title: Optional[str] = None
    genre_ids: Optional[List[int]] = []

    class Config:
        arbitrary_types_allowed = True
        json_schema_extra = {
            "example": {
                "movie_id": 912649,
                "title": "Venom: The Last Dance",
                "genre_ids": [28, 878, 12],
            }
        }

    class Settings:
        name = "movie"


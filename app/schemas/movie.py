from pydantic import BaseModel
from typing import List, Optional, Any

class MovieData(BaseModel):
    movie_id: Optional[int] = None
    title: Optional[str] = None
    view_count: Optional[int] = 0

    def __init__(self, **data):
        super().__init__(**data)
        if self.genre_ids is None:
            self.genre_ids = []

    class Config:
        json_schema_extra = {
            "example": {
                "movie_id": 912649,
                "title": "Venom: The Last Dance",
                "view_count": 0
            }
        }


class Genre(BaseModel):
    id: int
    name: str

class MovieDetail(BaseModel):
    movie_id: int
    genres: List[int]
    title: str

    class Config:
        json_schema_extra = {
            "example": {
                "movie_id": 912649,
                "title": "Venom: The Last Dance",
                "view_count": 0
            }
        }

class Response(BaseModel):
    status_code: int
    response_type: str
    description: str
    data: Optional[Any]

    class Config:
        json_schema_extra = {
            "example": {
                "status_code": 200,
                "response_type": "success",
                "description": "Operation successful",
                "data": "Sample data",
            }
        }

class UpdateMovieModel(BaseModel):
    movie_id: Optional[int] = None
    title: Optional[str] = None
    genre_ids: Optional[list[int]] = []

    class Collection:
        name = "movie"

    class Config:
        json_schema_extra = {
            "example": {
                "movie_id": 912649,
                "title": "Venom: The Last Dance"
            }
        }
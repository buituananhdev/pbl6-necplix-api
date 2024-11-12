from pydantic import BaseModel
from typing import List, Optional, Any

class MovieData(BaseModel):
    movie_id: Optional[int] = None  # ID do người dùng tự định nghĩa
    title: Optional[str] = None
    genre_ids: Optional[list[int]] = []

    def __init__(self, **data):
        super().__init__(**data)
        if self.genre_ids is None:
            self.genre_ids = []

    class Config:
        json_schema_extra = {
            "example": {
                "movie_id": 912649,
                "title": "Venom: The Last Dance",
                "genre_ids": [28, 878, 12],
            }
        }


class Genre(BaseModel):
    id: int
    name: str

class ProductionCompany(BaseModel):
    id: int
    logo_path: Optional[str] = None
    name: str
    origin_country: str


class ProductionCountry(BaseModel):
    iso_3166_1: str
    name: str


class SpokenLanguage(BaseModel):
    english_name: str
    iso_639_1: str
    name: str


class Video(BaseModel):
    iso_639_1: str
    iso_3166_1: str
    name: str
    key: str
    site: str
    size: int
    type: str
    official: bool
    published_at: str
    id: str


class VideoResults(BaseModel):
    results: List[Video]


class BelongsToCollection(BaseModel):
    id: int
    name: str
    poster_path: Optional[str] = None
    backdrop_path: Optional[str] = None


class MovieDetail(BaseModel):
    movie_id: int
    genres: List[Genre]
    title: str

    class Config:
        json_schema_extra = {
            "example": {
                "genres": [
                    {
                        "id": 28,
                        "name": "Action"
                    },
                    {
                        "id": 878,
                        "name": "Science Fiction"
                    },
                    {
                        "id": 12,
                        "name": "Adventure"
                    }
                ],
                "movie_id": 912649,
                "title": "Venom: The Last Dance",
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
                "title": "Venom: The Last Dance",
                "genre_ids": [28, 878, 12],
            }
        }
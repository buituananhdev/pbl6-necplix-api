from pydantic import BaseModel
from typing import List, Optional, Any


class MovieData(BaseModel):
    id: Optional[int] = None
    title: Optional[str] = None
    original_title: Optional[str] = None
    overview: Optional[str] = None
    poster_path: Optional[str] = None
    backdrop_path: Optional[str] = None
    adult: Optional[bool] = True
    original_language: Optional[str] = None
    genre_ids: Optional[list[int]] = []
    popularity: Optional[float] = None
    release_date: Optional[str] = None
    vote_average: Optional[float] = None
    vote_count: Optional[int] = None

    def __init__(self, **data):
        super().__init__(**data)
        if self.genre_ids is None:
            self.genre_ids = []

    class Config:
        json_schema_extra = {
            "example": {
                "id": 912649,
                "title": "Venom: The Last Dance",
                "original_title": "Venom: The Last Dance",
                "overview": "Eddie and Venom are on the run. Hunted by both of their worlds and with the net closing in, the duo are forced into a devastating decision that will bring the curtains down on Venom and Eddie's last dance.",
                "poster_path": "/k42Owka8v91trK1qMYwCQCNwJKr.jpg",
                "backdrop_path": "/3V4kLQg0kSqPLctI5ziYWabAZYF.jpg",
                "adult": False,
                "original_language": "en",
                "genre_ids": [28, 878, 12],
                "popularity": 5868.656,
                "release_date": "2024-10-22",
                "vote_average": 6.3,
                "vote_count": 163
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
    adult: bool
    backdrop_path: Optional[str] = None
    belongs_to_collection: Optional[BelongsToCollection] = None
    budget: Optional[int] = None
    genres: List[Genre]
    homepage: Optional[str] = None
    id: int
    imdb_id: Optional[str] = None
    origin_country: List[str]
    original_language: str
    original_title: str
    overview: str
    popularity: float
    poster_path: Optional[str] = None
    production_companies: List[ProductionCompany]
    production_countries: List[ProductionCountry]
    release_date: str
    revenue: Optional[int] = None
    runtime: Optional[int] = None
    spoken_languages: List[SpokenLanguage]
    status: str
    tagline: Optional[str] = None
    title: str
    video: bool
    vote_average: float
    vote_count: int
    videos: VideoResults

    class Config:
        json_schema_extra = {
            "example": {
                "adult": False,
                "backdrop_path": "/3V4kLQg0kSqPLctI5ziYWabAZYF.jpg",
                "belongs_to_collection": {
                    "id": 558216,
                    "name": "Venom Collection",
                    "poster_path": "/hoTLlTIohrzQ13HQVkZrDlvffuT.jpg",
                    "backdrop_path": "/vq340s8DxA5Q209FT8PHA6CXYOx.jpg"
                },
                "budget": 120000000,
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
                "homepage": "https://venom.movie",
                "id": 912649,
                "imdb_id": "tt16366836",
                "origin_country": [
                    "US"
                ],
                "original_language": "en",
                "original_title": "Venom: The Last Dance",
                "overview": "Eddie and Venom are on the run. Hunted by both of their worlds and with the net closing in, the duo are forced into a devastating decision that will bring the curtains down on Venom and Eddie's last dance.",
                "popularity": 5868.656,
                "poster_path": "/k42Owka8v91trK1qMYwCQCNwJKr.jpg",
                "production_companies": [
                    {
                        "id": 5,
                        "logo_path": "/71BqEFAF4V3qjjMPCpLuyJFB9A.png",
                        "name": "Columbia Pictures",
                        "origin_country": "US"
                    },
                    {
                        "id": 84041,
                        "logo_path": "/nw4kyc29QRpNtFbdsBHkRSFavvt.png",
                        "name": "Pascal Pictures",
                        "origin_country": "US"
                    },
                    {
                        "id": 53462,
                        "logo_path": "/nx8B3Phlcse02w86RW4CJqzCnfL.png",
                        "name": "Matt Tolmach Productions",
                        "origin_country": "US"
                    },
                    {
                        "id": 91797,
                        "logo_path": None,
                        "name": "Hutch Parker Entertainment",
                        "origin_country": "US"
                    },
                    {
                        "id": 14439,
                        "logo_path": None,
                        "name": "Arad Productions",
                        "origin_country": "US"
                    }
                ],
                "production_countries": [
                    {
                        "iso_3166_1": "US",
                        "name": "United States of America"
                    }
                ],
                "release_date": "2024-10-22",
                "revenue": 8500000,
                "runtime": 109,
                "spoken_languages": [
                    {
                        "english_name": "English",
                        "iso_639_1": "en",
                        "name": "English"
                    }
                ],
                "status": "Released",
                "tagline": "'Til death do they part.",
                "title": "Venom: The Last Dance",
                "video": False,
                "vote_average": 6.35,
                "vote_count": 167,
                "videos": {
                    "results": [
                        {
                            "iso_639_1": "en",
                            "iso_3166_1": "US",
                            "name": "A VIP cutie patootie 🖤 Blue stole our hearts",
                            "key": "oAazxCOLF8c",
                            "site": "YouTube",
                            "size": 1080,
                            "type": "Featurette",
                            "official": True,
                            "published_at": "2024-10-25T10:15:02.000Z",
                            "id": "671ba06c27bd57d91f629487"
                        },
                        {
                            "iso_639_1": "en",
                            "iso_3166_1": "US",
                            "name": "London, it was a blast",
                            "key": "z5aYy3qktGg",
                            "site": "YouTube",
                            "size": 1080,
                            "type": "Featurette",
                            "official": True,
                            "published_at": "2024-10-25T09:30:31.000Z",
                            "id": "671ba0471ea33928297d285a"
                        }
                    ]
                }
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
    id: Optional[int] = None
    title: Optional[str] = None
    original_title: Optional[str] = None
    overview: Optional[str] = None
    poster_path: Optional[str] = None
    backdrop_path: Optional[str] = None
    adult: Optional[bool] = True
    original_language: Optional[str] = None
    genre_ids: Optional[list[int]] = []
    popularity: Optional[float] = None
    release_date: Optional[str] = None
    vote_average: Optional[float] = None
    vote_count: Optional[int] = None

    class Collection:
        name = "movie"

    class Config:
        json_schema_extra = {
            "example": {
                "id": 912649,
                "title": "Venom: The Last Dance",
                "original_title": "Venom: The Last Dance",
                "overview": "Eddie and Venom are on the run. Hunted by both of their worlds and with the net closing in, the duo are forced into a devastating decision that will bring the curtains down on Venom and Eddie's last dance.",
                "poster_path": "/k42Owka8v91trK1qMYwCQCNwJKr.jpg",
                "backdrop_path": "/3V4kLQg0kSqPLctI5ziYWabAZYF.jpg",
                "adult": False,
                "original_language": "en",
                "genre_ids": [28, 878, 12],
                "popularity": 5868.656,
                "release_date": "2024-10-22",
                "vote_average": 6.3,
                "vote_count": 163
            }
        }
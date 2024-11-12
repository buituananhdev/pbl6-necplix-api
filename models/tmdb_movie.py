from beanie import Document
from typing import List, Optional


class TMDBMovie(Document):
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
    class Settings:
        name = "tmdb_movie"
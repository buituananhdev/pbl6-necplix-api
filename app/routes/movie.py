from fastapi import APIRouter, Query
from schemas.movie import Response
from models.movie import Movie
from database.movie import *

router = APIRouter()

@router.get("/", response_description="Movies retrieved", response_model=Response)
async def get_movies():
    movies = await retrieve_movies()
    return {
        "status_code": 200,
        "response_type": "success",
        "description": "Movies data retrieved successfully",
        "data": movies,
    }

@router.get("", response_description="Movie data retrieved", response_model=Response)
async def get_movie_by_movie_id(movie_id: int = Query(...)):
    movie = await retrieve_movie_by_movie_id(movie_id)
    if movie:
        return {
            "status_code": 200,
            "response_type": "success",
            "description": "Movie data retrieved successfully",
            "data": movie,
        }
    return {
        "status_code": 404,
        "response_type": "error",
        "description": "Movie doesn't exist",
        "data": None,
    }

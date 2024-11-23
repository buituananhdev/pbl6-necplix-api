from typing import List
from fastapi import Body, Depends, APIRouter, HTTPException, status
from schemas.movie import MovieDetail, MovieData, Response, UpdateMovieModel
from models.movie import Movie
from database.movie import retrieve_movies, add_movie, update_movie_data, delete_movie, retrieve_movie
from beanie import PydanticObjectId


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

@router.get("/{id}", response_description="Movie data retrieved", response_model=Response)
async def get_movie_data(id: PydanticObjectId):
    movie = await retrieve_movie(id)
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
    }

@router.post(
    "/",
    response_description="Movie data added into the database",
    response_model=Response,
)
async def add_movie_data(movie: Movie = Body(...)):
    new_movie = await add_movie(movie)
    return {
        "status_code": 200,
        "response_type": "success",
        "description": "Movie created successfully",
        "data": new_movie,
    }

@router.delete("/{id}", response_description="Movie data deleted from the database")
async def delete_movie_data(id: PydanticObjectId):
    deleted_movie = await delete_movie(id)
    if deleted_movie:
        return {
            "status_code": 200,
            "response_type": "success",
            "description": "Movie with ID: {} removed".format(id),
            "data": deleted_movie,
        }
    return {
        "status_code": 404,
        "response_type": "error",
        "description": "Movie with id {0} doesn't exist".format(id),
        "data": False,
    }

@router.put("/{id}", response_model=Response)
async def update_movie(id: PydanticObjectId, req: UpdateMovieModel = Body(...)):
    updated_movie = await update_movie_data(id, req.dict())
    if updated_movie:
        return {
            "status_code": 200,
            "response_type": "success",
            "description": "Movie with ID: {} updated".format(id),
            "data": updated_movie,
        }
    return {
        "status_code": 404,
        "response_type": "error",
        "description": "An error occurred. Movie with ID: {} not found".format(id),
        "data": False,
    }
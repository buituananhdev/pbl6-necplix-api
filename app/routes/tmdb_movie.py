from typing import List
from fastapi import APIRouter, HTTPException, Query, Depends
from tmdb.tmdb import *
from auth.jwt_bearer import get_current_user
from schemas.user import TokenUserPayload
router = APIRouter()

@router.get("/polular", response_description="Movies retrieved")
async def get_movies_popular(page: int = Query(1), user: TokenUserPayload = Depends(get_current_user)):
    movies = await fetch_movies_popular(page)
    return {
        "status_code": 200,
        "response_type": "success",
        "description": "Movies data retrieved successfully",
        "data": movies,
    }


@router.get("/trending", response_description="Movies retrieved")
async def get_movies_trending(page: int = Query(1), user: TokenUserPayload = Depends(get_current_user)):
    movies = await fetch_movies_trending(page)
    return {
        "status_code": 200,
        "response_type": "success",
        "description": "Movies data retrieved successfully",
        "data": movies,
    }


@router.get("/tv/popular", response_description="Movies retrieved")
async def get_tv_popular(page: int = Query(1), user: TokenUserPayload = Depends(get_current_user)):
    movies = await fetch_tv_popular(page)
    return {
        "status_code": 200,
        "response_type": "success",
        "description": "Movies data retrieved successfully",
        "data": movies,
    }


@router.get("/tv/trending", response_description="Movies retrieved")
async def get_tv_trending(page: int = Query(1), user: TokenUserPayload = Depends(get_current_user)):
    movies = await fetch_tv_trending(page)
    return {
        "status_code": 200,
        "response_type": "success",
        "description": "Movies data retrieved successfully",
        "data": movies,
    }

@router.get("/", response_description="Movies retrieved")
async def get_movie_detail(movie_id: int = Query(...), user: TokenUserPayload = Depends(get_current_user)):
    movie = await fetch_movie_detail(movie_id, user.user_id)

    if movie is None or movie == {}:
        raise HTTPException(status_code=404, detail="Movie not found")

    return {
        "status_code": 200,
        "response_type": "success",
        "description": "Movies data retrieved successfully",
        "data": movie,
    }

@router.get("/recommendations", response_description="Movies recommendations retrieved")
async def get_movie_recommendations(movie_id: int = Query(...), page: int = Query(1)):
    images = await fetch_movie_recommendations(movie_id, page)

    if images is None or images == {}:
        raise HTTPException(status_code=404, detail="Movie not found")

    return {
        "status_code": 200,
        "response_type": "success",
        "description": "Movie images data retrieved successfully",
        "data": images,
    }

@router.get("/search", response_description="Movies search retrieved")
async def get_movie_search(
    key_word: str = Query(..., description="Keyword for movie search"),
    page: int = Query(1, ge=1, description="Page number for pagination"),
    user: TokenUserPayload = Depends(get_current_user)
):
    images = await fetch_movies_by_keyword(key_word, page)

    if not images:
        raise HTTPException(status_code=404, detail="Movies not found")

    return {
        "status_code": 200,
        "response_type": "success",
        "description": "Movies data retrieved successfully",
        "data": images,
    }

@router.get("/recently-viewed", response_description="Movies retrieved")
async def get_recently_viewed(user: TokenUserPayload = Depends(get_current_user)):
    movies = await fetch_recently_viewed(user.user_id)
    return {
        "status_code": 200,
        "response_type": "success",
        "description": "Movies data retrieved successfully",
        "data": movies,
    }

@router.get("/discover", response_description="Movies retrieved")
async def get_discover_movies(page: int = Query(1), genre: str = Query(...), user: TokenUserPayload = Depends(get_current_user)):
    movies = await fetch_movies_by_genre(page, genre, user.age > 18)
    return {
        "status_code": 200,
        "response_type": "success",
        "description": "Movies data retrieved successfully",
        "data": movies,
    }

@router.get("/genres", response_description="Movies retrieved")
async def get_genres():
    genres = await fetch_genres()
    return {
        "status_code": 200,
        "response_type": "success",
        "description": "Movies data retrieved successfully",
        "data": genres,
    }

@router.post("/view", response_description="View movies")
async def view_movies(movie_id: int = Query(...), user: TokenUserPayload = Depends(get_current_user)):
    await increment_viewcount(movie_id)
    await add_to_recently_viewed(user.user_id, movie_id)
    return {
        "status_code": 200,
        "response_type": "success",
        "description": "View successfully",
    }
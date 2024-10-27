from typing import List
from fastapi import APIRouter, Body, Query
from schemas.movie import MovieData
from tmdb.tmdb import fetch_movies_popular, fetch_movies_trending, fetch_tv_popular, fetch_tv_trending

router = APIRouter()

@router.get("/polular", response_description="Movies retrieved")
async def get_movies_popular(page: int = Query()):
    movies = await fetch_movies_popular(page)
    return {
        "status_code": 200,
        "response_type": "success",
        "description": "Movies data retrieved successfully",
        "data": movies,
    }


@router.get("/trending", response_description="Movies retrieved")
async def get_movies_trending(page: int = Query()):
    movies = await fetch_movies_trending(page)
    return {
        "status_code": 200,
        "response_type": "success",
        "description": "Movies data retrieved successfully",
        "data": movies,
    }


@router.get("/tv/popular", response_description="Movies retrieved")
async def get_tv_popular(page: int = Query()):
    movies = await fetch_tv_popular(page)
    return {
        "status_code": 200,
        "response_type": "success",
        "description": "Movies data retrieved successfully",
        "data": movies,
    }


@router.get("/tv/trending", response_description="Movies retrieved")
async def get_tv_trending(page: int = Query()):
    movies = await fetch_tv_trending(page)
    return {
        "status_code": 200,
        "response_type": "success",
        "description": "Movies data retrieved successfully",
        "data": movies,
    }


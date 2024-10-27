from typing import List
from schemas.movie import MovieData
from config.config import Settings
import httpx

headers = {"accept": "application/json"}
settings = Settings()
api_key = settings.TMDB_API_KEY

async def fetch_movies_popular(page: int) -> List[MovieData]:
    url = f"https://api.themoviedb.org/3/movie/popular?api_key={api_key}&language=en-US&page={page}"
    
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
    
    if response.status_code == 200:
        movies_data = response.json().get("results", [])
        return [MovieData(**movie) for movie in movies_data]
    else:
        print(f"Failed to fetch movies: {response.status_code}")
        return []


async def fetch_movies_trending(page: int) -> List[MovieData]:
    url = f"https://api.themoviedb.org/3/trending/movie/day?api_key={api_key}&language=en-US&page={page}"
    
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
    
    if response.status_code == 200:
        movies_data = response.json().get("results", [])
        return [MovieData(**movie) for movie in movies_data]
    else:
        print(f"Failed to fetch movies: {response.status_code}")
        return []

async def fetch_tv_popular(page: int) -> List[MovieData]:
    url = f"https://api.themoviedb.org/3/tv/popular?api_key={api_key}&language=en-US&page={page}"
    
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
    
    if response.status_code == 200:
        movies_data = response.json().get("results", [])
        return [MovieData(**movie) for movie in movies_data]
    else:
        print(f"Failed to fetch movies: {response.status_code}")
        return []

async def fetch_tv_trending(page: int) -> List[MovieData]:
    url = f"https://api.themoviedb.org/3/trending/tv/day?api_key={api_key}&language=en-US&page={page}"
    
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
    
    if response.status_code == 200:
        movies_data = response.json().get("results", [])
        return [MovieData(**movie) for movie in movies_data]
    else:
        print(f"Failed to fetch movies: {response.status_code}")
        return []

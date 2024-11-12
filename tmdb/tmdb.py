from typing import List
from schemas.tmdb_movie import MovieData, MovieDetail
from config.config import Settings
from services.redis import get_redis_service
import httpx
import json

headers = {"accept": "application/json"}
settings = Settings()
api_key = settings.TMDB_API_KEY
redis_service = get_redis_service()

async def fetch_movies_popular(page: int) -> List[MovieData]:
    cache_key = f"movies_popular_{page}"
    cached_data = redis_service.get(cache_key)
    
    if cached_data:
        return [MovieData(**movie) for movie in json.loads(cached_data)]
    
    url = f"https://api.themoviedb.org/3/movie/popular?api_key={api_key}&language=en-US&page={page}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
    
    if response.status_code == 200:
        movies_data = response.json().get("results", [])
        redis_service.set(cache_key, json.dumps(movies_data), ttl=3600)
        return [MovieData(**movie) for movie in movies_data]
    else:
        print(f"Failed to fetch movies: {response.status_code}")
        return []

async def fetch_movies_trending(page: int) -> List[MovieData]:
    cache_key = f"movies_trending_{page}"
    cached_data = redis_service.get(cache_key)
    
    if cached_data:
        return [MovieData(**movie) for movie in json.loads(cached_data)]
    
    url = f"https://api.themoviedb.org/3/trending/movie/day?api_key={api_key}&language=en-US&page={page}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
    
    if response.status_code == 200:
        movies_data = response.json().get("results", [])
        redis_service.set(cache_key, json.dumps(movies_data), ttl=3600)
        return [MovieData(**movie) for movie in movies_data]
    else:
        print(f"Failed to fetch movies: {response.status_code}")
        return []

async def fetch_tv_popular(page: int) -> List[MovieData]:
    cache_key = f"tv_popular_{page}"
    cached_data = redis_service.get(cache_key)
    
    if cached_data:
        return [MovieData(**movie) for movie in json.loads(cached_data)]
    
    url = f"https://api.themoviedb.org/3/tv/popular?api_key={api_key}&language=en-US&page={page}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
    
    if response.status_code == 200:
        movies_data = response.json().get("results", [])
        redis_service.set(cache_key, json.dumps(movies_data), ttl=3600)
        return [MovieData(**movie) for movie in movies_data]
    else:
        print(f"Failed to fetch movies: {response.status_code}")
        return []

async def fetch_tv_trending(page: int) -> List[MovieData]:
    cache_key = f"tv_trending_{page}"
    cached_data = redis_service.get(cache_key)
    
    if cached_data:
        return [MovieData(**movie) for movie in json.loads(cached_data)]
    
    url = f"https://api.themoviedb.org/3/trending/tv/day?api_key={api_key}&language=en-US&page={page}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
    
    if response.status_code == 200:
        movies_data = response.json().get("results", [])
        redis_service.set(cache_key, json.dumps(movies_data), ttl=3600)
        return [MovieData(**movie) for movie in movies_data]
    else:
        print(f"Failed to fetch movies: {response.status_code}")
        return []

async def fetch_movie_detail(movie_id: int) -> MovieDetail:
    cache_key = f"movie_detail_{movie_id}"
    cached_data = redis_service.get(cache_key)
    
    if cached_data:
        return MovieDetail(**json.loads(cached_data))
    
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US&append_to_response=videos"
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
    
    if response.status_code == 200:
        movie_data = response.json()
        redis_service.set(cache_key, json.dumps(movie_data), ttl=3600)
        return MovieDetail(**movie_data)
    else:
        print(f"Failed to fetch movie detail: {response.status_code}")
        return {}

from typing import List
from schemas.tmdb_movie import TMDBMovie, MovieDetail, Genre
from common.config.config import Settings
from services.redis import get_redis_service
from database.movie import add_movie, increment_viewcount, retrieve_movie_by_movie_id
from database.user import add_to_recently_viewed, retrieve_user
import httpx
import json
import logging
import asyncio
from beanie import PydanticObjectId

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

headers = {"accept": "application/json"}
settings = Settings()
api_key = settings.TMDB_API_KEY
redis_service = get_redis_service()

async def fetch_movies_popular(page: int) -> List[TMDBMovie]:
    cache_key = f"movies_popular_{page}"
    try:
        cached_data = redis_service.get(cache_key)
        if cached_data:
            return [TMDBMovie(**movie) for movie in json.loads(cached_data)]

        url = f"https://api.themoviedb.org/3/movie/popular?api_key={api_key}&language=en-US&page={page}"
        
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers)
        
        if response.status_code == 200:
            movies_data = response.json().get("results", [])
            redis_service.set(cache_key, json.dumps(movies_data), ttl=3600)
            return [TMDBMovie(**movie) for movie in movies_data]
        else:
            logger.error(f"Failed to fetch popular movies: {response.status_code}")
            return []
    except Exception as e:
        logger.exception(f"Error fetching popular movies for page {page}: {e}")
        return []


async def fetch_movies_trending(page: int) -> List[TMDBMovie]:
    cache_key = f"movies_trending_{page}"
    try:
        cached_data = redis_service.get(cache_key)
        if cached_data:
            return [TMDBMovie(**movie) for movie in json.loads(cached_data)]

        url = f"https://api.themoviedb.org/3/trending/movie/day?api_key={api_key}&language=en-US&page={page}"
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers)
        
        if response.status_code == 200:
            movies_data = response.json().get("results", [])
            redis_service.set(cache_key, json.dumps(movies_data), ttl=3600)
            return [TMDBMovie(**movie) for movie in movies_data]
        else:
            logger.error(f"Failed to fetch trending movies: {response.status_code}")
            return []
    except Exception as e:
        logger.exception(f"Error fetching trending movies for page {page}: {e}")
        return []


async def fetch_tv_popular(page: int) -> List[TMDBMovie]:
    cache_key = f"tv_popular_{page}"
    try:
        cached_data = redis_service.get(cache_key)
        if cached_data:
            return [TMDBMovie(**movie) for movie in json.loads(cached_data)]

        url = f"https://api.themoviedb.org/3/tv/popular?api_key={api_key}&language=en-US&page={page}"
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers)
        
        if response.status_code == 200:
            movies_data = response.json().get("results", [])
            redis_service.set(cache_key, json.dumps(movies_data), ttl=3600)
            return [TMDBMovie(**movie) for movie in movies_data]
        else:
            logger.error(f"Failed to fetch popular TV shows: {response.status_code}")
            return []
    except Exception as e:
        logger.exception(f"Error fetching popular TV shows for page {page}: {e}")
        return []


async def fetch_tv_trending(page: int) -> List[TMDBMovie]:
    cache_key = f"tv_trending_{page}"
    try:
        cached_data = redis_service.get(cache_key)
        if cached_data:
            return [TMDBMovie(**movie) for movie in json.loads(cached_data)]

        url = f"https://api.themoviedb.org/3/trending/tv/day?api_key={api_key}&language=en-US&page={page}"
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers)
        
        if response.status_code == 200:
            movies_data = response.json().get("results", [])
            redis_service.set(cache_key, json.dumps(movies_data), ttl=3600)
            return [TMDBMovie(**movie) for movie in movies_data]
        else:
            logger.error(f"Failed to fetch trending TV shows: {response.status_code}")
            return []
    except Exception as e:
        logger.exception(f"Error fetching trending TV shows for page {page}: {e}")
        return []

async def fetch_movie_detail(movie_id: int, user_id: PydanticObjectId = None) -> MovieDetail:
    cache_key = f"movie_detail_{movie_id}"
    try:
        cached_data = redis_service.get(cache_key)
        if cached_data:
            movie_data = json.loads(cached_data)
        else:
            url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US&append_to_response=videos"
            async with httpx.AsyncClient() as client:
                response = await client.get(url, headers=headers)
            
            if response.status_code != 200:
                logger.error(f"Failed to fetch movie detail for ID {movie_id}: {response.status_code}")
                return None
            
            movie_data = response.json()
            redis_service.set(cache_key, json.dumps(movie_data), ttl=36000)

        movie = await retrieve_movie_by_movie_id(movie_data['id'])
        if movie is None:
            await add_movie(movie_data['id'], movie_data['title'])
        await increment_viewcount(movie_data['id'])
        if user_id:
            await add_to_recently_viewed(user_id, movie_data['id'])
        return MovieDetail(**movie_data)
    except Exception as e:
        logger.exception(f"Error fetching movie detail for ID {movie_id}: {e}")
        return None

async def fetch_movie_recommendations(movie_id: int, page: int = 1) -> List[TMDBMovie]:
    cache_key = f"movie_recommendations_{movie_id}"
    try:
        cached_data = redis_service.get(cache_key)
        if cached_data:
            return MovieDetail(**json.loads(cached_data))

        url = f"https://api.themoviedb.org/3/movie/{movie_id}/recommendations?api_key={api_key}&language=en-US&page={page}"
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers)
        
        if response.status_code == 200:
            movies_data = response.json().get("results", [])
            redis_service.set(cache_key, json.dumps(movies_data), ttl=3600)
            return [TMDBMovie(**movie) for movie in movies_data]
        else:
            logger.error(f"Failed to fetch movie recommendations for ID {movie_id}: {response.status_code}")
            return None
    except Exception as e:
        logger.exception(f"Error fetching movie recommendations for ID {movie_id}: {e}")
        return None

async def fetch_movies_by_movie_ids(movie_ids: List[int]) -> List[TMDBMovie]:
    cache_key = f"movies_{'_'.join(map(str, sorted(movie_ids)))}"
    try:
        cached_data = redis_service.get(cache_key)
        if cached_data:
            logger.info(f"Cache hit for key: {cache_key}")
            return [TMDBMovie(**movie) for movie in json.loads(cached_data)]
        else:
            logger.info(f"Cache miss for key: {cache_key}")

        tasks = [fetch_movie_detail(movie_id) for movie_id in movie_ids]
        movies_data = await asyncio.gather(*tasks, return_exceptions=True)

        valid_movies = []
        for movie_id, result in zip(movie_ids, movies_data):
            if isinstance(result, Exception):
                logger.error(f"Error fetching movie detail for ID {movie_id}: {result}")
            else:
                valid_movies.append(result)

        if valid_movies:
            redis_service.set(cache_key, json.dumps([movie.dict() for movie in valid_movies]), ttl=3600)
        else:
            logger.warning(f"No valid movies fetched for IDs: {movie_ids}")

        return valid_movies
    except Exception as e:
        logger.exception(f"Unexpected error in fetch_movies_by_movie_ids: {e}")
        return []

async def fetch_movies_by_keyword(keyword: str, page: int) -> List[TMDBMovie]:
    cache_key = f"movies_keyword_{keyword}"
    try:
        cached_data = redis_service.get(cache_key)
        if cached_data:
            return [TMDBMovie(**movie) for movie in json.loads(cached_data)]

        url = f"https://api.themoviedb.org/3/search/movie?api_key={api_key}&language=en-US&query={keyword}&page={page}"
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers)
        
        if response.status_code == 200:
            movies_data = response.json().get("results", [])
            redis_service.set(cache_key, json.dumps(movies_data), ttl=3600)
            return [TMDBMovie(**movie) for movie in movies_data]
        else:
            logger.error(f"Failed to fetch movies by keyword {keyword}: {response.status_code}")
            return []
    except Exception as e:
        logger.exception(f"Error fetching movies by keyword {keyword}: {e}")
        return []

async def fetch_recently_viewed(user_id: int) -> List[TMDBMovie]:
    try:
        user = await retrieve_user(user_id)
        if user is None or user.recently_viewed is None:
            return []

        return await fetch_movies_by_movie_ids(user.recently_viewed)
    except Exception as e:
        logger.exception(f"Error fetching recently viewed movies for user ID {user_id}: {e}")
        return []

async def fetch_movies_by_genre(page: int, genre_id: int, include_adult: bool) -> List[TMDBMovie]:
    cache_key = f"movies_genre_{genre_id}_page_{page}_adult_{include_adult}"
    try:
        cached_data = redis_service.get(cache_key)
        if cached_data:
            return [TMDBMovie(**movie) for movie in json.loads(cached_data)]
        if not include_adult:
            genre_id = "16,10751"

        url = (
            f"https://api.themoviedb.org/3/discover/movie"
            f"?api_key={api_key}"
            f"&language=en-US"
            f"&page={page}"
            f"&include_adult={include_adult}"
            f"&sort_by=popularity.desc"
            f"&with_genres={genre_id}"
        )

        if not include_adult:
            url += "&certification_country=US&certification.lte=G@sort_by=popularity.desc"

        print("include", include_adult)
        print(url)
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers)

        if response.status_code == 200:
            movies_data = response.json().get("results", [])
            redis_service.set(cache_key, json.dumps(movies_data), ttl=3600)
            return [TMDBMovie(**movie) for movie in movies_data]
        else:
            logger.error(f"Failed to fetch movies for genre {genre_id}: {response.status_code}")
            return []
    except Exception as e:
        logger.exception(f"Error fetching movies for genre {genre_id} on page {page}: {e}")
        return []

async def fetch_genres() -> List[Genre]:
    cache_key = f"genres"
    try:
        cached_data = redis_service.get(cache_key)
        if cached_data:
            return [Genre(**genre) for genre in json.loads(cached_data)]

        url = f"https://api.themoviedb.org/3/genre/movie/list?api_key={api_key}"

        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers)

        if response.status_code == 200:
            genres_data = response.json().get("genres", [])
            redis_service.set(cache_key, json.dumps(genres_data), ttl=3600)
            return [Genre(**genre) for genre in genres_data]
        else:
            logger.error(f"Failed to fetch genres: {response.status_code}")
            return []
    except Exception as e:
        logger.exception(f"Error fetching genres: {e}")
        return []
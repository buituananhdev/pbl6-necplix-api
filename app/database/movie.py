import logging
from typing import List, Union
from beanie import PydanticObjectId
from models.user import User
from models.movie import Movie

movie_collection = Movie
logger = logging.getLogger(__name__)

async def retrieve_movies() -> List[Movie]:
    try:
        movies = await movie_collection.all().to_list()
        return movies
    except Exception as e:
        logger.error(f"Error retrieving movies: {e}")
        return []

async def retrieve_movie(id: PydanticObjectId) -> Union[Movie, None]:
    try:
        movie = await movie_collection.get(id)
        return movie
    except Exception as e:
        logger.error(f"Error retrieving movie with id {id}: {e}")
        return None

async def add_movie(movie_id: int, title: str) -> Union[Movie, None]:
    try:
        new_movie = Movie(movie_id=movie_id, title=title)
        await new_movie.create()
        return new_movie
    except Exception as e:
        logger.error(f"Error adding movie with id {movie_id}, title '{title}': {e}")
        return None

async def delete_movie(id: PydanticObjectId) -> bool:
    try:
        movie = await movie_collection.get(id)
        if movie:
            await movie.delete()
            return True
        return False
    except Exception as e:
        logger.error(f"Error deleting movie with id {id}: {e}")
        return False

async def update_movie_data(id: PydanticObjectId, data: dict) -> Union[bool, Movie]:
    try:
        des_body = {k: v for k, v in data.items() if v is not None}
        update_query = {"$set": {field: value for field, value in des_body.items()}}
        movie = await movie_collection.get(id)
        if movie:
            await movie.update(update_query)
            return movie
        return False
    except Exception as e:
        logger.error(f"Error updating movie with id {id}, data {data}: {e}")
        return False

async def increment_viewcount(movie_id: int) -> Union[bool, Movie]:
    try:
        movie = await movie_collection.find_one({"movie_id": movie_id})
        if movie:
            update_query = {"$inc": {"viewcount": 1}}
            await movie.update(update_query)
            return await movie_collection.get(movie.id)
        return False
    except Exception as e:
        logger.error(f"Error incrementing viewcount for movie with id {movie_id}: {e}")
        return False

async def retrieve_movie_by_movie_id(movie_id: str) -> Union[Movie, None]:
    try:
        movie = await movie_collection.find_one({"movie_id": movie_id})
        return movie
    except Exception as e:
        logger.error(f"Error retrieving movie with movie_id {movie_id}: {e}")
        return None

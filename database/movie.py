from typing import List, Union
from beanie import PydanticObjectId
from models.user import User
from models.movie import Movie

movie_collection = Movie

async def retrieve_movies() -> List[Movie]:
    movies = await movie_collection.all().to_list()
    return movies

async def retrieve_movie(id: PydanticObjectId) -> Movie:
    movie = await movie_collection.get(id)
    if movie:
        return movie

async def add_movie(new_movie: Movie) -> Movie:
    movie = await new_movie.create()
    return movie

async def delete_movie(id: PydanticObjectId) -> bool:
    movie = await movie_collection.get(id)
    if movie:
        await movie.delete()
        return True
    
async def update_movie_data(id: PydanticObjectId, data: dict) -> Union[bool, Movie]:
    des_body = {k: v for k, v in data.items() if v is not None}
    update_query = {"$set": {field: value for field, value in des_body.items()}}
    movie = await movie_collection.get(id)
    if movie:
        await movie.update(update_query)
        return movie
    return False
from typing import List, Union
from beanie import PydanticObjectId
from models.rating import Rating

rating_collection = Rating

async def add_rating(new_rating: Rating) -> Rating:
    rating = await new_rating.create()
    return rating

async def retrieve_ratings() -> List[Rating]:
    ratings = await rating_collection.all().to_list()
    return ratings

async def retrieve_rating(id: PydanticObjectId) -> Rating:
    rating = await rating_collection.get(id)
    if rating:
        return rating

async def delete_rating(id: PydanticObjectId) -> bool:
    rating = await rating_collection.get(id)
    if rating:
        await rating.delete()
        return True

async def update_rating_data(id: PydanticObjectId, data: dict) -> Union[bool, Rating]:
    des_body = {k: v for k, v in data.items() if v is not None}
    update_query = {"$set": {field: value for field, value in des_body.items()}}
    rating = await rating_collection.get(id)
    if rating:
        await rating.update(update_query)
        return rating
    return False

async def retrieve_movies_ratings(movie_id: int) -> List[Rating]:
    ratings = await rating_collection.find({"movie_id": movie_id}).to_list()
    return ratings
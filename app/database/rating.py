from typing import List, Union
from beanie import PydanticObjectId
from models.rating import Rating
from schemas.rating import Response
from schemas.user import UserData
from models.movie import Movie
from fastapi import HTTPException

rating_collection = Rating
movie_collection = Movie
async def add_rating(new_rating: Rating) -> Union[str, Rating]:
    movie = await movie_collection.find_one({"movie_id": new_rating.movie_id})
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found!")

    existing_rating = await rating_collection.find_one({"movie_id": new_rating.movie_id, "user_id": new_rating.user_id})
    if existing_rating:
        raise HTTPException(status_code=409, detail="User already rated this movie!")

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

async def retrieve_movies_ratings(movie_id: int) -> List[dict]:
    ratings = await rating_collection.find(Rating.movie_id == movie_id).to_list()

    rating_response = []
    
    for rating in ratings:
        response = Response(**rating.dict())
        
        if rating.user_id:
            user_data = await rating.user_id.fetch()
            response.user = UserData(**user_data.dict())

        rating_response.append(response)

    return rating_response
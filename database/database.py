from typing import List, Union

from beanie import PydanticObjectId

from models.user import User
from models.rating import Rating

user_collection = User
rating_collection = Rating


async def add_user(new_user: User) -> User:
    user = await new_user.create()
    return user


async def retrieve_ratings() -> List[Rating]:
    ratings = await rating_collection.all().to_list()
    return ratings


async def add_rating(new_rating: Rating) -> Rating:
    rating = await new_rating.create()
    return rating


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

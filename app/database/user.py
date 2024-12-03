from typing import List, Union
from beanie import PydanticObjectId
from models.user import User

user_collection = User

async def add_user(new_user: User) -> User:
    user = await new_user.create()
    return user

async def retrieve_users() -> List[User]:
    users = await user_collection.all().to_list()
    return users

async def retrieve_user(id: PydanticObjectId) -> User:
    user = await user_collection.get(id)
    if user:
        return user

async def delete_user(id: PydanticObjectId) -> bool:
    user = await user_collection.get(id)
    if user:
        await user.delete()
        return True

async def update_user_data(id: PydanticObjectId, data: dict) -> Union[bool, User]:
    des_body = {k: v for k, v in data.items() if v is not None}
    update_query = {"$set": {field: value for field, value in des_body.items()}}
    user = await user_collection.get(id)
    if user:
        await user.update(update_query)
        return user
    return False

async def get_user_by_email(email: str) -> User:
    user = await user_collection.find_one({"email": email})
    return user

async def add_to_recently_viewed(user_id: PydanticObjectId, movie_id: int) -> bool:
    user = await user_collection.get(user_id)
    if user:
        if user.recently_viewed is None:
            user.recently_viewed = []
        if movie_id in user.recently_viewed:
            user.recently_viewed.remove(movie_id)
        
        user.recently_viewed.insert(0, movie_id)
        user.recently_viewed = user.recently_viewed[:10]
        await user.save()
        return True
    return False

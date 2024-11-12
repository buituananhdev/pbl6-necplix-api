from fastapi import APIRouter, Body, Depends
from bson import ObjectId
from database.database import *
from models.rating import Rating
from schemas.rating import Response, UpdateRatingModel
from auth.jwt_bearer import JWTBearer
from auth.jwt_handler import decode_jwt
from beanie import PydanticObjectId

token_listener = JWTBearer()
router = APIRouter()


@router.get("/", response_description="Ratings retrieved", response_model=Response)
async def get_ratings():
    ratings = await retrieve_ratings()
    return {
        "status_code": 200,
        "response_type": "success",
        "description": "Ratings data retrieved successfully",
        "data": ratings,
    }


@router.get("/{id}", response_description="Rating data retrieved", response_model=Response)
async def get_rating_data(id: PydanticObjectId):
    rating = await retrieve_rating(id)
    if rating:
        return {
            "status_code": 200,
            "response_type": "success",
            "description": "Rating data retrieved successfully",
            "data": rating,
        }
    return {
        "status_code": 404,
        "response_type": "error",
        "description": "Rating doesn't exist",
    }


@router.post(
    "/",
    response_description="Rating data added into the database"
)
async def add_rating_data(rating: Rating = Body(...)):
    # print('checekc')
    # print(rating)
    # decoded = decode_jwt(token)
    # rating.user_id = ObjectId(decoded["user_id"])
    new_rating = await add_rating(rating)
    return {
        "status_code": 200,
        "response_type": "success",
        "description": "Rating created successfully",
        "data": new_rating,
    }


@router.delete("/{id}", response_description="Rating data deleted from the database")
async def delete_rating_data(id: PydanticObjectId):
    deleted_rating = await delete_rating(id)
    if deleted_rating:
        return {
            "status_code": 200,
            "response_type": "success",
            "description": "Rating with ID: {} removed".format(id),
            "data": deleted_rating,
        }
    return {
        "status_code": 404,
        "response_type": "error",
        "description": "Rating with id {0} doesn't exist".format(id),
        "data": False,
    }


@router.put("/{id}", response_model=Response)
async def update_rating(id: PydanticObjectId, req: UpdateRatingModel = Body(...)):
    updated_rating = await update_rating_data(id, req.dict())
    if updated_rating:
        return {
            "status_code": 200,
            "response_type": "success",
            "description": "Rating with ID: {} updated".format(id),
            "data": updated_rating,
        }
    return {
        "status_code": 404,
        "response_type": "error",
        "description": "An error occurred. Rating with ID: {} not found".format(id),
        "data": False,
    }

from fastapi import APIRouter, Body, HTTPException, Depends, Query
from database.rating import *
from models.rating import Rating
from schemas.rating import Response, UpdateRatingModel, CreateRatingModel
from auth.jwt_bearer import JWTBearer, get_user_id_from_token
from auth.jwt_handler import decode_jwt
from beanie import PydanticObjectId

token_listener = JWTBearer()
router = APIRouter()

def create_response(status_code: int, response_type: str, description: str, data=None):
    return {
        "status_code": status_code,
        "response_type": response_type,
        "description": description,
        "data": data,
    }

@router.get("", response_description="Ratings retrieved")
async def get_movies_ratings(movie_id: int = Query(...)):
    ratings = await retrieve_movies_ratings(movie_id)
    return create_response(
        status_code=200,
        response_type="success",
        description="Ratings data retrieved successfully",
        data=ratings,
    )


@router.get("/{id}", response_description="Rating data retrieved", response_model=Response)
async def get_rating_data(id: PydanticObjectId):
    rating = await retrieve_rating(id)
    if rating:
        return create_response(
            status_code=200,
            response_type="success",
            description="Rating data retrieved successfully",
            data=rating,
        )
    raise HTTPException(
        status_code=404,
        detail="Rating doesn't exist"
    )


@router.post("", response_description="Rating data added into the database")
async def add_rating_data(create_rating: CreateRatingModel = Body(...), user_id: str = Depends(get_user_id_from_token)):
    rating = Rating(**create_rating.dict(), user_id=user_id)
    print(rating)
    new_rating = await add_rating(rating)
    if new_rating:
        return create_response(
            status_code=200,
            response_type="success",
            description="Rating created successfully",
            data=new_rating,
        )
    raise HTTPException(
        status_code=500,
        detail="Failed to create rating"
    )


@router.delete("/{id}", response_description="Rating data deleted from the database")
async def delete_rating_data(id: PydanticObjectId):
    deleted_rating = await delete_rating(id)
    if deleted_rating:
        return create_response(
            status_code=200,
            response_type="success",
            description=f"Rating with ID: {id} removed",
            data=deleted_rating,
        )
    raise HTTPException(
        status_code=404,
        detail=f"Rating with id {id} doesn't exist"
    )


@router.put("/{id}", response_model=Response)
async def update_rating(id: PydanticObjectId, req: UpdateRatingModel = Body(...)):
    updated_rating = await update_rating_data(id, req.dict())
    if updated_rating:
        return create_response(
            status_code=200,
            response_type="success",
            description=f"Rating with ID: {id} updated",
            data=updated_rating,
        )
    raise HTTPException(
        status_code=404,
        detail=f"An error occurred. Rating with ID: {id} not found"
    )

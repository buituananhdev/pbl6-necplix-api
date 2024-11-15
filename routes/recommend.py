from typing import List, Optional
from fastapi import Body, Depends, APIRouter, HTTPException, status, Query
from recommender.content_based import get_recommendations_fuzzy
import json
router = APIRouter()

@router.get("/content_based_recommend")
async def get_movies_recommend(query: Optional[str] = Query(None, description="Search term for movie title")):
    if not query:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Query parameter cannot be empty"
        )

    # Retrieve movies based on a fuzzy match of the query string
    matching_movies = await get_recommendations_fuzzy(query)  # Assuming this function provides fuzzy matching
    
    if matching_movies:
        return {
            "status_code": 200,
            "response_type": "success",
            "description": "Movies retrieved successfully",
            "data": json.loads(matching_movies),
        }
    return {
        "status_code": 404,
        "response_type": "error",
        "description": "No movies found matching the search term",
    }
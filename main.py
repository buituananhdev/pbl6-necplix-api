from fastapi import FastAPI, Request, Body, Query
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
# from src.recommendations import get_recommendations_fuzzy
from src.cfRecommendation import get_prioritized_recommendations

app = FastAPI(
    title="PBL6",
    debug=True,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)

@app.get("/v1", include_in_schema=False)
async def healthcheck(request: Request) -> JSONResponse:
    return JSONResponse(content={"status": "ok"})

# @app.post("/v1/recommendations", include_in_schema=False)
# async def get_movie_recommendations(request: Request, title: str = Body(...)) -> JSONResponse:
#     result = get_recommendations_fuzzy(title)
#     return JSONResponse(content=result)

@app.post("/v1/CFrecommendations", include_in_schema=False)
async def get_CF_movie_recommendations(
    request: Request, 
    user_id: int = Body(...), 
    search_query: str = Body(...), 
    page: int = Query(1, ge=1), 
    page_size: int = Query(10, ge=1)
) -> JSONResponse:
    # Lấy kết quả recommendation
    result = get_prioritized_recommendations(user_id, search_query)
    
    # Áp dụng pagination
    start = (page - 1) * page_size
    end = start + page_size
    paginated_result = result[start:end]
    
    return JSONResponse(content={
        "page": page,
        "page_size": page_size,
        "total_results": len(result),
        "results": paginated_result
    })

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)

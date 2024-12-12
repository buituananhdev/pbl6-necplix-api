from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

from recommend import router as RecommendRouter
from content_based import initiate_content_based_recommendation_optimized
from collaborative_based import initiate_collaborative_based_recommendation
app = FastAPI()


origins = [
    "http://localhost:3000",
    "https://necplix.site",
    "http://necplix.site"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def start_database():
    # await initiate_content_based_recommendation_optimized()
    await initiate_collaborative_based_recommendation()


@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to this fantastic app."}


app.include_router(RecommendRouter, tags=["Recommender"], prefix="/recommend")
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

from auth.jwt_bearer import JWTBearer
from config.config import initiate_database
from routes.user import router as UserRouter
from routes.tmdb_movie import router as TMDBMovieRouter
from routes.movie import router as MoviesRouter
from routes.rating import router as RatingRouter
app = FastAPI()

token_listener = JWTBearer()

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
    await initiate_database()


@app.get("/", tags=["Root"])
async def read_root():
    await initiate_database()
    return {"message": "Welcome to this fantastic app."}


app.include_router(UserRouter, tags=["Users"], prefix="/users")
app.include_router(TMDBMovieRouter, tags=["TMDB Movies"], prefix="/tmdb-movies",dependencies=[Depends(token_listener)])
app.include_router(MoviesRouter, tags=["Movies"], prefix="/movies", dependencies=[Depends(token_listener)])
app.include_router(RatingRouter,tags=["Ratings"],prefix="/ratings",dependencies=[Depends(token_listener)])
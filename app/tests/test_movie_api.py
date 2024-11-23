import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient
from app import app
from common.config.config import initiate_database  # Đảm bảo sử dụng hàm này
from models.movie import Movie
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

@pytest.fixture(scope="module", autouse=True)
async def setup_database():
    """
    Khởi tạo cơ sở dữ liệu và collection trước khi chạy bài kiểm tra.
    """
    # Khởi tạo cơ sở dữ liệu thông qua initiate_database()
    await initiate_database()

    yield  # Bắt đầu bài kiểm tra

    # Sau khi kiểm tra xong, xóa cơ sở dữ liệu test_db
    client = AsyncIOMotorClient("mongodb://localhost:27017")
    database = client.get_database("test_db")
    await database.client.drop_database("test_db")


@pytest.mark.anyio
async def test_get_movies():
    """
    Kiểm tra API GET /movies/
    """
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/movies/")
        assert response.status_code == 200
        assert response.json()["status_code"] == 200
        assert isinstance(response.json()["data"], list)


@pytest.mark.anyio
async def test_add_movie():
    """
    Kiểm tra API POST /movies/
    """
    movie_data = {
        "movie_id": 912649,
        "title": "Venom: The Last Dance",
        "genre_ids": [28, 878, 12]
    }
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("/movies/", json=movie_data)
        assert response.status_code == 200
        assert response.json()["data"]["movie_id"] == movie_data["movie_id"]


@pytest.mark.anyio
async def test_get_movie_by_id():
    """
    Kiểm tra API GET /movies/{id}
    """
    # Chèn dữ liệu test trước
    movie = Movie(movie_id=912649, title="Venom: The Last Dance", genre_ids=[28, 878, 12])
    await movie.insert()

    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get(f"/movies/{movie.id}")
        assert response.status_code == 200
        assert response.json()["data"]["title"] == "Venom: The Last Dance"


@pytest.mark.anyio
async def test_update_movie():
    """
    Kiểm tra API PUT /movies/{id}
    """
    # Chèn dữ liệu test trước
    movie = Movie(movie_id=912649, title="Venom: The Last Dance", genre_ids=[28, 878, 12])
    await movie.insert()

    update_data = {"title": "Venom: Updated Title"}
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.put(f"/movies/{movie.id}", json=update_data)
        assert response.status_code == 200
        assert response.json()["data"]["title"] == "Venom: Updated Title"


@pytest.mark.anyio
async def test_delete_movie():
    """
    Kiểm tra API DELETE /movies/{id}
    """
    # Chèn dữ liệu test trước
    movie = Movie(movie_id=912649, title="Venom: The Last Dance", genre_ids=[28, 878, 12])
    await movie.insert()

    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.delete(f"/movies/{movie.id}")
        assert response.status_code == 200
        assert response.json()["description"] == f"Movie with ID: {movie.id} removed"

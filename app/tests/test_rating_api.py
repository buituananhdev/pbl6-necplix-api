import pytest
from httpx import AsyncClient
from app import app
from common.config.config import initiate_database
from models.rating import Rating
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient


@pytest.fixture(scope="module", autouse=True)
async def setup_database():
    """
    Khởi tạo cơ sở dữ liệu và collection trước khi chạy bài kiểm tra.
    """
    # Sử dụng hàm initiate_database() để khởi tạo
    await initiate_database()

    yield  # Dừng trước khi bài kiểm tra kết thúc

    # Sau khi kiểm tra xong, xóa cơ sở dữ liệu test_db
    client = AsyncIOMotorClient("mongodb://localhost:27017")
    database = client.get_database("test_db")
    await database.client.drop_database("test_db")


@pytest.mark.anyio
async def test_get_ratings():
    """
    Kiểm tra API GET /ratings/
    """
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/ratings/")
        assert response.status_code == 200
        assert response.json()["status_code"] == 200
        assert isinstance(response.json()["data"], list)


@pytest.mark.anyio
async def test_add_rating():
    """
    Kiểm tra API POST /ratings/
    """
    rating_data = {
        "movie_id": 123,
        "rating": 4,
        "timestamp": "2024-11-22T12:00:00Z"
    }
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("/ratings/", json=rating_data)
        assert response.status_code == 200
        assert response.json()["data"]["movie_id"] == rating_data["movie_id"]
        assert response.json()["data"]["rating"] == rating_data["rating"]


@pytest.mark.anyio
async def test_get_rating_by_id():
    """
    Kiểm tra API GET /ratings/{id}
    """
    # Chèn dữ liệu test trước
    rating = Rating(movie_id=123, rating=4)
    await rating.insert()

    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get(f"/ratings/{rating.id}")
        assert response.status_code == 200
        assert response.json()["data"]["movie_id"] == 123
        assert response.json()["data"]["rating"] == 4


@pytest.mark.anyio
async def test_update_rating():
    """
    Kiểm tra API PUT /ratings/{id}
    """
    # Chèn dữ liệu test trước
    rating = Rating(movie_id=123, rating=4)
    await rating.insert()

    update_data = {"rating": 5}
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.put(f"/ratings/{rating.id}", json=update_data)
        assert response.status_code == 200
        assert response.json()["data"]["rating"] == 5


@pytest.mark.anyio
async def test_delete_rating():
    """
    Kiểm tra API DELETE /ratings/{id}
    """
    # Chèn dữ liệu test trước
    rating = Rating(movie_id=123, rating=4)
    await rating.insert()

    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.delete(f"/ratings/{rating.id}")
        assert response.status_code == 200
        assert response.json()["description"] == f"Rating with ID: {rating.id} removed"

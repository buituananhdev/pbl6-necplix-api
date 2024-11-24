import pytest
from httpx import AsyncClient
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from app import app
from models.movie import Movie
from app import app, token_listener


@pytest.fixture(scope="module", autouse=True)
async def init_test_db():
    """
    Khởi tạo cơ sở dữ liệu test cho Beanie.
    """
    client = AsyncIOMotorClient("mongodb://localhost:27017")  # Thay đổi nếu dùng URI khác
    test_db = client.get_database("test_db")
    await init_beanie(database=test_db, document_models=[Movie])

    yield  # Cung cấp database cho các test

    # Dọn dẹp database sau khi test
    await test_db.client.drop_database("test_db")

def mock_no_authentication():
    app.dependency_overrides[token_listener] = lambda: {}


@pytest.fixture
async def client():
    """
    Tạo một client để test FastAPI app.
    """
    async with AsyncClient(app=app, base_url="http://testserver") as ac:
        yield ac

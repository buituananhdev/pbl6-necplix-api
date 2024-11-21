# """Tests fixtures."""
# from beanie import init_beanie
# import pytest
# from asgi_lifespan import LifespanManager
# from httpx import AsyncClient

# from app import app
# from mongomock_motor import AsyncMongoMockClient
# from config.config import initiate_database

# import models as models
# from app import app, token_listener


# async def mock_database():
#     client = AsyncMongoMockClient()
#     await init_beanie(
#         database=client["database_name"],
#         recreate_views=True,
#         document_models=models.__all__,
#     )


# def mock_no_authentication():
#     app.dependency_overrides[token_listener] = lambda: {}


# @pytest.fixture
# async def client_test(mocker):
#     """
#     Create an instance of the client.
#     :return: yield HTTP client.
#     """

#     mocker.patch("config.config.initiate_database", return_value=await mock_database())

#     async with LifespanManager(app):
#         async with AsyncClient(
#             app=app, base_url="http://test", follow_redirects=True
#         ) as ac:
#             yield ac


# @pytest.fixture
# def anyio_backend():
#     return "asyncio"







import pytest
from httpx import AsyncClient
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from app import app
from models.movie import Movie
from config.config import Settings

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


@pytest.fixture
async def client():
    """
    Tạo một client để test FastAPI app.
    """
    async with AsyncClient(app=app, base_url="http://testserver") as ac:
        yield ac

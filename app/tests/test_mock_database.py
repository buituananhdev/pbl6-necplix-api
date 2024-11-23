import asyncio
from beanie import init_beanie
from fastapi.testclient import TestClient
from httpx import AsyncClient
import pytest

from models.user import User
from models.rating import Rating
from tests.conftest import mock_no_authentication


class TestMockAuthentication:
    @classmethod
    def setup_class(cls):
        mock_no_authentication()

    @pytest.mark.anyio
    async def test_mock_databases(self, client_test: AsyncClient):
        # generate data
        await User(
            fullname="user", email="user@user.com", password="user"
        ).create()

        await Rating(
            fullname="rating",
            email="rating@rating.com",
            course_of_study="computer science",
            year=2021,
            gpa=4.0,
        ).create()

        response = await client_test.get("rating")

        assert response.status_code == 200

    @pytest.mark.anyio
    async def test_mock_database(self, client_test: AsyncClient):
        await User(
            fullname="user", email="user@user.com", password="user"
        ).create()

        await Rating(
            fullname="rating",
            email="rating@rating.com",
            course_of_study="computer science",
            year=2021,
            gpa=4.0,
        ).create()

        response = await client_test.get("rating")

        assert response.status_code == 200

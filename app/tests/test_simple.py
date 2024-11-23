# test_simple.py
import pytest
from fastapi import FastAPI
from httpx import AsyncClient

app = FastAPI()

@app.get("/")
async def read_root():
    return {"message": "Hello, World!"}

@pytest.mark.asyncio
async def test_root():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello, World!"}

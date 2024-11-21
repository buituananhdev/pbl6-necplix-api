import pytest
from fastapi.testclient import TestClient

@pytest.mark.parametrize(
    "endpoint, page, expected_status",
    [
        ("/polular", 1, 200),
        ("/trending", 1, 200),
        ("/tv/popular", 1, 200),
        ("/tv/trending", 1, 200),
    ],
)
def test_get_movies_list(client: TestClient, endpoint: str, page: int, expected_status: int):
    """
    Kiểm tra các API lấy danh sách phim.
    """
    response = client.get(endpoint, params={"page": page})
    assert response.status_code == expected_status
    json_data = response.json()
    assert json_data["status_code"] == 200
    assert json_data["response_type"] == "success"
    assert "data" in json_data

def test_get_movie_detail_success(client: TestClient):
    """
    Kiểm tra API lấy chi tiết phim (thành công).
    """
    movie_id = 123  # Thay thế bằng ID phim hợp lệ
    response = client.get("/", params={"movie_id": movie_id})
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["status_code"] == 200
    assert json_data["response_type"] == "success"
    assert "data" in json_data

def test_get_movie_detail_not_found(client: TestClient):
    """
    Kiểm tra API lấy chi tiết phim (không tìm thấy).
    """
    invalid_movie_id = -1  # ID không hợp lệ
    response = client.get("/", params={"movie_id": invalid_movie_id})
    assert response.status_code == 404
    json_data = response.json()
    assert json_data["detail"] == "Movie not found"

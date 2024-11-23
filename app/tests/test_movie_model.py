import pytest
from pydantic import ValidationError
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from models.movie import Movie

# Sử dụng pytest-asyncio để hỗ trợ kiểm thử bất đồng bộ
@pytest.mark.asyncio
async def test_movie_model():
    # Khởi tạo cơ sở dữ liệu giả lập (in-memory) để kiểm thử
    client = AsyncIOMotorClient("mongodb://localhost:27017")  # Đảm bảo rằng MongoDB đang chạy ở địa chỉ này
    database = client.get_database("test_db")  # Tạo database thử nghiệm
    await init_beanie(database, document_models=[Movie])  # Khởi tạo Beanie với database thử nghiệm

    # Tạo một Movie mới
    movie = Movie(movie_id=912649, title="Venom: The Last Dance", genre_ids=[28, 878, 12])

    # Kiểm tra các giá trị trong object Movie
    assert movie.movie_id == 912649
    assert movie.title == "Venom: The Last Dance"
    assert movie.genre_ids == [28, 878, 12]

    # Kiểm tra nếu insert vào cơ sở dữ liệu hoạt động đúng
    await movie.insert()

    # Tìm lại movie từ database để kiểm tra
    stored_movie = await Movie.get(movie.id)
    assert stored_movie.movie_id == movie.movie_id
    assert stored_movie.title == movie.title
    assert stored_movie.genre_ids == movie.genre_ids

    # Kiểm tra validate dữ liệu không hợp lệ
    with pytest.raises(ValidationError):
        invalid_movie = Movie(movie_id="string_instead_of_int", title="Invalid Movie")
        await invalid_movie.insert()

    # Kiểm tra default giá trị (genre_ids mặc định là [])
    movie_without_genres = Movie(movie_id=912650, title="No Genres")
    assert movie_without_genres.genre_ids == []

    # Xóa dữ liệu sau khi kiểm thử
    await movie.delete()
    await movie_without_genres.delete()


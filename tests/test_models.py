import pytest
from pydantic import ValidationError
from beanie import init_beanie, Document, Link
from motor.motor_asyncio import AsyncIOMotorClient
from models.movie import Movie
from typing import List
from models.user import User
from models.rating import Rating
from datetime import datetime
from bson import ObjectId

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

# Khởi tạo pytest-asyncio để hỗ trợ kiểm thử bất đồng bộ
@pytest.mark.asyncio
async def test_user_model():
    # Khởi tạo cơ sở dữ liệu thử nghiệm
    client = AsyncIOMotorClient("mongodb://localhost:27017")  # Đảm bảo MongoDB đang chạy ở địa chỉ này
    database = client.get_database("test_db")  # Tạo database thử nghiệm
    await init_beanie(database, document_models=[User])  # Khởi tạo Beanie với mô hình User

    # Tạo đối tượng User mới
    user = User(fullname="Bui Tuan Anh", email="anhaanh2003@gmail.com", password="3xt3m#", user_id=1)

    # Kiểm tra các giá trị trong đối tượng User
    assert user.fullname == "Bui Tuan Anh"
    assert user.email == "anhaanh2003@gmail.com"
    assert user.password == "3xt3m#"
    assert user.user_id == 1

    # Kiểm tra chức năng insert vào cơ sở dữ liệu
    await user.insert()

    # Kiểm tra lấy lại đối tượng User từ cơ sở dữ liệu
    stored_user = await User.get(user.id)
    assert stored_user.fullname == user.fullname
    assert stored_user.email == user.email
    assert stored_user.password == user.password
    assert stored_user.user_id == user.user_id

    # Kiểm tra validate dữ liệu không hợp lệ
    with pytest.raises(ValidationError):
        invalid_user = User(fullname="Invalid User", email="invalid_email", password="short", user_id=1)
        await invalid_user.insert()

    # Xóa dữ liệu sau khi kiểm thử
    await user.delete()



class Rating(Document):
    user_id: Link[User]  # Sử dụng Link cho mối quan hệ với User
    movie_id: int
    rating: int
    timestamp: datetime


@pytest.mark.asyncio
async def test_rating_model():
    # Khởi tạo cơ sở dữ liệu thử nghiệm
    client = AsyncIOMotorClient("mongodb://localhost:27017")  # Đảm bảo MongoDB đang chạy ở địa chỉ này      
    database = client.get_database("test_db")  # Tạo database thử nghiệm
    await init_beanie(database, document_models=[Rating, User])  # Khởi tạo Beanie với mô hình Rating và User
    
    # Tạo đối tượng User
    user = User(fullname="Nguyen Binh Minh", email="nbinhminh158@gmail.com", password="@123456Aa", user_id=1)
    await user.insert()

    # Tạo đối tượng Rating cho User, sử dụng user.id cho user_id
    rating = Rating(user_id=user, movie_id=123, rating=4, timestamp=datetime(2024, 11, 17, 12, 0, 0))

    # Kiểm tra các giá trị trong đối tượng Rating
    assert rating.user_id.id == user.id  # So sánh ObjectId với ObjectId

    # Kiểm tra các thuộc tính còn lại
    assert rating.movie_id == 123
    assert rating.rating == 4
    assert isinstance(rating.timestamp, datetime)  # Kiểm tra kiểu dữ liệu timestamp

    # Kiểm tra insert vào cơ sở dữ liệu
    await rating.insert()

    # Lấy lại Rating từ cơ sở dữ liệu
    stored_rating = await Rating.get(rating.id)

    # Fetch User từ user_id của Rating và so sánh với user.id
    stored_user = await stored_rating.user_id.fetch()
    assert stored_user.id == user.id  # So sánh ObjectId của stored_user với user.id

    # Xóa dữ liệu sau khi kiểm thử
    await rating.delete()
    await user.delete()

import pytest
from beanie import init_beanie, Document, Link
from motor.motor_asyncio import AsyncIOMotorClient
from models.user import User
from models.rating import Rating
from datetime import datetime

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

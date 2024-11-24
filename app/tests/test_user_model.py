import pytest
from pydantic import ValidationError
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from models.user import User

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

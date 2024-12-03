from beanie import Document, Link
from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional, List
from datetime import datetime
from beanie import PydanticObjectId

class User(Document):
    fullname: str
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    age: Optional[int] = None
    is_active: bool = True
    created_at: datetime = datetime.now()
    parent_id: PydanticObjectId = None
    user_id: Optional[int] = None
    recently_viewed: Optional[List[int]] = []

    class Config:
        json_schema_extra = {
            "example": {
                "fullname": "Bui Tuan Anh",
                "email": "anhaanh2003@gmail.com",
                "password": "3xt3m#",
                "age": 21,
                "is_active": True,
                "created_at": "2024-11-24T12:00:00Z"
            }
        }
    class Settings:
        name = "users"
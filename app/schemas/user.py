from pydantic import BaseModel, Field, EmailStr
from fastapi.security import HTTPBasicCredentials
from typing import Optional
from beanie import PydanticObjectId

class UserSignIn(HTTPBasicCredentials):
    class Config:
        json_schema_extra = {
            "example": {
                "username": "anhaanh2003@gmail.com",
                "password": "3xt3m#"
            }
        }

class UserSignUp(BaseModel):
    fullname: str = Field(..., max_length=100, example="Bui Tuan Anh")
    email: EmailStr = Field(..., example="anhaanh2003@gmail.com")
    password: str = Field(..., min_length=6, example="3xt3m#")
    age: Optional[int] = Field(None, ge=0, example=21)

    class Config:
        json_schema_extra = {
            "example": {
                "fullname": "Bui Tuan Anh",
                "email": "anhaanh2003@gmail.com",
                "password": "3xt3m#",
                "age": 21,
            }
        }

class UserData(BaseModel):
    fullname: str
    email: EmailStr
    age: int
    parent_id: Optional[PydanticObjectId] = None

    class Config:
        json_schema_extra = {
            "example": {
                "fullname": "Bui Tuan Anh",
                "email": "anhaanh2003@gmail.com",
                "age": 1
            }
        }

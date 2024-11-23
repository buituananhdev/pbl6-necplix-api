from pydantic import BaseModel
from fastapi.security import HTTPBasicCredentials
from pydantic import EmailStr

class UserSignIn(HTTPBasicCredentials):
    class Config:
        json_schema_extra = {
            "example": {"username": "anhaanh2003@gmail.com", "password": "3xt3m#"}
        }


class UserData(BaseModel):
    fullname: str
    email: EmailStr
    user_id: int

    class Config:
        json_schema_extra = {
            "example": {
                "fullname": "Bui Tuan Anh",
                "email": "anhaanh2003@gmail.com",
                "user_id": 1
            }
        }

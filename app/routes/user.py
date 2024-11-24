from fastapi import Body, Depends, APIRouter, HTTPException, status
from passlib.context import CryptContext

from auth.jwt_bearer import JWTBearer, get_user_id_from_token
from auth.jwt_handler import sign_jwt, decode_jwt
from database.user import add_user
from models.user import User
from schemas.user import UserData, UserSignIn, UserSignUp

router = APIRouter()

hash_helper = CryptContext(schemes=["bcrypt"])


@router.post("/login")
async def user_login(user_credentials: UserSignIn = Body(...)):
    user_exists = await User.find_one({"email": user_credentials.username})
    
    if user_exists:
        password_correct = hash_helper.verify(user_credentials.password, user_exists.password)
        if password_correct:
            return sign_jwt(str(user_exists.id))

        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect email or password")
    
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect email or password")

@router.get("/get-me", response_model=UserData)
async def get_me(user_id: str = Depends(get_user_id_from_token)):
    print(user_id)
    user = await User.find_one({"_id": user_id})
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    return UserData(**user.dict())

@router.post("", response_model=UserData)
async def user_signup(user_sign_up: UserSignUp = Body(...)):
    user_exists = await User.find_one(User.email == user_sign_up.email)
    if user_exists:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="User with email supplied already exists"
        )
    user = User(**user_sign_up.dict())
    user.password = hash_helper.encrypt(user.password)
    new_user = await add_user(user)
    return new_user

from fastapi import Body, Depends, APIRouter, HTTPException, status
from passlib.context import CryptContext

from auth.jwt_bearer import JWTBearer
from auth.jwt_handler import sign_jwt, decode_jwt
from database.database import add_user
from models.user import User
from schemas.user import UserData, UserSignIn

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
@router.get("/get-me", response_model=UserData, dependencies=[Depends(JWTBearer())])
async def get_me(token: str = Depends(JWTBearer())):
    payload = decode_jwt(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )
    
    email = payload.get("email")
    if email is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token data",
        )
    
    user = await User.find_one(User.email == email)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    
    return UserData(**user.dict())

@router.post("", response_model=UserData)
async def user_signup(user: User = Body(...)):
    user_exists = await User.find_one(User.email == user.email)
    if user_exists:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="User with email supplied already exists"
        )

    user.password = hash_helper.encrypt(user.password)
    new_user = await add_user(user)
    return new_user

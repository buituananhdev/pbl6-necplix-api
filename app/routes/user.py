from fastapi import Body, Depends, APIRouter, HTTPException, status
from passlib.context import CryptContext
from auth.jwt_bearer import get_current_user
from auth.jwt_handler import sign_jwt
from database.user import add_user, get_user_by_email
from models.user import User
from schemas.user import *

router = APIRouter()

hash_helper = CryptContext(schemes=["bcrypt"])


@router.post("/login")
async def user_login(user_credentials: UserSignIn = Body(...)):
    user_exists = await User.find_one({"email": user_credentials.username})
    
    if user_exists:
        password_correct = hash_helper.verify(user_credentials.password, user_exists.password)
        if password_correct:
            return sign_jwt(str(user_exists.id), user_exists.age)

        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect email or password")
    
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect email or password")

@router.get("/get-me", response_model=UserData)
async def get_me(user: TokenUserPayload = Depends(get_current_user)):
    user = await User.find_one({"_id": user.user_id})
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    return UserData(**user.dict())

@router.post("", response_model=UserData)
async def user_signup(user_sign_up: UserSignUp = Body(...)):
    user_exists = await get_user_by_email(user_sign_up.email)
    if user_exists:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="User with email supplied already exists"
        )
    user = User(**user_sign_up.dict())
    user.password = hash_helper.encrypt(user.password)
    new_user = await add_user(user)
    return new_user

@router.post("/childs", response_model=UserData)
async def create_child(
    user_sign_up: ChildSignUp = Body(...),
    parent: TokenUserPayload = Depends(get_current_user),
):
    user = User(**user_sign_up.dict())
    user.parent_id = parent.user_id
    await add_user(user)

    return UserData(
        fullname=user.fullname,
        age=user.age,
        parent_id=user.parent_id
    )

@router.get("/childs", response_model=list[UserData])
async def get_childs(parent: TokenUserPayload = Depends(get_current_user)):
    users = await User.find(User.parent_id == parent.user_id).to_list()
    return users

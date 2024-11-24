from fastapi import Body, Depends, APIRouter, HTTPException, status
from passlib.context import CryptContext
from bson import ObjectId
from auth.jwt_bearer import JWTBearer, get_user_id_from_token
from auth.jwt_handler import sign_jwt, decode_jwt
from database.user import add_user, get_user_by_email
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
    user = await User.find_one({"_id": user_id})
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
async def user_signup(
    user_sign_up: UserSignUp = Body(...),
    parent_id: ObjectId = Depends(get_user_id_from_token),
):
    user_exists = await User.find_one({"email": user_sign_up.email})
    if user_exists:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="User with email supplied already exists"
        )

    user = User(**user_sign_up.dict())
    user.password = hash_helper.encrypt(user.password)
    user.parent_id = parent_id
    await user.insert()

    return UserData(
        fullname=user.fullname,
        email=user.email,
        age=user.age,
        is_active=user.is_active,
        created_at=user.created_at,
    )

@router.get("/childs", response_model=list[UserData])
async def get_childs(parent_id: str = Depends(get_user_id_from_token)):
    users = await User.find(User.parent_id == parent_id).to_list()
    return users

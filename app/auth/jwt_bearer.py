from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends, HTTPException
from beanie import PydanticObjectId

from .jwt_handler import decode_jwt


def verify_jwt(jwtoken: str) -> bool:
    isTokenValid: bool = False

    payload = decode_jwt(jwtoken)
    if payload:
        isTokenValid = True
    return isTokenValid


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(
            JWTBearer, self
        ).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(
                    status_code=403, detail="Invalid authentication token"
                )

            if not verify_jwt(credentials.credentials):
                raise HTTPException(
                    status_code=403, detail="Invalid token or expired token"
                )

            return credentials.credentials
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization token")

async def get_user_id_from_token(token: str = Depends(JWTBearer())) -> PydanticObjectId:
    payload = decode_jwt(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    user_id = payload.get("user_id")
    if user_id is None or not PydanticObjectId.is_valid(user_id):
        raise HTTPException(status_code=401, detail="Invalid token data")

    return PydanticObjectId(user_id)
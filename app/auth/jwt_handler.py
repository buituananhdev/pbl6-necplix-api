import time
from typing import Dict

import jwt
from common.config.config import Settings

def token_response(token: str):
    return {"access_token": token}


secret_key = Settings().secret_key


def sign_jwt(user_id: str, age: int) -> Dict[str, str]:
    # Set the expiry time to 1 hour (3600 seconds).
    payload = {"user_id": user_id, "age": age, "expires": time.time() + 3600}
    return token_response(jwt.encode(payload, secret_key, algorithm="HS256"))


def decode_jwt(token: str) -> dict:
    decoded_token = jwt.decode(token.encode(), secret_key, algorithms=["HS256"])
    return decoded_token if decoded_token["expires"] >= time.time() else {}

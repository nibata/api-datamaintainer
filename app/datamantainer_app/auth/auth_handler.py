import jwt
import time
from typing import Dict, List
from ..configs import settings
from ..models.authentication.groups import Group


JWT_SECRET = settings.JWT_SECRET
JWT_ALGORITHM = settings.JWT_ALGORITHM


def token_response(token: str):
    return {
        "access_token": token
    }


def sign_jwt(user_id: str, roles: List[Group]) -> Dict[str, str]:
    roles_list = [role.Code for role in roles]
    payload = {
        "user_id": user_id,
        "roles": roles_list,
        "expires": time.time() + (24 * 60 * 60)  # 24 hr
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

    return token_response(token)


def decode_jwt(token: str) -> dict:
    try:
        decoded_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return decoded_token if decoded_token["expires"] >= time.time() else None

    except:
        return {}

import time
from typing import Dict, List

import jwt
from ..configs import settings
from ..models.groups import Groups


JWT_SECRET = settings.JWT_SECRET
JWT_ALGORITHM = settings.JWT_ALGORITHM


def token_response(token: str):
    return {
        "access_token": token
    }


def signJWT(user_id: str, roles: List[Groups]) -> Dict[str, str]:
    roles_list = [role.code for role in roles]
    payload = {
        "user_id": user_id,
        "roles": roles_list,
        "expires": time.time() + 600
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

    return token_response(token)


def decodeJWT(token: str) -> dict:
    try:
        decoded_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return decoded_token if decoded_token["expires"] >= time.time() else None
    except:
        return {}
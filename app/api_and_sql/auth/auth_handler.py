import logging

from ..models.authentication.groups import Group
from ..modules.encrypter_module import Encrypter
from ..configs import settings
from typing import Dict, List
import time
import jwt


JWT_SECRET = settings.JWT_SECRET
JWT_ALGORITHM = settings.JWT_ALGORITHM


def token_response(token: str):
    return {
        "access_token": token
    }


def sign_jwt(user_id: str, roles: List[Group]) -> Dict[str, str]:
    encrypter = Encrypter(settings.CRYPTO_KEY)
    roles_list = [role.code for role in roles]

    data = {
        "user_id": user_id,
        "roles": roles_list,
        "expires": time.time() + (24 * 60 * 60)  # 24 hr
    }

    encrypted_data = encrypter.encrypt(data)
    payload = {"info": encrypted_data}
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

    return token_response(token)


def decode_jwt(token: str) -> dict:
    try:
        encrypter = Encrypter(settings.CRYPTO_KEY)
        decoded_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        decoded_payload = encrypter.decrypt(decoded_token["info"])

        return decoded_payload if decoded_payload["expires"] >= time.time() else None

    except Exception as er:
        raise Exception(f"Error al obtener token: {er}")

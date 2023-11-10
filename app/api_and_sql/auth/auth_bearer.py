from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Request, HTTPException
from .auth_handler import decode_jwt
from typing import List


class JWTBearer(HTTPBearer):
    def __init__(self, required_permission: List[str], auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)
        self.required_permission: List[str] = required_permission

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)

        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Invalid authentication scheme.")
            
            if not self.verify_jwt(credentials.credentials):
                raise HTTPException(status_code=403, detail="Invalid token or expired token.")
            
            return credentials.credentials
        
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")

    def verify_jwt(self, jwt_token: str) -> bool:
        is_token_valid: bool = False

        try:
            payload = decode_jwt(jwt_token)

        except:
            payload = None
            
        if payload:
            user_roles = payload["roles"]
            is_token_valid = any(role in self.required_permission for role in user_roles)
            
        return is_token_valid

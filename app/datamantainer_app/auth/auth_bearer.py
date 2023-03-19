from typing import List
from .auth_handler import decodeJWT
from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials


class JWTBearer(HTTPBearer):
    def __init__(self, required_permision: List[str], auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

        self.required_permision: List[str] = required_permision


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
        isTokenValid: bool = False

        try:
            payload = decodeJWT(jwt_token)

        except:
            payload = None
            
        if payload:
            user_roles = payload["roles"]
            isTokenValid = any(role in self.required_permision for role in user_roles)
            
        return isTokenValid

import jwt
import time
from decouple import config
from fastapi import HTTPException, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials


JWT_SECRET = config("secret")
JWT_ALGORITHM = config("algorithm")

def token_response(token:str):
    return{
        "access_token": token
    }

def generate_token(user_id:int):
    payload = {
        "user_id": user_id,
        "expires": time.time() + 6000

    }
    token = jwt.encode(payload, JWT_SECRET, algorithm = JWT_ALGORITHM)

    return token_response(token)

def decode_jwt(token:str):
    try:
        decode_token = jwt.decode(token, JWT_SECRET, algorithms = [JWT_ALGORITHM])
        return decode_token if decode_token["expires"] >= time.time() else None 
    except:
        return {}


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

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

    def verify_jwt(self, jwtoken: str) -> bool:
        isTokenValid: bool = False

        try:
            payload = decode_jwt(jwtoken)
        except:
            payload = None
        if payload:
            isTokenValid = True

        return isTokenValid
 


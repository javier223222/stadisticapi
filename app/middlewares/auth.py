import os
import jwt
from fastapi import HTTPException
from fastapi.requests import Request


SECRET_KEY = os.getenv("JWT_SECRET")

def verify_token(request: Request):
    try:
        token = request.headers.get("Authorization")
        if not token:
            raise HTTPException(status_code=401, detail="Token is missing")
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload
    except Exception as e:
        print(e)
        raise HTTPException(status_code=401, detail="Invalid token")
       
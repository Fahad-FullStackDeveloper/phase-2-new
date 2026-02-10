from fastapi import HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from typing import Optional
from ..config import BETTER_AUTH_SECRET
from ..models.user import User


security = HTTPBearer()


def verify_token(token: str) -> dict:
    """
    Verify the JWT token and return the payload
    """
    try:
        payload = jwt.decode(
            token, 
            BETTER_AUTH_SECRET, 
            algorithms=["HS256"],
            options={"verify_aud": False}  # Better Auth tokens may not have aud claim
        )
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
    """
    Get the current user ID from the JWT token
    """
    token = credentials.credentials
    payload = verify_token(token)
    
    user_id: str = payload.get("userId")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return user_id
from fastapi import APIRouter, HTTPException, status, Depends, Form
from sqlmodel import Session
from typing import Optional
from jose import jwt
from datetime import datetime, timedelta
from database.database import get_session
from config import BETTER_AUTH_SECRET
from models.user import User
from services.auth_service import authenticate_user, get_user_by_email, create_user
from models.task import Task

router = APIRouter()


@router.post("/register")
async def register_user(
    email: str = Form(...),
    password: str = Form(...),
    name: str = Form(None),
    session: Session = Depends(get_session)
):
    """
    Register a new user
    """
    # Check if user already exists
    existing_user = get_user_by_email(session, email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A user with this email already exists"
        )

    # Create new user
    user = create_user(session, email, password, name)

    # Create JWT token for the new user
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user.email, "userId": user.id}, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer", "user_id": user.id}


@router.post("/login")
async def login_user(
    email: str = Form(...),
    password: str = Form(...),
    session: Session = Depends(get_session)
):
    """
    Authenticate user and return JWT token
    """
    user = authenticate_user(session, email, password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create JWT token
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user.email, "userId": user.id}, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer", "user_id": user.id}


@router.get("/me")
def get_current_user():
    """
    Get the current authenticated user
    This is a placeholder - actual implementation depends on Better Auth integration
    """
    # In a real implementation, this would extract user info from the JWT
    # that was validated by the middleware
    return {"message": "User info would be returned here based on JWT"}


@router.post("/logout")
def logout():
    """
    Logout the current user
    This is a placeholder - actual implementation depends on Better Auth integration
    """
    return {"message": "Logged out successfully"}


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    Create a JWT access token
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, BETTER_AUTH_SECRET, algorithm="HS256")
    return encoded_jwt
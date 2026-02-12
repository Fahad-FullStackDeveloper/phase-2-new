from sqlmodel import Session, select
from fastapi import HTTPException, status
from typing import Optional
from models.user import User
from passlib.context import CryptContext


# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against a hashed password"""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Hash a plain password"""
    return pwd_context.hash(password)


def authenticate_user(session: Session, email: str, password: str) -> Optional[User]:
    """Authenticate a user by email and password"""
    statement = select(User).where(User.email == email)
    user = session.exec(statement).first()
    
    if not user or not verify_password(password, user.password):
        return None
    
    return user


def get_user_by_email(session: Session, email: str) -> Optional[User]:
    """Get a user by email"""
    statement = select(User).where(User.email == email)
    return session.exec(statement).first()


def create_user(session: Session, email: str, password: str, name: Optional[str] = None) -> User:
    """Create a new user with hashed password"""
    hashed_password = get_password_hash(password)
    
    user = User(
        email=email,
        password=hashed_password,
        name=name
    )
    
    session.add(user)
    session.commit()
    session.refresh(user)
    
    return user
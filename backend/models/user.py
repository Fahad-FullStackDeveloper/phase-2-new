from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime


class UserBase(SQLModel):
    email: str = Field(unique=True, index=True)
    name: Optional[str] = Field(default=None)


class User(UserBase, table=True):
    id: str = Field(default=None, primary_key=True)  # Using string ID as managed by Better Auth
    password: str = Field()  # Hashed password
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
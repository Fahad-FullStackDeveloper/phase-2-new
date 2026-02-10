from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime


class TaskBase(SQLModel):
    title: str = Field(min_length=1, max_length=50)
    description: Optional[str] = Field(default=None, max_length=500)
    completed: bool = Field(default=False)


class Task(TaskBase, table=True):
    id: int = Field(default=None, primary_key=True)
    user_id: str = Field(foreign_key="user.id", index=True)  # Foreign key to User.id
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class TaskUpdate(SQLModel):
    title: Optional[str] = Field(default=None, min_length=1, max_length=50)
    description: Optional[str] = Field(default=None, max_length=500)
    completed: Optional[bool] = Field(default=None)


class TaskCreate(TaskBase):
    pass  # Inherits all fields from TaskBase
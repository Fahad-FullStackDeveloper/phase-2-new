from sqlmodel import Session, select
from fastapi import HTTPException, status
from typing import List, Optional
from models.task import Task, TaskCreate, TaskUpdate
from models.user import User


def get_tasks_by_user_id(
    session: Session, 
    user_id: str, 
    skip: int = 0, 
    limit: int = 100, 
    completed: Optional[bool] = None
) -> List[Task]:
    """Get tasks for a specific user with pagination and optional filtering"""
    statement = select(Task).where(Task.user_id == user_id)
    
    # Apply completion status filter if specified
    if completed is not None:
        statement = statement.where(Task.completed == completed)
    
    # Apply pagination
    statement = statement.offset(skip).limit(limit)
    
    return session.exec(statement).all()


def create_task_for_user(session: Session, user_id: str, task: TaskCreate) -> Task:
    """Create a new task for a specific user"""
    db_task = Task(user_id=user_id, **task.dict())
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task


def get_task_by_id_and_user_id(session: Session, task_id: int, user_id: str) -> Task:
    """Get a specific task by ID for a specific user"""
    statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
    db_task = session.exec(statement).first()
    
    if not db_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    
    return db_task


def update_task_by_id_and_user_id(
    session: Session, 
    task_id: int, 
    user_id: str, 
    task_update: TaskUpdate
) -> Task:
    """Update a specific task by ID for a specific user"""
    db_task = get_task_by_id_and_user_id(session, task_id, user_id)
    
    update_data = task_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_task, field, value)
    
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task


def delete_task_by_id_and_user_id(session: Session, task_id: int, user_id: str) -> bool:
    """Delete a specific task by ID for a specific user"""
    db_task = get_task_by_id_and_user_id(session, task_id, user_id)
    
    session.delete(db_task)
    session.commit()
    return True


def toggle_task_completion(session: Session, task_id: int, user_id: str) -> Task:
    """Toggle the completion status of a specific task for a specific user"""
    db_task = get_task_by_id_and_user_id(session, task_id, user_id)
    
    db_task.completed = not db_task.completed
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task
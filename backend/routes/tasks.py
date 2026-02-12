from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Optional
from sqlmodel import Session
from database.database import get_session
from auth.jwt import get_current_user
from models.task import Task, TaskCreate, TaskUpdate
from services.task_service import (
    get_tasks_by_user_id,
    create_task_for_user,
    get_task_by_id_and_user_id,
    update_task_by_id_and_user_id,
    delete_task_by_id_and_user_id,
    toggle_task_completion
)

router = APIRouter()


@router.get("/tasks", response_model=List[Task])
def get_tasks(
    user_id: str,
    current_user_id: str = Depends(get_current_user),
    session: Session = Depends(get_session),
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=100, description="Maximum number of records to return"),
    completed: Optional[bool] = Query(None, description="Filter by completion status")
):
    """
    Get tasks for the current user with pagination and optional filtering
    """
    # Verify that the requested user_id matches the authenticated user_id
    if user_id != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access these tasks"
        )

    tasks = get_tasks_by_user_id(session, user_id, skip=skip, limit=limit, completed=completed)
    return tasks


@router.post("/tasks", response_model=Task)
def create_task(
    user_id: str,
    task: TaskCreate,
    current_user_id: str = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Create a new task for the current user
    """
    # Verify that the requested user_id matches the authenticated user_id
    if user_id != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to create tasks for this user"
        )
    
    db_task = create_task_for_user(session, user_id, task)
    return db_task


@router.get("/tasks/{id}", response_model=Task)
def get_task(
    user_id: str,
    id: int,
    current_user_id: str = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Get a specific task by ID
    """
    # Verify that the requested user_id matches the authenticated user_id
    if user_id != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this task"
        )
    
    db_task = get_task_by_id_and_user_id(session, id, user_id)
    return db_task


@router.put("/tasks/{id}", response_model=Task)
def update_task(
    user_id: str,
    id: int,
    task_update: TaskUpdate,
    current_user_id: str = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Update a specific task by ID
    """
    # Verify that the requested user_id matches the authenticated user_id
    if user_id != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this task"
        )
    
    db_task = update_task_by_id_and_user_id(session, id, user_id, task_update)
    return db_task


@router.delete("/tasks/{id}")
def delete_task(
    user_id: str,
    id: int,
    current_user_id: str = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Delete a specific task by ID
    """
    # Verify that the requested user_id matches the authenticated user_id
    if user_id != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this task"
        )
    
    success = delete_task_by_id_and_user_id(session, id, user_id)
    if success:
        return {"message": "Task deleted successfully"}
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )


@router.patch("/tasks/{id}/complete")
def toggle_task_complete(
    user_id: str,
    id: int,
    current_user_id: str = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Toggle the completion status of a specific task
    """
    # Verify that the requested user_id matches the authenticated user_id
    if user_id != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this task"
        )
    
    db_task = toggle_task_completion(session, id, user_id)
    return {"completed": db_task.completed}
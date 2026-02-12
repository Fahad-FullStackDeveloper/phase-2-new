"""
Security tests for data isolation
Tests that users can only access their own data
"""

import pytest
from fastapi.testclient import TestClient
from sqlmodel import create_engine, Session, SQLModel
from unittest.mock import Mock

from main import app
from database.database import get_session
from models.task import Task


# Create a test database engine
test_engine = create_engine("sqlite:///./test_security_isolation.db", echo=True)


@pytest.fixture(scope="module")
def test_client():
    # Override the database session dependency
    def get_test_session():
        with Session(test_engine) as session:
            yield session

    app.dependency_overrides[get_session] = get_test_session
    
    with TestClient(app) as client:
        yield client


@pytest.fixture(autouse=True)
def setup_and_teardown():
    # Create tables before each test
    SQLModel.metadata.create_all(test_engine)
    yield
    # Optionally clean up after each test


def test_user_data_isolation_get_tasks(test_client):
    """
    Security test for user data isolation in get tasks endpoint
    Verifies that users can only access their own tasks
    """
    # Create tasks for user 1
    user1_id = "user-1-id"
    user1_tasks = [
        {"title": "User 1 Task 1", "description": "Task for user 1", "completed": False},
        {"title": "User 1 Task 2", "description": "Another task for user 1", "completed": True}
    ]
    
    for task_data in user1_tasks:
        response = test_client.post(f"/{user1_id}/tasks", json=task_data)
        assert response.status_code in [200, 201], \
            f"Creating task for user 1 failed: {response.text}"
    
    # Create tasks for user 2
    user2_id = "user-2-id"
    user2_tasks = [
        {"title": "User 2 Task 1", "description": "Task for user 2", "completed": False},
        {"title": "User 2 Task 2", "description": "Another task for user 2", "completed": True},
        {"title": "User 2 Task 3", "description": "Third task for user 2", "completed": False}
    ]
    
    for task_data in user2_tasks:
        response = test_client.post(f"/{user2_id}/tasks", json=task_data)
        assert response.status_code in [200, 201], \
            f"Creating task for user 2 failed: {response.text}"
    
    # Get tasks for user 1 - should only see user 1's tasks
    user1_tasks_response = test_client.get(f"/{user1_id}/tasks")
    assert user1_tasks_response.status_code == 200
    user1_tasks_list = user1_tasks_response.json()
    
    assert len(user1_tasks_list) == len(user1_tasks), \
        f"User 1 should see {len(user1_tasks)} tasks, saw {len(user1_tasks_list)}"
    
    user1_returned_titles = {task["title"] for task in user1_tasks_list}
    user1_original_titles = {task["title"] for task in user1_tasks}
    assert user1_returned_titles == user1_original_titles, \
        "User 1 should only see their own tasks"
    
    # Get tasks for user 2 - should only see user 2's tasks
    user2_tasks_response = test_client.get(f"/{user2_id}/tasks")
    assert user2_tasks_response.status_code == 200
    user2_tasks_list = user2_tasks_response.json()
    
    assert len(user2_tasks_list) == len(user2_tasks), \
        f"User 2 should see {len(user2_tasks)} tasks, saw {len(user2_tasks_list)}"
    
    user2_returned_titles = {task["title"] for task in user2_tasks_list}
    user2_original_titles = {task["title"] for task in user2_tasks}
    assert user2_returned_titles == user2_original_titles, \
        "User 2 should only see their own tasks"
    
    # Verify no cross-contamination
    assert len(user1_returned_titles.intersection(user2_returned_titles)) == 0, \
        "Users should not see each other's tasks"


def test_user_data_isolation_access_specific_task(test_client):
    """
    Security test for user data isolation when accessing specific tasks
    Verifies that users cannot access tasks belonging to other users
    """
    # Create a task for user 1
    user1_id = "iso-user-1-id"
    user2_id = "iso-user-2-id"
    
    user1_task_data = {
        "title": "Private Task for User 1",
        "description": "This should only be accessible by user 1",
        "completed": False
    }
    
    create_response = test_client.post(f"/{user1_id}/tasks", json=user1_task_data)
    assert create_response.status_code in [200, 201], \
        f"Creating task for user 1 failed: {create_response.text}"
    
    user1_task = create_response.json()
    assert "id" in user1_task
    task_id = user1_task["id"]
    
    # Try to access user 1's task as user 2 (should fail)
    access_response = test_client.get(f"/{user2_id}/tasks/{task_id}")
    assert access_response.status_code == 403, \
        f"User 2 should not be able to access user 1's task, got status {access_response.status_code}"
    
    # Verify user 1 can still access their own task
    own_access_response = test_client.get(f"/{user1_id}/tasks/{task_id}")
    assert own_access_response.status_code == 200, \
        f"User 1 should be able to access their own task, got status {own_access_response.status_code}"


def test_user_data_isolation_modify_task(test_client):
    """
    Security test for user data isolation when modifying tasks
    Verifies that users cannot modify tasks belonging to other users
    """
    # Create a task for user 1
    user1_id = "mod-user-1-id"
    user2_id = "mod-user-2-id"
    
    user1_task_data = {
        "title": "Modifiable Task for User 1",
        "description": "This should only be modifiable by user 1",
        "completed": False
    }
    
    create_response = test_client.post(f"/{user1_id}/tasks", json=user1_task_data)
    assert create_response.status_code in [200, 201], \
        f"Creating task for user 1 failed: {create_response.text}"
    
    user1_task = create_response.json()
    assert "id" in user1_task
    task_id = user1_task["id"]
    
    # Try to update user 1's task as user 2 (should fail)
    update_data = {
        "title": "Hacked Task Title",
        "description": "Attempt to modify someone else's task",
        "completed": True
    }
    
    update_response = test_client.put(f"/{user2_id}/tasks/{task_id}", json=update_data)
    assert update_response.status_code == 403, \
        f"User 2 should not be able to modify user 1's task, got status {update_response.status_code}"
    
    # Verify the task was not modified by checking with user 1
    get_response = test_client.get(f"/{user1_id}/tasks/{task_id}")
    assert get_response.status_code == 200
    retrieved_task = get_response.json()
    assert retrieved_task["title"] == user1_task_data["title"], \
        "Task should not have been modified by unauthorized user"
    assert retrieved_task["description"] == user1_task_data["description"], \
        "Task should not have been modified by unauthorized user"
    assert retrieved_task["completed"] == user1_task_data["completed"], \
        "Task should not have been modified by unauthorized user"


def test_user_data_isolation_delete_task(test_client):
    """
    Security test for user data isolation when deleting tasks
    Verifies that users cannot delete tasks belonging to other users
    """
    # Create a task for user 1
    user1_id = "del-user-1-id"
    user2_id = "del-user-2-id"
    
    user1_task_data = {
        "title": "Deletable Task for User 1",
        "description": "This should only be deletable by user 1",
        "completed": False
    }
    
    create_response = test_client.post(f"/{user1_id}/tasks", json=user1_task_data)
    assert create_response.status_code in [200, 201], \
        f"Creating task for user 1 failed: {create_response.text}"
    
    user1_task = create_response.json()
    assert "id" in user1_task
    task_id = user1_task["id"]
    
    # Try to delete user 1's task as user 2 (should fail)
    delete_response = test_client.delete(f"/{user2_id}/tasks/{task_id}")
    assert delete_response.status_code == 403, \
        f"User 2 should not be able to delete user 1's task, got status {delete_response.status_code}"
    
    # Verify the task still exists by checking with user 1
    get_response = test_client.get(f"/{user1_id}/tasks/{task_id}")
    assert get_response.status_code == 200, \
        "Task should still exist after unauthorized deletion attempt"
    
    # Now delete the task as the rightful owner
    owner_delete_response = test_client.delete(f"/{user1_id}/tasks/{task_id}")
    assert owner_delete_response.status_code in [200, 204], \
        f"Owner should be able to delete their own task, got status {owner_delete_response.status_code}"
    
    # Verify the task is now gone
    get_after_delete_response = test_client.get(f"/{user1_id}/tasks/{task_id}")
    assert get_after_delete_response.status_code == 404, \
        "Task should be gone after owner deletion"


def test_cross_user_access_prevention_in_toggle_operation(test_client):
    """
    Security test for preventing cross-user access in toggle completion operation
    Verifies that users cannot toggle completion status of tasks belonging to other users
    """
    # Create a task for user 1
    user1_id = "toggle-user-1-id"
    user2_id = "toggle-user-2-id"
    
    user1_task_data = {
        "title": "Toggle Task for User 1",
        "description": "This should only be toggleable by user 1",
        "completed": False
    }
    
    create_response = test_client.post(f"/{user1_id}/tasks", json=user1_task_data)
    assert create_response.status_code in [200, 201], \
        f"Creating task for user 1 failed: {create_response.text}"
    
    user1_task = create_response.json()
    assert "id" in user1_task
    task_id = user1_task["id"]
    
    # Try to toggle user 1's task completion as user 2 (should fail)
    toggle_response = test_client.patch(f"/{user2_id}/tasks/{task_id}/complete")
    assert toggle_response.status_code == 403, \
        f"User 2 should not be able to toggle user 1's task completion, got status {toggle_response.status_code}"
    
    # Verify the task completion status was not changed by checking with user 1
    get_response = test_client.get(f"/{user1_id}/tasks/{task_id}")
    assert get_response.status_code == 200
    retrieved_task = get_response.json()
    assert retrieved_task["completed"] == user1_task_data["completed"], \
        "Task completion status should not have been changed by unauthorized user"


if __name__ == "__main__":
    pytest.main([__file__])
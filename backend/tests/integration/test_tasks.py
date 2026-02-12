"""
Integration tests for task operations
Tests complete workflows for task-related functionality
"""

import pytest
from fastapi.testclient import TestClient
from sqlmodel import create_engine, Session, SQLModel
from unittest.mock import Mock

from main import app
from database.database import get_session
from models.task import Task


# Create a test database engine
test_engine = create_engine("sqlite:///./test_integration_tasks.db", echo=True)


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


def test_task_crud_operations_journey(test_client):
    """
    Integration test for complete task CRUD operations
    Tests create, read, update, and delete workflows
    """
    # Mock user ID (in real scenario, this would come from authentication)
    user_id = "test-user-id"
    
    # Step 1: Create a task
    task_data = {
        "title": "Integration Test Task",
        "description": "Description for integration test task",
        "completed": False
    }
    
    create_response = test_client.post(f"/{user_id}/tasks", json=task_data)
    assert create_response.status_code in [200, 201], \
        f"Task creation failed with status {create_response.status_code}: {create_response.text}"
    
    created_task = create_response.json()
    assert "id" in created_task
    assert created_task["title"] == task_data["title"]
    assert created_task["user_id"] == user_id
    task_id = created_task["id"]
    
    # Step 2: Retrieve the task
    get_response = test_client.get(f"/{user_id}/tasks/{task_id}")
    assert get_response.status_code == 200, \
        f"Task retrieval failed with status {get_response.status_code}: {get_response.text}"
    
    retrieved_task = get_response.json()
    assert retrieved_task["id"] == task_id
    assert retrieved_task["title"] == task_data["title"]
    assert retrieved_task["user_id"] == user_id
    
    # Step 3: Update the task
    update_data = {
        "title": "Updated Integration Test Task",
        "description": "Updated description for integration test task",
        "completed": True
    }
    
    update_response = test_client.put(f"/{user_id}/tasks/{task_id}", json=update_data)
    assert update_response.status_code == 200, \
        f"Task update failed with status {update_response.status_code}: {update_response.text}"
    
    updated_task = update_response.json()
    assert updated_task["id"] == task_id
    assert updated_task["title"] == update_data["title"]
    assert updated_task["completed"] == update_data["completed"]
    
    # Step 4: Verify the update persisted
    verify_response = test_client.get(f"/{user_id}/tasks/{task_id}")
    assert verify_response.status_code == 200
    verified_task = verify_response.json()
    assert verified_task["title"] == update_data["title"]
    assert verified_task["completed"] == update_data["completed"]
    
    # Step 5: Delete the task
    delete_response = test_client.delete(f"/{user_id}/tasks/{task_id}")
    assert delete_response.status_code in [200, 204], \
        f"Task deletion failed with status {delete_response.status_code}: {delete_response.text}"
    
    # Step 6: Verify the task is gone
    get_deleted_response = test_client.get(f"/{user_id}/tasks/{task_id}")
    assert get_deleted_response.status_code == 404, \
        "Deleted task should no longer be accessible"


def test_task_list_with_multiple_tasks(test_client):
    """
    Integration test for listing tasks with multiple tasks
    Tests the workflow of creating multiple tasks and listing them
    """
    user_id = "test-list-user-id"
    
    # Create multiple tasks
    tasks_to_create = [
        {"title": "Task 1", "description": "First test task", "completed": False},
        {"title": "Task 2", "description": "Second test task", "completed": True},
        {"title": "Task 3", "description": "Third test task", "completed": False}
    ]
    
    created_tasks = []
    for task_data in tasks_to_create:
        response = test_client.post(f"/{user_id}/tasks", json=task_data)
        assert response.status_code in [200, 201], \
            f"Task creation failed with status {response.status_code}: {response.text}"
        
        created_task = response.json()
        assert "id" in created_task
        created_tasks.append(created_task)
    
    # Retrieve the list of tasks
    list_response = test_client.get(f"/{user_id}/tasks")
    assert list_response.status_code == 200, \
        f"Task listing failed with status {list_response.status_code}: {list_response.text}"
    
    tasks_list = list_response.json()
    assert isinstance(tasks_list, list), "Response should be a list"
    assert len(tasks_list) == len(created_tasks), \
        f"Expected {len(created_tasks)} tasks, got {len(tasks_list)}"
    
    # Verify all created tasks are in the list
    created_task_ids = {task["id"] for task in created_tasks}
    returned_task_ids = {task["id"] for task in tasks_list}
    assert created_task_ids == returned_task_ids, \
        "All created tasks should be in the returned list"


def test_task_completion_toggle_workflow(test_client):
    """
    Integration test for task completion toggle workflow
    Tests the complete workflow of toggling task completion status
    """
    user_id = "test-completion-user-id"
    
    # Create a task that is initially not completed
    task_data = {
        "title": "Completion Toggle Test Task",
        "description": "Task to test completion toggling",
        "completed": False
    }
    
    create_response = test_client.post(f"/{user_id}/tasks", json=task_data)
    assert create_response.status_code in [200, 201], \
        f"Task creation failed with status {create_response.status_code}: {create_response.text}"
    
    created_task = create_response.json()
    assert "id" in created_task
    task_id = created_task["id"]
    assert created_task["completed"] is False
    
    # Toggle the task completion status to True
    toggle_response = test_client.patch(f"/{user_id}/tasks/{task_id}/complete")
    assert toggle_response.status_code == 200, \
        f"Task completion toggle failed with status {toggle_response.status_code}: {toggle_response.text}"
    
    toggle_result = toggle_response.json()
    assert "completed" in toggle_result
    assert toggle_result["completed"] is True
    
    # Verify the change persisted by retrieving the task
    get_response = test_client.get(f"/{user_id}/tasks/{task_id}")
    assert get_response.status_code == 200
    retrieved_task = get_response.json()
    assert retrieved_task["completed"] is True
    
    # Toggle the task completion status back to False
    toggle_response_2 = test_client.patch(f"/{user_id}/tasks/{task_id}/complete")
    assert toggle_response_2.status_code == 200, \
        f"Task completion toggle failed with status {toggle_response_2.status_code}: {toggle_response_2.text}"
    
    toggle_result_2 = toggle_response_2.json()
    assert "completed" in toggle_result_2
    assert toggle_result_2["completed"] is False
    
    # Verify the change persisted
    get_response_2 = test_client.get(f"/{user_id}/tasks/{task_id}")
    assert get_response_2.status_code == 200
    retrieved_task_2 = get_response_2.json()
    assert retrieved_task_2["completed"] is False


def test_task_creation_with_validation_errors(test_client):
    """
    Integration test for task creation with validation errors
    Tests that appropriate errors are returned for invalid inputs
    """
    user_id = "test-validation-user-id"
    
    # Test with empty title (should fail validation)
    invalid_task_data = {
        "title": "",  # Empty title should fail validation
        "description": "Task with empty title",
        "completed": False
    }
    
    response = test_client.post(f"/{user_id}/tasks", json=invalid_task_data)
    # Should return a validation error (422) or similar
    assert response.status_code in [422, 400], \
        f"Expected validation error (422 or 400), got {response.status_code}: {response.text}"
    
    # Test with very long title (should fail validation if length is limited)
    long_title = "A" * 1000  # Assuming there's a length limit
    invalid_task_data_long = {
        "title": long_title,
        "description": "Task with very long title",
        "completed": False
    }
    
    response_long = test_client.post(f"/{user_id}/tasks", json=invalid_task_data_long)
    assert response_long.status_code in [422, 400], \
        f"Expected validation error for long title, got {response_long.status_code}: {response_long.text}"


if __name__ == "__main__":
    pytest.main([__file__])
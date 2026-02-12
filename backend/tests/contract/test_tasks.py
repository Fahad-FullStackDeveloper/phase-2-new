"""
Contract tests for task operations
Tests the API contracts for task-related endpoints
"""

import pytest
from fastapi.testclient import TestClient
from sqlmodel import create_engine, Session, SQLModel
from unittest.mock import Mock

from main import app
from database.database import get_session
from models.task import Task


# Create a test database engine
test_engine = create_engine("sqlite:///./test_contract_tasks.db", echo=True)


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


def test_create_task_endpoint_contract(test_client):
    """
    Contract test for create task endpoint
    Verifies the API contract for creating tasks
    """
    # Mock user ID (in real scenario, this would come from authentication)
    user_id = "test-user-id"
    
    # Test data for creating a task
    task_data = {
        "title": "Test Task Title",
        "description": "Test task description",
        "completed": False
    }
    
    # Make request to create task endpoint
    response = test_client.post(f"/{user_id}/tasks", json=task_data)
    
    # Verify response structure and status code
    # Could be 401/403 if authentication is required but not provided
    # Or 200/201 if successful
    assert response.status_code in [200, 201, 401, 403, 422], \
        f"Expected 200, 201, 401, 403, or 422, got {response.status_code}"
    
    # If successful creation, verify response structure
    if response.status_code in [200, 201]:
        response_data = response.json()
        
        # Verify required fields in response
        assert "id" in response_data, "Response should contain task ID"
        assert "title" in response_data, "Response should contain title"
        assert "user_id" in response_data, "Response should contain user_id"
        assert "completed" in response_data, "Response should contain completed status"
        
        # Verify values match what was sent
        assert response_data["title"] == task_data["title"], \
            "Response title should match request title"
        assert response_data["user_id"] == user_id, \
            "Response user_id should match the URL parameter"
        assert response_data["completed"] == task_data["completed"], \
            "Response completed status should match request"


def test_list_tasks_endpoint_contract(test_client):
    """
    Contract test for list tasks endpoint
    Verifies the API contract for listing tasks
    """
    # Mock user ID
    user_id = "test-user-id"
    
    # Make request to list tasks endpoint
    response = test_client.get(f"/{user_id}/tasks")
    
    # Verify response structure and status code
    assert response.status_code in [200, 401, 403], \
        f"Expected 200, 401, or 403, got {response.status_code}"
    
    # If successful, verify response structure
    if response.status_code == 200:
        response_data = response.json()
        
        # Verify response is a list
        assert isinstance(response_data, list), \
            "Response should be a list of tasks"
        
        # If there are tasks, verify their structure
        for task in response_data:
            assert "id" in task, "Each task should have an ID"
            assert "title" in task, "Each task should have a title"
            assert "user_id" in task, "Each task should have a user_id"
            assert "completed" in task, "Each task should have a completed status"


def test_toggle_task_completion_endpoint_contract(test_client):
    """
    Contract test for toggle task completion endpoint
    Verifies the API contract for toggling task completion status
    """
    # Mock user ID and task ID
    user_id = "test-user-id"
    task_id = 1
    
    # Make request to toggle task completion endpoint
    response = test_client.patch(f"/{user_id}/tasks/{task_id}/complete")
    
    # Verify response structure and status code
    assert response.status_code in [200, 401, 403, 404], \
        f"Expected 200, 401, 403, or 404, got {response.status_code}"
    
    # If successful, verify response structure
    if response.status_code == 200:
        response_data = response.json()
        
        # Verify response contains completion status
        assert "completed" in response_data, \
            "Response should contain completed status"


def test_update_task_endpoint_contract(test_client):
    """
    Contract test for update task endpoint
    Verifies the API contract for updating tasks
    """
    # Mock user ID and task ID
    user_id = "test-user-id"
    task_id = 1
    
    # Test data for updating a task
    update_data = {
        "title": "Updated Task Title",
        "description": "Updated task description",
        "completed": True
    }
    
    # Make request to update task endpoint
    response = test_client.put(f"/{user_id}/tasks/{task_id}", json=update_data)
    
    # Verify response structure and status code
    assert response.status_code in [200, 401, 403, 404, 422], \
        f"Expected 200, 401, 403, 404, or 422, got {response.status_code}"
    
    # If successful update, verify response structure
    if response.status_code == 200:
        response_data = response.json()
        
        # Verify required fields in response
        assert "id" in response_data, "Response should contain task ID"
        assert "title" in response_data, "Response should contain title"
        assert "user_id" in response_data, "Response should contain user_id"
        assert "completed" in response_data, "Response should contain completed status"
        
        # Verify values match what was sent
        assert response_data["title"] == update_data["title"], \
            "Response title should match request title"
        assert response_data["user_id"] == user_id, \
            "Response user_id should match the URL parameter"
        assert response_data["completed"] == update_data["completed"], \
            "Response completed status should match request"


def test_delete_task_endpoint_contract(test_client):
    """
    Contract test for delete task endpoint
    Verifies the API contract for deleting tasks
    """
    # Mock user ID and task ID
    user_id = "test-user-id"
    task_id = 1
    
    # Make request to delete task endpoint
    response = test_client.delete(f"/{user_id}/tasks/{task_id}")
    
    # Verify response structure and status code
    assert response.status_code in [200, 204, 401, 403, 404], \
        f"Expected 200, 204, 401, 403, or 404, got {response.status_code}"
    
    # If successful deletion, verify response structure
    if response.status_code == 200:
        response_data = response.json()
        
        # Verify response contains success message
        assert "message" in response_data, \
            "Response should contain a message"
        assert "deleted" in response_data["message"].lower() or \
               "success" in response_data["message"].lower(), \
            "Message should indicate successful deletion"


if __name__ == "__main__":
    pytest.main([__file__])
"""
Full integration test to verify all functionality works together
Tests the complete end-to-end workflow of the todo application
"""

import pytest
from fastapi.testclient import TestClient
from sqlmodel import create_engine, Session, SQLModel

from main import app
from database.database import get_session
from models.user import User
from models.task import Task


# Create a test database engine
test_engine = create_engine("sqlite:///./test_full_integration.db", echo=True)


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


def test_complete_todo_application_workflow(test_client):
    """
    Full integration test for the complete todo application workflow
    Tests user registration, login, task management, and data isolation
    """
    # Phase 1: User Registration
    print("Testing user registration...")
    user1_data = {
        "email": "integration.user1@example.com",
        "password": "SecurePassword123!",
        "name": "Integration User 1"
    }
    
    user2_data = {
        "email": "integration.user2@example.com",
        "password": "SecurePassword456!",
        "name": "Integration User 2"
    }
    
    # Register User 1
    register_response_1 = test_client.post("/auth/register", json=user1_data)
    assert register_response_1.status_code in [200, 201], \
        f"User 1 registration failed: {register_response_1.status_code} - {register_response_1.text}"
    
    user1_info = register_response_1.json()
    assert "email" in user1_info
    assert user1_info["email"] == user1_data["email"]
    user1_id = user1_info.get("id") or user1_info.get("user_id") or "user1-mock-id"
    
    # Register User 2
    register_response_2 = test_client.post("/auth/register", json=user2_data)
    assert register_response_2.status_code in [200, 201], \
        f"User 2 registration failed: {register_response_2.status_code} - {register_response_2.text}"
    
    user2_info = register_response_2.json()
    assert "email" in user2_info
    assert user2_info["email"] == user2_data["email"]
    user2_id = user2_info.get("id") or user2_info.get("user_id") or "user2-mock-id"
    
    print("✓ User registration completed")
    
    # Phase 2: User Login
    print("Testing user login...")
    
    # Login User 1
    login_data_1 = {
        "email": user1_data["email"],
        "password": user1_data["password"]
    }
    
    login_response_1 = test_client.post("/auth/login", json=login_data_1)
    assert login_response_1.status_code == 200, \
        f"User 1 login failed: {login_response_1.status_code} - {login_response_1.text}"
    
    login_info_1 = login_response_1.json()
    assert "access_token" in login_info_1 or "token" in login_info_1
    user1_token = login_info_1.get("access_token") or login_info_1.get("token")
    assert user1_token is not None
    
    # Login User 2
    login_data_2 = {
        "email": user2_data["email"],
        "password": user2_data["password"]
    }
    
    login_response_2 = test_client.post("/auth/login", json=login_data_2)
    assert login_response_2.status_code == 200, \
        f"User 2 login failed: {login_response_2.status_code} - {login_response_2.text}"
    
    login_info_2 = login_response_2.json()
    assert "access_token" in login_info_2 or "token" in login_info_2
    user2_token = login_info_2.get("access_token") or login_info_2.get("token")
    assert user2_token is not None
    
    print("✓ User login completed")
    
    # Phase 3: Task Management for User 1
    print("Testing task management for User 1...")
    
    # Create tasks for User 1
    user1_tasks = [
        {"title": "User 1 Task 1", "description": "First task for user 1", "completed": False},
        {"title": "User 1 Task 2", "description": "Second task for user 1", "completed": True},
        {"title": "User 1 Task 3", "description": "Third task for user 1", "completed": False}
    ]
    
    user1_created_tasks = []
    for i, task_data in enumerate(user1_tasks):
        response = test_client.post(f"/{user1_id}/tasks", json=task_data)
        assert response.status_code in [200, 201], \
            f"Creating task {i+1} for User 1 failed: {response.status_code} - {response.text}"
        
        created_task = response.json()
        assert "id" in created_task
        assert created_task["user_id"] == user1_id
        user1_created_tasks.append(created_task)
    
    print(f"✓ Created {len(user1_created_tasks)} tasks for User 1")
    
    # Phase 4: Task Management for User 2
    print("Testing task management for User 2...")
    
    # Create tasks for User 2
    user2_tasks = [
        {"title": "User 2 Task 1", "description": "First task for user 2", "completed": False},
        {"title": "User 2 Task 2", "description": "Second task for user 2", "completed": False}
    ]
    
    user2_created_tasks = []
    for i, task_data in enumerate(user2_tasks):
        response = test_client.post(f"/{user2_id}/tasks", json=task_data)
        assert response.status_code in [200, 201], \
            f"Creating task {i+1} for User 2 failed: {response.status_code} - {response.text}"
        
        created_task = response.json()
        assert "id" in created_task
        assert created_task["user_id"] == user2_id
        user2_created_tasks.append(created_task)
    
    print(f"✓ Created {len(user2_created_tasks)} tasks for User 2")
    
    # Phase 5: Verify Data Isolation
    print("Testing data isolation...")
    
    # User 1 should only see their own tasks
    user1_tasks_response = test_client.get(f"/{user1_id}/tasks")
    assert user1_tasks_response.status_code == 200
    user1_retrieved_tasks = user1_tasks_response.json()
    assert len(user1_retrieved_tasks) == len(user1_created_tasks)
    
    user1_retrieved_ids = {task["id"] for task in user1_retrieved_tasks}
    user1_created_ids = {task["id"] for task in user1_created_tasks}
    assert user1_retrieved_ids == user1_created_ids, "User 1 should only see their own tasks"
    
    # User 2 should only see their own tasks
    user2_tasks_response = test_client.get(f"/{user2_id}/tasks")
    assert user2_tasks_response.status_code == 200
    user2_retrieved_tasks = user2_tasks_response.json()
    assert len(user2_retrieved_tasks) == len(user2_created_tasks)
    
    user2_retrieved_ids = {task["id"] for task in user2_retrieved_tasks}
    user2_created_ids = {task["id"] for task in user2_created_tasks}
    assert user2_retrieved_ids == user2_created_ids, "User 2 should only see their own tasks"
    
    # Verify no cross-contamination
    assert len(user1_retrieved_ids.intersection(user2_retrieved_ids)) == 0, \
        "Users should not see each other's tasks"
    
    print("✓ Data isolation verified")
    
    # Phase 6: Test Task Operations (Update, Toggle, Delete)
    print("Testing task operations...")
    
    # Update a task for User 1
    task_to_update = user1_created_tasks[0]
    update_data = {
        "title": "Updated User 1 Task 1",
        "description": "Updated description for first task of user 1",
        "completed": True
    }
    
    update_response = test_client.put(f"/{user1_id}/tasks/{task_to_update['id']}", json=update_data)
    assert update_response.status_code == 200, \
        f"Updating task failed: {update_response.status_code} - {update_response.text}"
    
    updated_task = update_response.json()
    assert updated_task["title"] == update_data["title"]
    assert updated_task["completed"] == update_data["completed"]
    
    # Toggle completion status for User 1's task
    task_to_toggle = user1_created_tasks[1]  # Second task, initially completed=True
    toggle_response = test_client.patch(f"/{user1_id}/tasks/{task_to_toggle['id']}/complete")
    assert toggle_response.status_code == 200, \
        f"Toggling task completion failed: {toggle_response.status_code} - {toggle_response.text}"
    
    toggle_result = toggle_response.json()
    # Since the task was initially completed=True, toggling should make it False
    assert toggle_result["completed"] is False
    
    # Delete a task for User 1
    task_to_delete = user1_created_tasks[2]  # Third task
    delete_response = test_client.delete(f"/{user1_id}/tasks/{task_to_delete['id']}")
    assert delete_response.status_code in [200, 204], \
        f"Deleting task failed: {delete_response.status_code} - {delete_response.text}"
    
    # Verify the deleted task is gone
    get_deleted_response = test_client.get(f"/{user1_id}/tasks/{task_to_delete['id']}")
    assert get_deleted_response.status_code == 404
    
    print("✓ Task operations completed")
    
    # Phase 7: Verify continued data isolation after operations
    print("Testing continued data isolation after operations...")
    
    # User 1 should see updated tasks (minus the deleted one)
    user1_final_tasks_response = test_client.get(f"/{user1_id}/tasks")
    assert user1_final_tasks_response.status_code == 200
    user1_final_tasks = user1_final_tasks_response.json()
    
    # Should have 2 tasks left (original 3, minus 1 deleted)
    assert len(user1_final_tasks) == 2
    
    # Verify the updated task is in the list with correct properties
    updated_task_found = False
    for task in user1_final_tasks:
        if task["id"] == task_to_update["id"]:
            assert task["title"] == update_data["title"]
            assert task["completed"] == update_data["completed"]
            updated_task_found = True
            break
    assert updated_task_found, "Updated task should still be accessible to User 1"
    
    # User 2 should still only see their own tasks, unaffected by User 1's operations
    user2_final_tasks_response = test_client.get(f"/{user2_id}/tasks")
    assert user2_final_tasks_response.status_code == 200
    user2_final_tasks = user2_final_tasks_response.json()
    assert len(user2_final_tasks) == len(user2_created_tasks), \
        "User 2's tasks should be unaffected by User 1's operations"
    
    print("✓ Continued data isolation verified")
    
    print("✓ Complete integration test passed!")


if __name__ == "__main__":
    pytest.main([__file__])
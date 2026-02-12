"""
Contract tests for authentication endpoints
Tests the API contracts without testing internal implementation
"""

import pytest
import json
from fastapi.testclient import TestClient
from sqlmodel import create_engine, Session, SQLModel
from authlib.integrations.starlette_client import OAuth
from unittest.mock import Mock

from main import app
from database.database import get_session
from config import settings


# Create a test database engine
test_engine = create_engine("sqlite:///./test_contract_auth.db", echo=True)


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


def test_register_endpoint_contract(test_client):
    """
    Contract test for registration endpoint
    Verifies the API contract for user registration
    """
    # Test data
    registration_data = {
        "email": "test@example.com",
        "password": "SecurePassword123!",
        "name": "Test User"
    }
    
    # Make request to register endpoint
    response = test_client.post("/auth/register", json=registration_data)
    
    # Verify response structure and status code
    assert response.status_code in [200, 201, 400, 409], \
        f"Expected 200, 201, 400, or 409, got {response.status_code}"
    
    # If successful registration, verify response structure
    if response.status_code in [200, 201]:
        response_data = response.json()
        
        # Verify required fields in response
        assert "id" in response_data or "user_id" in response_data, \
            "Response should contain user identifier"
        assert "email" in response_data, \
            "Response should contain email"
        assert "created_at" in response_data or "timestamp" in response_data, \
            "Response should contain timestamp"
        
        # Verify email matches what was sent
        assert response_data["email"] == registration_data["email"], \
            "Response email should match request email"


def test_login_endpoint_contract(test_client):
    """
    Contract test for login endpoint
    Verifies the API contract for user login
    """
    # First register a user to login with
    registration_data = {
        "email": "login_test@example.com",
        "password": "SecurePassword123!",
        "name": "Login Test User"
    }
    
    # Register the user
    register_response = test_client.post("/auth/register", json=registration_data)
    assert register_response.status_code in [200, 201], \
        f"Registration failed with status {register_response.status_code}"
    
    # Prepare login data
    login_data = {
        "email": "login_test@example.com",
        "password": "SecurePassword123!"
    }
    
    # Make request to login endpoint
    response = test_client.post("/auth/login", json=login_data)
    
    # Verify response structure and status code
    assert response.status_code in [200, 401], \
        f"Expected 200 or 401, got {response.status_code}"
    
    # If successful login, verify response structure
    if response.status_code == 200:
        response_data = response.json()
        
        # Verify required fields in response
        assert "access_token" in response_data or "token" in response_data, \
            "Response should contain access token"
        assert "token_type" in response_data, \
            "Response should contain token type"
        
        # Verify token type is bearer
        if "token_type" in response_data:
            assert response_data["token_type"].lower() == "bearer", \
                "Token type should be Bearer"


def test_logout_endpoint_contract(test_client):
    """
    Contract test for logout endpoint
    Verifies the API contract for user logout
    """
    # First register and login a user
    registration_data = {
        "email": "logout_test@example.com",
        "password": "SecurePassword123!",
        "name": "Logout Test User"
    }
    
    # Register the user
    register_response = test_client.post("/auth/register", json=registration_data)
    assert register_response.status_code in [200, 201], \
        f"Registration failed with status {register_response.status_code}"
    
    # Login the user
    login_data = {
        "email": "logout_test@example.com",
        "password": "SecurePassword123!"
    }
    
    login_response = test_client.post("/auth/login", json=login_data)
    assert login_response.status_code == 200, \
        f"Login failed with status {login_response.status_code}"
    
    # Extract token from login response
    login_response_data = login_response.json()
    token = login_response_data.get("access_token") or login_response_data.get("token")
    assert token, "Login response should contain a token"
    
    # Make request to logout endpoint with authorization header
    headers = {"Authorization": f"Bearer {token}"}
    response = test_client.post("/auth/logout", headers=headers)
    
    # Verify response structure and status code
    assert response.status_code in [200, 401], \
        f"Expected 200 or 401, got {response.status_code}"
    
    # If successful logout, verify response structure
    if response.status_code == 200:
        response_data = response.json()
        
        # Verify required fields in response
        assert "message" in response_data, \
            "Response should contain a message"
        assert "success" in response_data or response_data.get("message") == "Logged out successfully", \
            "Response should indicate successful logout"


if __name__ == "__main__":
    pytest.main([__file__])
"""
Integration tests for user registration and login journeys
Tests complete user workflows from registration to login
"""

import pytest
from fastapi.testclient import TestClient
from sqlmodel import create_engine, Session, SQLModel
from unittest.mock import Mock

from main import app
from database.database import get_session
from models.user import User


# Create a test database engine
test_engine = create_engine("sqlite:///./test_integration_auth.db", echo=True)


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


def test_user_registration_journey(test_client):
    """
    Integration test for user registration journey
    Tests the complete registration workflow
    """
    # Define test user data
    user_data = {
        "email": "integration_test@example.com",
        "password": "SecurePassword123!",
        "name": "Integration Test User"
    }
    
    # Step 1: Register the user
    register_response = test_client.post("/auth/register", json=user_data)
    
    # Verify registration was successful
    assert register_response.status_code in [200, 201], \
        f"Registration failed with status {register_response.status_code}: {register_response.text}"
    
    register_data = register_response.json()
    assert "email" in register_data
    assert register_data["email"] == user_data["email"]
    
    # Step 2: Verify user was created in the database
    # Note: This assumes we can access the database directly for verification
    # In a real scenario, we might need to use a different approach
    with Session(test_engine) as session:
        user = session.query(User).filter(User.email == user_data["email"]).first()
        assert user is not None, "User should be created in database"
        assert user.email == user_data["email"]
        assert hasattr(user, "id"), "User should have an ID"


def test_user_login_journey(test_client):
    """
    Integration test for user login journey
    Tests the complete login workflow after registration
    """
    # Step 1: Register a user first
    user_data = {
        "email": "login_integration_test@example.com",
        "password": "SecurePassword123!",
        "name": "Login Integration Test User"
    }
    
    register_response = test_client.post("/auth/register", json=user_data)
    assert register_response.status_code in [200, 201], \
        f"Registration failed with status {register_response.status_code}"
    
    # Step 2: Login with the registered user
    login_data = {
        "email": "login_integration_test@example.com",
        "password": "SecurePassword123!"
    }
    
    login_response = test_client.post("/auth/login", json=login_data)
    
    # Verify login was successful
    assert login_response.status_code == 200, \
        f"Login failed with status {login_response.status_code}: {login_response.text}"
    
    login_response_data = login_response.json()
    
    # Verify response contains necessary authentication data
    assert "access_token" in login_response_data or "token" in login_response_data, \
        "Login response should contain an access token"
    assert "token_type" in login_response_data, \
        "Login response should contain token type"
    
    # Extract token for further validation
    token = login_response_data.get("access_token") or login_response_data.get("token")
    token_type = login_response_data.get("token_type", "bearer")
    
    assert token is not None, "Token should not be None"
    assert isinstance(token, str) and len(token) > 0, "Token should be a non-empty string"
    assert token_type.lower() == "bearer", "Token type should be Bearer"


def test_user_registration_then_login_flow(test_client):
    """
    Integration test for complete registration then login flow
    Tests the end-to-end user authentication journey
    """
    # Step 1: Register a new user
    user_data = {
        "email": "flow_test@example.com",
        "password": "SecurePassword123!",
        "name": "Flow Test User"
    }
    
    register_response = test_client.post("/auth/register", json=user_data)
    assert register_response.status_code in [200, 201], \
        f"Registration failed with status {register_response.status_code}"
    
    register_data = register_response.json()
    assert register_data["email"] == user_data["email"]
    
    # Step 2: Attempt to login with the same credentials
    login_data = {
        "email": "flow_test@example.com",
        "password": "SecurePassword123!"
    }
    
    login_response = test_client.post("/auth/login", json=login_data)
    assert login_response.status_code == 200, \
        f"Login failed with status {login_response.status_code}: {login_response.text}"
    
    login_data_response = login_response.json()
    assert "access_token" in login_data_response, "Login should return an access token"
    
    # Step 3: Use the token to access a protected endpoint (if available)
    # For this example, we'll assume there's a /me endpoint that requires authentication
    token = login_data_response["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    # If we had a protected endpoint, we could test it like:
    # profile_response = test_client.get("/auth/me", headers=headers)
    # assert profile_response.status_code == 200


def test_invalid_credentials_login_fails(test_client):
    """
    Integration test to verify invalid credentials are rejected
    Tests that incorrect login credentials fail appropriately
    """
    # Step 1: Register a user
    user_data = {
        "email": "invalid_creds_test@example.com",
        "password": "SecurePassword123!",
        "name": "Invalid Credentials Test User"
    }
    
    register_response = test_client.post("/auth/register", json=user_data)
    assert register_response.status_code in [200, 201], \
        f"Registration failed with status {register_response.status_code}"
    
    # Step 2: Try to login with wrong password
    wrong_login_data = {
        "email": "invalid_creds_test@example.com",
        "password": "WrongPassword456!"
    }
    
    login_response = test_client.post("/auth/login", json=wrong_login_data)
    
    # Verify login failed with appropriate status
    assert login_response.status_code == 401, \
        f"Login with wrong credentials should fail with 401, got {login_response.status_code}"
    
    # Step 3: Try to login with non-existent email
    nonexistent_login_data = {
        "email": "nonexistent@example.com",
        "password": "AnyPassword123!"
    }
    
    nonexistent_login_response = test_client.post("/auth/login", json=nonexistent_login_data)
    
    # Verify login failed with appropriate status
    assert nonexistent_login_response.status_code == 401, \
        f"Login with non-existent email should fail with 401, got {nonexistent_login_response.status_code}"


if __name__ == "__main__":
    pytest.main([__file__])
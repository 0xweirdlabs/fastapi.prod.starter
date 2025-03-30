"""
Tests for the Authentication API

This module contains integration tests for the authentication endpoints,
testing the login flow and token validation.
"""
import pytest
from fastapi import status
from sqlalchemy.orm import Session

from app.core.security import get_password_hash
from app.models.primary.user import User


@pytest.fixture
def test_user(db_session: Session):
    """Create a test user in the database"""
    user = User(
        email="test@example.com",
        hashed_password=get_password_hash("password123"),
        full_name="Test User",
        is_active=True,
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


def test_login_valid_credentials(client, test_user):
    """Test login endpoint with valid credentials"""
    # Arrange
    login_data = {
        "username": test_user.email,  # OAuth2 uses 'username' for the email
        "password": "password123",
    }
    
    # Act
    response = client.post("/api/v1/auth/login", data=login_data)
    
    # Assert
    assert response.status_code == status.HTTP_200_OK
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"


def test_login_invalid_password(client, test_user):
    """Test login endpoint with invalid password"""
    # Arrange
    login_data = {
        "username": test_user.email,
        "password": "wrong_password",
    }
    
    # Act
    response = client.post("/api/v1/auth/login", data=login_data)
    
    # Assert
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_login_nonexistent_user(client):
    """Test login endpoint with nonexistent user"""
    # Arrange
    login_data = {
        "username": "nonexistent@example.com",
        "password": "password123",
    }
    
    # Act
    response = client.post("/api/v1/auth/login", data=login_data)
    
    # Assert
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

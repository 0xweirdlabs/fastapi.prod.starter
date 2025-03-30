"""
Tests for the UserService

This module contains unit tests for the UserService class, which handles
user-related business logic including creation, authentication, and management.
"""
import pytest
from unittest.mock import MagicMock, patch

from app.services.user_service import UserService
from app.models.primary.user import User
from app.api.v1.schemas.user import UserCreate, UserUpdate


@pytest.fixture
def mock_user():
    """Create a mock user for testing"""
    return User(
        id=1,
        email="test@example.com",
        hashed_password="hashed_password",
        full_name="Test User",
        is_active=True,
        is_superuser=False,
    )


@pytest.fixture
def user_service(db_session):
    """Create a UserService instance with mocked dependencies"""
    return UserService(db_session)


@patch("app.repositories.user_repository.UserRepository.get_by_email")
def test_get_by_email_returns_user(mock_get_by_email, user_service, mock_user):
    """Test that get_by_email returns a user when found"""
    # Arrange
    mock_get_by_email.return_value = mock_user
    
    # Act
    result = user_service.get_by_email("test@example.com")
    
    # Assert
    assert result == mock_user
    mock_get_by_email.assert_called_once_with(email="test@example.com")


@patch("app.repositories.user_repository.UserRepository.get_by_email")
def test_get_by_email_returns_none_when_not_found(mock_get_by_email, user_service):
    """Test that get_by_email returns None when user not found"""
    # Arrange
    mock_get_by_email.return_value = None
    
    # Act
    result = user_service.get_by_email("nonexistent@example.com")
    
    # Assert
    assert result is None
    mock_get_by_email.assert_called_once_with(email="nonexistent@example.com")


@patch("app.core.security.get_password_hash")
@patch("app.repositories.user_repository.UserRepository.create")
def test_create_user_hashes_password(mock_create, mock_get_password_hash, user_service):
    """Test that create user correctly hashes the password"""
    # Arrange
    mock_get_password_hash.return_value = "hashed_password"
    user_create = UserCreate(
        email="new@example.com",
        password="password123",
        full_name="New User"
    )
    mock_create.return_value = User(
        id=2,
        email="new@example.com",
        hashed_password="hashed_password",
        full_name="New User"
    )
    
    # Act
    user_service.create(user_create)
    
    # Assert
    mock_get_password_hash.assert_called_once_with("password123")


@patch("app.core.security.verify_password")
@patch("app.repositories.user_repository.UserRepository.get_by_email")
def test_authenticate_returns_user_when_valid(
    mock_get_by_email, mock_verify_password, user_service, mock_user
):
    """Test that authenticate returns a user when credentials are valid"""
    # Arrange
    mock_get_by_email.return_value = mock_user
    mock_verify_password.return_value = True
    
    # Act
    result = user_service.authenticate(email="test@example.com", password="correct_password")
    
    # Assert
    assert result == mock_user
    mock_verify_password.assert_called_once_with("correct_password", "hashed_password")


@patch("app.core.security.verify_password")
@patch("app.repositories.user_repository.UserRepository.get_by_email")
def test_authenticate_returns_none_when_invalid_password(
    mock_get_by_email, mock_verify_password, user_service, mock_user
):
    """Test that authenticate returns None when password is invalid"""
    # Arrange
    mock_get_by_email.return_value = mock_user
    mock_verify_password.return_value = False
    
    # Act
    result = user_service.authenticate(email="test@example.com", password="wrong_password")
    
    # Assert
    assert result is None
    mock_verify_password.assert_called_once_with("wrong_password", "hashed_password")

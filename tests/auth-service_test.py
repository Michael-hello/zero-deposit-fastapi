
import pytest
from fastapi import HTTPException
from app.api.auth.schema import UserCreate, UserLoginRequest
from tests.helpers import init_test_db
from app.api.auth.service import UserService


def test_create():
    """Test UserService.create """
    
    mock_session = init_test_db(inMemory=True)
    service = UserService(session=mock_session)
    
    user_create = UserCreate(
        password="password123",
        username="mike"
    )

    _user = service.create(user_create)
    created_user = service.get_user(mock_session, _user.username)

    assert created_user.username == "mike"


def test_login_success():
    """Test UserService.login with correct credentials"""
    
    mock_session = init_test_db(inMemory=True)
    service = UserService(session=mock_session)
    
    # Create a user first
    user_create = UserCreate(
        password="password123",
        username="testuser"
    )
    created_user = service.create(user_create)
    
    # Login with correct credentials
    login_request = UserLoginRequest(
        username="testuser",
        password="password123"
    )
    
    logged_in_user = service.login(login_request)
    
    assert logged_in_user.id == created_user.id
    assert logged_in_user.username == "testuser"


def test_login_invalid_username():
    """Test UserService.login with invalid username"""
    
    mock_session = init_test_db(inMemory=True)
    service = UserService(session=mock_session)
    
    login_request = UserLoginRequest(
        username="nonexistent",
        password="password123"
    )
    
    with pytest.raises(HTTPException) as exc_info:
        service.login(login_request)
    
    assert exc_info.value.status_code == 401
    assert "Incorrect username or password" in exc_info.value.detail


def test_login_invalid_password():
    """Test UserService.login with incorrect password"""
    
    mock_session = init_test_db(inMemory=True)
    service = UserService(session=mock_session)
    
    # Create a user first
    user_create = UserCreate(
        password="password123",
        username="testuser"
    )
    service.create(user_create)
    
    # Login with incorrect password
    login_request = UserLoginRequest(
        username="testuser",
        password="wrongpassword"
    )
    
    with pytest.raises(HTTPException) as exc_info:
        service.login(login_request)
    
    assert exc_info.value.status_code == 401
    assert "Incorrect username or password" in exc_info.value.detail


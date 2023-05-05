import pytest
from unittest.mock import MagicMock, patch, ANY

from core.config import settings
from core.jwt_authentication.jwt_bearer import jwt_scheme
from main import app
from tests.conftest import get_test_db

test_user_1 = {
    "username": "test_user_1",
    "is_active": False,
    "created_at": "2038-01-19T03:14:07.123456",
    "updated_at": "2038-01-19T03:14:07.123456"
}

test_user_profile_1 = {
    "username": "test_user_1",
    "first_name": "Test",
    "last_name": "User",
    "created_at": "2038-01-19T03:14:07.123456",
    "updated_at": "2038-01-19T03:14:07.123456",
    "tasks": []
}


# Override the JWT scheme dependency in the test environment
def mock_jwt_scheme():
    return "test_user_1"

app.dependency_overrides[jwt_scheme] = mock_jwt_scheme


def test_read_users(get_test_db):
    #1 Test the read_users endpoint for calling the crud_user.get_users function
    mock_get_users = MagicMock(return_value=[test_user_1])
    with patch("crud.crud_user.get_users", mock_get_users):
        response = get_test_db.get(
            f"{settings.API_V1_STR}/users/",
            headers={"Authorization": "Bearer test_token"}
        )
        mock_get_users.assert_called_once(), \
            "The crud_user's get_users function should be called"
        assert response.status_code == 200, \
            "The response should contain a success status code"
        assert response.json() == [test_user_1], \
            "The response should be a list containing Test user"


def test_create_user(get_test_db):
    #2 Test the signup endpoint for calling the crud_user.create_user function
    mock_get_user = MagicMock(return_value=None)
    mock_create_user = MagicMock(return_value=test_user_1)
    mock_user_profile_create = MagicMock(return_value=None)
    with patch("crud.crud_user.get_user", mock_get_user), \
        patch("crud.crud_user.create_user", mock_create_user), \
        patch("crud.crud_user_profile.user_profile_create", \
        mock_user_profile_create):
        response = get_test_db.post(
            f"{settings.API_V1_STR}/users/signup/",
            json={"username": "test_user", "password": "test_password"}
        )
        mock_get_user.assert_called_once(), \
            "The crud_user's get_user function should be called"
        mock_create_user.assert_called_once(), \
            "The crud_user's create_user function should be called"
        mock_user_profile_create.assert_called_once(), \
            "The crud_user_profile's user_profile_create function should be called"
        assert response.status_code == 201, \
            "The response should contain a created status code"
        assert response.json() == test_user_1, \
            "The response should be a dict containing Test user"


def test_read_current_user(get_test_db):
    #3 Test the read_current_user endpoint for calling the crud_user_profile.user_profile_get function
    mock_user_profile_get = MagicMock(return_value=test_user_profile_1)
    with patch("crud.crud_user_profile.user_profile_get", mock_user_profile_get):
        response = get_test_db.get(
            f"{settings.API_V1_STR}/users/me/",
            headers={"Authorization": "Bearer test_token"}
        )
        mock_user_profile_get.assert_called_once_with(db=ANY, username=test_user_profile_1['username']), \
            "The crud_user_profile's user_profile_get function should be called with the test_user1 username"
        assert response.status_code == 200, \
            "The response should contain a success status code"
        assert response.json() == test_user_profile_1, \
            "The response should be a dict containing Test user profile"


def test_read_user(get_test_db):
    #4 Test the read_user endpoint for calling the crud_user_profile.user_profile_get function
    mock_user_profile_get = MagicMock(return_value=test_user_profile_1)
    with patch("crud.crud_user_profile.user_profile_get", mock_user_profile_get):
        response = get_test_db.get(
            f"{settings.API_V1_STR}/users/user/{test_user_profile_1['username']}/",
            headers={"Authorization": "Bearer test_token"}
        )
        mock_user_profile_get.assert_called_once_with(db=ANY, username=test_user_profile_1['username']), \
            "The crud_user_profile's user_profile_get function should be called with the test_user1 username"
        assert response.status_code == 200, \
            "The response should contain a success status code"
        assert response.json() == test_user_profile_1, \
            "The response should be a dict containing Test user profile"


def test_update_user_profile(get_test_db):
    #5 Test the update_user_profile endpoint for calling the crud_user_profile's user_profile_get and user_profile_update functions
    mock_user_profile_get = MagicMock(return_value=test_user_profile_1)
    mock_user_profile_update = MagicMock(return_value=test_user_profile_1)
    with patch("crud.crud_user_profile.user_profile_get", mock_user_profile_get), \
        patch("crud.crud_user_profile.user_profile_update", mock_user_profile_update):
        response = get_test_db.patch(
            f"{settings.API_V1_STR}/users/user/{test_user_profile_1['username']}/",
            headers={"Authorization": "Bearer test_token"},
            json={"first_name": "Test", "last_name": "User"}
        )
        mock_user_profile_get.assert_called_once_with(db=ANY, username=test_user_profile_1['username']), \
            "The crud_user_profile's user_profile_get function should be called with the test_user1 username"
        mock_user_profile_update.assert_called_once_with(
            db=ANY,
            user_profile=ANY,
            username=test_user_profile_1['username']
        ), \
            "The crud_user_profile's user_profile_update function should be called with the test_user1 user profile"
        assert response.status_code == 200, \
            "The response should contain a success status code"
        assert response.json() == test_user_profile_1, \
            "The response should be a dict containing Test user profile"


def test_delete_user_by_username(get_test_db):
    #6 Test the delete_user_by_username endpoint for calling the crud_user's delete_user function
    mock_get_user = MagicMock(return_value=test_user_1)
    mock_delete_user = MagicMock(return_value=test_user_1)
    with patch("crud.crud_user.get_user", mock_get_user), \
        patch("crud.crud_user.delete_user", mock_delete_user):
        response = get_test_db.delete(
            f"{settings.API_V1_STR}/users/user/{test_user_1['username']}/",
            headers={"Authorization": "Bearer test_token"}
        )
        mock_get_user.assert_called_once_with(db=ANY, username=test_user_1['username']), \
            "The crud_user's get_user function should be called with the test_user1 username"
        mock_delete_user.assert_called_once_with(db=ANY, username=test_user_1['username']), \
            "The crud_user's delete_user function should be called with the test_user1 username"
        assert response.status_code == 200, \
            "The response should contain a success status code"
        assert response.json() == {"detail": f"User {test_user_1['username']} deleted successfully."}, \
            "The response should be a dict containing a success message"

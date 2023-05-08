import pytest

from datetime import datetime
from unittest.mock import MagicMock, patch

from core.config import settings
from models.task import Task
from models.user import User, UserProfile
from tests.conftest import get_test_db, test_client

user_data = {
    "username": "test_user",
    "password": "test_password"
}

updated_user_data = {
    "first_name": "Test",
    "last_name": "User"
}

test_task_data_1 = {
    "title": "test_task_1",
    "description": "test_description_1"
}

test_task_data_2 = {
    "title": "test_task_2",
    "description": "test_description_2"
}

updated_task_data = {
    "title": "test_task_1_updated",
    "description": "test_description_1_updated",
    "is_done": True
}

auth_headers = None

test_task_id: int = None

# System test the entire system end-to-end, from the user's perspective

def test_create_user(test_client):
    #1 Create a new user and user profile
    response = test_client.post(
        f"{settings.API_V1_STR}/users/signup/",
        json=user_data
    )
    # Test that the user was created successfully
    assert response.status_code == 201, \
        "The response should contain a success status code"
    assert response is not None, \
        "The response should not be None"
    assert response.json()["username"] == user_data["username"], \
        "The response should contain the username"
    assert "hashed_password" not in response.json(), \
        "The response should not contain the hashed_password"

    # Test that the Timestamp columns were automatically populated
    assert "created_at" in response.json(), \
        "The response should contain created_at"
    assert "updated_at" in response.json(), \
        "The response should contain updated_at"


def test_login_user(test_client):
    #2 Login with the new user
    response = test_client.post(
        f"{settings.API_V1_STR}/login/",
        json=user_data
    )

    # Test that the user was logged in successfully
    assert response.status_code == 200, \
        "The response should contain a success status code"
    assert response is not None, \
        "The response should not be None"
    assert response.json()["access_token"] is not None, \
        "The response should contain the access token"
    assert response.json()["token_type"] == "bearer", \
        "The response should contain the token type"
    
    # Save the auth headers for future requests
    auth_token = response.json()["access_token"]
    global auth_headers
    auth_headers = {"Authorization": f"Bearer {auth_token}"}


def test_read_current_user(test_client):
    #3 Retrieve the user profile
    response = test_client.get(
        f"{settings.API_V1_STR}/users/me/",
        headers=auth_headers
    )

    # Test that the user profile was retrieved successfully
    assert response.status_code == 200, \
        "The response should contain a success status code"
    assert response is not None, \
        "The response should not be None"
    assert response.json()["username"] == user_data["username"], \
        "The response should contain the username"
    assert "first_name" in response.json(), \
        "The response should contain first_name"
    assert response.json()["first_name"] is None, \
        "The response should contain first_name"
    assert "last_name" in response.json(), \
        "The response should contain last_name"
    assert response.json()["last_name"] is None, \
        "The response should contain last_name"

    # Test that the Timestamp columns were automatically populated
    assert "created_at" in response.json(), \
        "The response should contain created_at"
    assert "updated_at" in response.json(), \
        "The response should contain updated_at"


def test_update_user_profile(test_client):
    #4 Update the user profile
    response = test_client.patch(
        f"{settings.API_V1_STR}/users/me/",
        headers=auth_headers,
        json=updated_user_data
    )

    # Test that the user profile was updated successfully
    assert response.status_code == 200, \
        "The response should contain a success status code"
    assert response is not None, \
        "The response should not be None"
    assert response.json()["username"] == user_data["username"], \
        "The response should contain the username"
    assert response.json()["first_name"] == updated_user_data["first_name"], \
        "The response should contain the updated first_name"
    assert response.json()["last_name"] == updated_user_data["last_name"], \
        "The response should contain the updated last_name"

    # Test that the Timestamp columns were automatically populated
    assert response.json()["created_at"] != response.json()["updated_at"] , \
        "The created_at and updated_at should be different"


def test_logout_user(test_client):
    #5 Logout
    response = test_client.post(
        f"{settings.API_V1_STR}/logout/",
        headers=auth_headers
    )

    # Test that the user was logged out successfully
    assert response.status_code == 200, \
        "The response should contain a success status code"


def test_post_task(test_client):
    #6 Create a new tasks
    response = test_client.post(
        f"{settings.API_V1_STR}/tasks/",
        headers=auth_headers,
        json=test_task_data_1
    )

    # Test that the task was created successfully
    assert response.status_code == 201, \
        "The response should contain a success status code"
    assert response is not None, \
        "The response should not be None"
    assert response.json()["id"] is not None, \
        "The response should contain the id"
    assert response.json()["title"] == test_task_data_1["title"], \
        "The response should contain the title"
    assert response.json()["description"] == test_task_data_1["description"], \
        "The response should contain the description"
    assert response.json()["is_done"] == False, \
        "The response should contain the is_done status"
    assert response.json()["created_by"] == user_data["username"], \
        "The response should contain the username"

    # Test that the Timestamp columns were automatically populated
    assert "created_at" in response.json(), \
        "The response should contain created_at"
    assert "updated_at" in response.json(), \
        "The response should contain updated_at"

    # Save the task 1 id for future requests
    global test_task_id
    test_task_id = int(response.json()["id"])

    # Create a second task
    response = test_client.post(
        f"{settings.API_V1_STR}/tasks/",
        headers=auth_headers,
        json=test_task_data_2
    )


def test_read_user_tasks(test_client):
    #7 Retrieve tasks
    response = test_client.get(
        f"{settings.API_V1_STR}/tasks/",
        headers=auth_headers,
    )

    # Test that the tasks were retrieved successfully
    assert response.status_code == 200, \
        "The response should contain a success status code"
    assert response is not None, \
        "The response should not be None"
    assert len(response.json()) == 2, \
        "The response should contain 2 tasks"


def test_read_task_by_id(test_client):
    #8 Retrieve the task by id
    response = test_client.get(
        f"{settings.API_V1_STR}/tasks/{test_task_id}",
        headers=auth_headers,
    )

    # Test that the task was retrieved successfully
    assert response.status_code == 200, \
        "The response should contain a success status code"
    assert response is not None, \
        "The response should not be None"
    assert response.json()["id"] == test_task_id, \
        "The response should contain the id"
    assert response.json()["title"] == test_task_data_1["title"], \
        "The response should contain the title"
    assert response.json()["description"] == test_task_data_1["description"], \
        "The response should contain the description"


def test_update_task(test_client):
    #8 Update the task
    response = test_client.patch(
        f"{settings.API_V1_STR}/tasks/{test_task_id}",
        headers=auth_headers,
        json=updated_task_data
    )

    # Test that the task was updated successfully
    assert response.status_code == 200, \
        "The response should contain a success status code"
    assert response is not None, \
        "The response should not be None"
    assert response.json()["id"] == test_task_id, \
        "The response should contain the id"
    assert response.json()["title"] == updated_task_data["title"], \
        "The response should contain the updated title"
    assert response.json()["description"] == updated_task_data["description"], \
        "The response should contain the updated description"
    assert response.json()["is_done"] == True, \
        "The response should contain the updated is_done status"
    
    # Test that the Timestamp columns were automatically populated
    assert response.json()["created_at"] != response.json()["updated_at"] , \
        "The created_at and updated_at should be different"


def test_delete_task(test_client):
    #9 Delete the task
    response = test_client.delete(
        f"{settings.API_V1_STR}/tasks/{test_task_id}",
        headers=auth_headers,
    )

    # Test that response was successful
    assert response.status_code == 200, \
        "The response should contain a success status code"
    
    # Test that the task was deleted successfully
    response = test_client.get(
        f"{settings.API_V1_STR}/tasks/{test_task_id}",
        headers=auth_headers,
    )
    assert response.status_code == 404, \
        "The response should contain a not found status code"


def test_delete_user(get_test_db, test_client):
    #10 Delete the user
    response = test_client.delete(
        f"{settings.API_V1_STR}/users/me",
        headers=auth_headers,
    )

    # Test that response was successful
    assert response.status_code == 200, \
        "The response should contain a success status code"
    
    # Test that the user was deleted successfully
    test_user = get_test_db.query(User).filter(User.username == user_data["username"]).first()
    assert test_user is None, \
        "The response should be None"
    
    # Test that the user profile was deleted successfully
    test_user_profile = get_test_db.query(UserProfile).filter(UserProfile.username == user_data["username"]).first()
    assert test_user_profile is None, \
        "The response should be None"
    
    # Test that the user tasks were deleted successfully
    test_task = get_test_db.query(Task).filter(Task.created_by == user_data["username"]).first()
    assert test_task is None, \
        "The response should be None"
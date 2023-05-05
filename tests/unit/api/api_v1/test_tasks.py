import pytest
from unittest.mock import MagicMock, patch, ANY

from core.config import settings
from core.jwt_authentication.jwt_bearer import jwt_scheme
from main import app
from tests.conftest import get_test_db

test_user_1 = {
    "username": "test_user_1"
}

test_task_1 = {
    "id": 1,
    "title": "test_task_1",
    "description": "test_task_1",
    "is_done": False,
    "created_by": "test_user_1",
    "created_at": "2038-01-19T03:14:07.123456",
    "updated_at": "2038-01-19T03:14:07.123456"
}

# Add the created_by attribute to the test_task_obj_1 object
class TestTask:
    def __setattr__(self, key, value):
        self.__dict__[key] = value

test_task_obj_1 = TestTask()
test_task_obj_1.__dict__.update(test_task_1)
test_task_obj_1.created_by = test_task_1.get('created_by', test_user_1["username"])


# Override the JWT scheme dependency in the test environment
def mock_jwt_scheme():
    return "test_user_1"

app.dependency_overrides[jwt_scheme] = mock_jwt_scheme


def test_read_user_tasks(get_test_db):
    #1 Test the read_user_tasks endpoint for calling the crud_task.get_all_user_tasks function
    mock_get_all_user_tasks = MagicMock(return_value=[test_task_1])
    with patch("crud.crud_task.get_all_user_tasks", mock_get_all_user_tasks):
        response = get_test_db.get(
            f"{settings.API_V1_STR}/tasks/",
            headers={"Authorization": "Bearer test_token"}
        )
        mock_get_all_user_tasks.assert_called_once(), \
            "The crud_task's get_all_user_tasks function should be called"
        mock_get_all_user_tasks.assert_called_once_with(db=ANY, username=test_user_1["username"], skip=0, limit=100), \
            "The crud_task's get_all_user_tasks function should be called for test_user_1"
        assert response.status_code == 200, \
            "The response should contain a success status code"
        assert response.json() == [test_task_1], \
            "The response should be a list containing Test task"


def test_create_task(get_test_db):
    #2 Test the create_task endpoint for calling the crud_task's get_task_by_title and create_task functions
    mock_get_task_by_title = MagicMock(return_value=None)
    mock_create_task = MagicMock(return_value=test_task_1)
    with patch("crud.crud_task.get_task_by_title", mock_get_task_by_title), \
        patch("crud.crud_task.create_task", mock_create_task):
        response = get_test_db.post(
            f"{settings.API_V1_STR}/tasks/",
            headers={"Authorization": "Bearer test_token"},
            json={"title": "test_task_1", "description": "test_task_1"}
        )
        mock_get_task_by_title.assert_called_once(), \
            "The crud_task's get_task_by_title function should be called"
        mock_get_task_by_title.assert_called_once_with(db=ANY, task_title=test_task_1["title"], username=test_user_1["username"]), \
            "The crud_task's get_task_by_title function should be called for test_task_1"
        assert response.status_code == 201, \
            "The response should contain a successfully created status code"
        assert response.json() == test_task_1, \
            "The response should contain the created task"


def test_read_task_by_id(get_test_db):
    #3 Test the read_task_by_id endpoint for calling the crud_task's get_task_by_id function
    mock_get_task_by_id = MagicMock(return_value=test_task_1)
    with patch("crud.crud_task.get_task_by_id", mock_get_task_by_id):
        response = get_test_db.get(
            f"{settings.API_V1_STR}/tasks/{test_task_1['id']}",
            headers={"Authorization": "Bearer test_token"}
        )
        mock_get_task_by_id.assert_called_once_with(db=ANY, task_id=test_task_1["id"]), \
            "The crud_task's get_task_by_id function should be called for test_task_1 id"
        assert response.status_code == 200, \
            "The response should contain a success status code"
        assert response.json() == test_task_1, \
            "The response should contain the test_task_1"


def test_update_task_by_id(get_test_db):
    #4 Test the update_task_by_id endpoint for calling the crud_task's get_task_by_id and update_task functions
    mock_get_task_by_id = MagicMock(return_value=test_task_obj_1)
    mock_update_task = MagicMock(return_value=test_task_1)
    with patch("crud.crud_task.get_task_by_id", mock_get_task_by_id), \
        patch("crud.crud_task.update_task", mock_update_task):
        response = get_test_db.patch(
            f"{settings.API_V1_STR}/tasks/{test_task_1['id']}",
            headers={"Authorization": "Bearer test_token"},
            json={"title": "test_task_1", "description": "test_task_1"}
        )
        mock_get_task_by_id.assert_called_once_with(db=ANY, task_id=test_task_1["id"]), \
            "The crud_task's get_task_by_id function should be called for test_task_1 id"
        mock_update_task.assert_called_once_with(db=ANY, task_id=test_task_1["id"], task=ANY), \
            "The crud_task's update_task function should be called for test_task_1 id"
        assert response.status_code == 200, \
            "The response should contain a success status code"
        assert response.json() == test_task_1, \
            "The response should contain the test_task_1"


def test_delete_task_by_id(get_test_db):
    #5 Test the delete_task_by_id endpoint for calling the crud_task's get_task_by_id and delete_task functions
    mock_get_task_by_id = MagicMock(return_value=test_task_obj_1)
    mock_delete_task = MagicMock(return_value=test_task_1)
    with patch("crud.crud_task.get_task_by_id", mock_get_task_by_id), \
        patch("crud.crud_task.delete_task", mock_delete_task):
        response = get_test_db.delete(
            f"{settings.API_V1_STR}/tasks/{test_task_1['id']}",
            headers={"Authorization": "Bearer test_token"}
        )
        mock_get_task_by_id.assert_called_once_with(db=ANY, task_id=test_task_1["id"]), \
            "The crud_task's get_task_by_id function should be called for test_task_1 id"
        mock_delete_task.assert_called_once_with(db=ANY, task_id=test_task_1["id"]), \
            "The crud_task's delete_task function should be called for test_task_1 id"
        assert response.status_code == 200, \
            "The response should contain a success status code"
        assert response.json() == test_task_1, \
            "The response should contain the deleted test_task_1 data"

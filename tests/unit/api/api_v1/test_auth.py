import pytest
from unittest.mock import MagicMock, patch

from core.config import settings
from core.jwt_authentication.jwt_bearer import jwt_scheme
from main import app
from tests.conftest import test_client


# Override the JWT scheme dependency in the test environment
def mock_jwt_scheme():
    return "test_user_1"

app.dependency_overrides[jwt_scheme] = mock_jwt_scheme


def test_user_login(test_client):
    #1 Test the user_login endpoint for calling the crud_user.authenticate function and sign_jwt function
    mock_authenticate = MagicMock(return_value=True)
    mock_sign_jwt = MagicMock(return_value={"access_token": "test_token", "token_type": "bearer"})
    with patch("crud.crud_user.authenticate", mock_authenticate), \
        patch("core.jwt_authentication.jwt_handler.sign_jwt", mock_sign_jwt):
        response = test_client.post(
            f"{settings.API_V1_STR}/login/",
            json={"username": "test_user", "password": "test_password"}
        )
        mock_authenticate.assert_called_once(), \
            "The crud_user's authenticate function should be called"
        mock_sign_jwt.assert_called_once(), \
            "The jwt_handler's sign_jwt function should be called"
        assert response.status_code == 200, \
            "The response should contain a success status code"
        assert response.json() == {"access_token": "test_token", "token_type": "bearer"}, \
            "The response should contain the access token"

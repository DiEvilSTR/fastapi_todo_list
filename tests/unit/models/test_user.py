# from models.user import User
# from tests.conftest import get_test_db
# from tests.utils.utils import random_lower_string

# def test_user_model(get_test_db):
#     test_username = random_lower_string()
#     test_password = random_lower_string()
#     test_user = User(username=test_username, hashed_password=test_password)
#     get_test_db.post("/users/", json=test_user.dict())
#     response = get_test_db.get("/users/test_username")
#     assert response.status_code == 200
#     assert response.json() == {
#         "username": test_username,
#         "hashed_password": test_password,
#         "is_active": False,
#         "profile": None,
#     }
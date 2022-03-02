import pytest
from jose import jwt

from app import schemas
from app.config import settings
# from .database import client, session


# @pytest.fixture
# def test_user(client):
#     user_data = {"email": "test111@gmail.com",
#                  "password": "password123"}
#     res = client.post("/users/", json=user_data)
#
#     assert res.status_code == 201
#
#     new_user = res.json()
#     new_user['password'] = user_data['password']
#     return new_user


# def test_root(client):
#     res = client.get("/")
#
#     assert res.status_code == 200
#     assert res.json().get("message") == "Hello World!!!"


def test_create_user(client):
    # use /users/ instead of /users, because of APIRouter_prefix
    res = client.post("/users/", json={"email": "test@gmail.com", "password": "password123"})
    new_user = schemas.UserOut(**res.json())

    assert new_user.email == "test@gmail.com"
    assert res.status_code == 201


def test_login_user(test_user, client):
    res = client.post("/login", data={"username": test_user['email'], "password": test_user['password']})
    login_res = schemas.Token(**res.json())
    payload = jwt.decode(login_res.access_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    id = payload.get("user_id")

    assert id == test_user['id']
    assert login_res.token_type == "bearer"
    assert res.status_code == 200


@pytest.mark.parametrize("email, password, status_code", [
    ('wrongemail@gmail.com', 'password123', 403),
    ('test111@gmail.com', 'wrongpassword', 403),
    ('wrongemail@gmail.com', 'wrongpassword', 403),
    (None, 'password123', 422),
    ('test111@gmail.com', None, 422),
])
def test_incorrect_login(test_user, client, email, password, status_code):
    res = client.post("/login", data={"username": email, "password": password})

    assert res.status_code == status_code
    # assert res.json().get('detail') == "Invalid Credentials"

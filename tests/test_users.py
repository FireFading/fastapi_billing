from app.utils.messages import messages
from fastapi import status
from pytest_mock import MockerFixture
from tests.settings import Urls, User


class TestRegister:
    async def test_register_user(self, client, mocker: MockerFixture):
        response = client.post(
            Urls.register,
            json={
                "email": User.email,
                "name": User.name,
                "phone": User.phone,
                "password": User.password,
            },
        )
        assert response.status_code == status.HTTP_201_CREATED
        assert response.json().get("detail") == messages.USER_CREATED

    async def test_failed_repeat_register_user(self, register_user, client):
        response = client.post(
            Urls.register,
            json={
                "email": User.email,
                "name": User.name,
                "phone": User.phone,
                "password": User.password,
            },
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json().get("detail") == messages.USER_ALREADY_EXISTS

    async def test_login_unregistered_user(self, client):
        response = client.post(Urls.login, json={"email": User.email, "password": User.password})
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json().get("detail") == messages.USER_NOT_FOUND


class TestLogin:
    async def test_login_user(self, register_user, client):
        response = client.post(Urls.login, json={"email": User.email, "password": User.password})
        assert response.status_code == status.HTTP_200_OK
        assert "access_token" in response.json()
        assert "refresh_token" in response.json()

    async def test_wrong_password_login(self, register_user, client):
        response = client.post(
            Urls.login,
            json={"email": User.email, "password": User.wrong_password},
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.json().get("detail") == messages.WRONG_PASSWORD


class TestLogout:
    async def test_logout_user(self, auth_client):
        response = auth_client.delete(Urls.logout)
        assert response.status_code == status.HTTP_200_OK
        assert response.json().get("detail") == messages.USER_LOGOUT

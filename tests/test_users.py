import pytest
from app.utils.messages import messages
from fastapi import status
from pytest_mock import MockerFixture
from tests.settings import (
    Urls,
    User,
    change_password_schema,
    create_fake_token,
    login_credentials_schema,
    only_old_passwords_schema,
    register_user_schema,
    reset_password_token,
    wrong_change_password_schema,
    wrong_login_credentials_schema,
    wrong_old_password_schema,
)


class TestRegister:
    async def test_register_user(self, client, mocker: MockerFixture):
        response = client.post(
            Urls.register,
            json=register_user_schema,
        )
        assert response.status_code == status.HTTP_201_CREATED
        assert response.json().get("detail") == messages.USER_CREATED

    async def test_failed_repeat_register_user(self, register_user, client):
        response = client.post(
            Urls.register,
            json=register_user_schema,
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json().get("detail") == messages.USER_ALREADY_EXISTS


class TestLogin:
    async def test_login_user(self, register_user, client):
        response = client.post(Urls.login, json=login_credentials_schema)
        assert response.status_code == status.HTTP_200_OK
        assert "access_token" in response.json()
        assert "refresh_token" in response.json()

    async def test_wrong_password_login(self, register_user, client):
        response = client.post(
            Urls.login,
            json=wrong_login_credentials_schema,
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.json().get("detail") == messages.WRONG_PASSWORD

    async def test_user_not_found(self, client):
        response = client.post(Urls.login, json=login_credentials_schema)
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json().get("detail") == messages.USER_NOT_FOUND


class TestChangePassword:
    @pytest.mark.parametrize(
        "password_schema, expected_status_code, expected_detail",
        [
            (
                change_password_schema,
                status.HTTP_202_ACCEPTED,
                messages.PASSWORD_UPDATED,
            ),
            (
                wrong_change_password_schema,
                status.HTTP_400_BAD_REQUEST,
                messages.PASSWORDS_NOT_MATCH,
            ),
            (
                only_old_passwords_schema,
                status.HTTP_400_BAD_REQUEST,
                messages.NEW_PASSWORD_SIMILAR_OLD,
            ),
            (
                wrong_old_password_schema,
                status.HTTP_203_NON_AUTHORITATIVE_INFORMATION,
                messages.WRONG_OLD_PASSWORD,
            ),
        ],
    )
    async def test_user_change_password(self, auth_client, password_schema, expected_status_code, expected_detail):
        response = auth_client.post(
            Urls.change_password,
            json=password_schema,
        )
        assert response.status_code == expected_status_code
        assert response.json().get("detail") == expected_detail


class TestLogout:
    async def test_logout_user(self, auth_client):
        response = auth_client.delete(Urls.logout)
        assert response.status_code == status.HTTP_200_OK
        assert response.json().get("detail") == messages.USER_LOGOUT


class TestForgotPassword:
    @pytest.mark.parametrize(
        "email, expected_status, expected_detail",
        [
            (User.email, status.HTTP_202_ACCEPTED, messages.RESET_PASSWORD_MAIL_SENT),
            ("unknown@example.com", status.HTTP_404_NOT_FOUND, messages.USER_NOT_FOUND),
        ],
    )
    async def test_forgot_password(self, register_user, client, email, expected_status, expected_detail):
        response = client.post(Urls.forgot_password, json={"email": email})
        assert response.status_code == expected_status
        assert response.json().get("detail") == expected_detail


class TestResetPassword:
    @pytest.mark.parametrize(
        "token, payload, expected_status, expected_detail",
        [
            (
                reset_password_token,
                change_password_schema,
                status.HTTP_202_ACCEPTED,
                messages.PASSWORD_RESET,
            ),
            (
                create_fake_token(),
                change_password_schema,
                status.HTTP_203_NON_AUTHORITATIVE_INFORMATION,
                messages.INVALID_TOKEN,
            ),
            (
                reset_password_token,
                wrong_change_password_schema,
                status.HTTP_203_NON_AUTHORITATIVE_INFORMATION,
                messages.PASSWORDS_NOT_MATCH,
            ),
        ],
    )
    async def test_reset_password(self, register_user, client, token, payload, expected_status, expected_detail):
        response = client.post(
            f"{Urls.reset_password}{token}",
            json=payload,
        )
        assert response.status_code == expected_status
        assert response.json().get("detail") == expected_detail

    async def test_unregistered_user_reset_password(self, client):
        response = client.post(
            f"{Urls.reset_password}{reset_password_token}",
            json=change_password_schema,
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json().get("detail") == messages.USER_NOT_FOUND

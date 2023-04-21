import pytest
from app.utils.messages import messages
from fastapi import status
from tests.settings import Urls, top_up_balance_schema, withdraw_balance_schema


class TestBalance:
    @pytest.mark.parametrize(
        "url, method, post_data",
        [
            (Urls.deposit, "GET", None),
            (Urls.withdraw_balance, "POST", withdraw_balance_schema),
            (Urls.history, "GET", None),
            (Urls.top_up_balance, "POST", top_up_balance_schema),
        ],
    )
    async def test_not_found_balance(self, auth_client, url, method, post_data):
        if method == "GET":
            response = auth_client.get(url)
        elif method == "POST":
            response = auth_client.post(url, json=post_data)
        else:
            raise ValueError(f"Invalid method: {method}")
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json().get("detail") == messages.BALANCE_NOT_FOUND

    async def test_create_balance(self, auth_client):
        response = auth_client.post(Urls.create_balance)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.json().get("detail") == messages.BALANCE_CREATED

        response = auth_client.get(Urls.deposit)
        assert response.status_code == status.HTTP_200_OK
        assert float(response.json().get("deposit")) == 0

    async def test_failed_repeat_create_balance(self, create_balance, auth_client):
        response = auth_client.post(Urls.create_balance)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json().get("detail") == messages.BALANCE_ALREADY_EXISTS

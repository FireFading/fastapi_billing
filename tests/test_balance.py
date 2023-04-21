from app.utils.messages import messages
from fastapi import status
from pytest_mock import MockerFixture
from tests.settings import Urls, User


class TestBalance:
    async def test_top_up_balance(self, auth_client):
        response = auth_client.post(Urls.top_up_balance, json={"amount": 100})
        assert response.status_code == status.HTTP_200_OK
        result = response.json()
        assert result.get("detail") == messages.BALANCE_TOP_UP
        assert float(result.get("deposit")) == 100

        response = auth_client.get(Urls.history)
        assert response.status_code == status.HTTP_200_OK
        assert response.json() is not None

        response = auth_client.get(Urls.deposit)
        assert response.status_code == status.HTTP_200_OK
        assert float(response.json().get("deposit")) == 100

    async def test_withdraw_balance(self, auth_client):
        response = auth_client.post(Urls.top_up_balance, json={"amount": 100})
        assert response.status_code == status.HTTP_200_OK
        assert response.json().get("detail") == messages.BALANCE_TOP_UP

        response = auth_client.post(Urls.withdraw_balance, json={"amount": -10})
        assert response.status_code == status.HTTP_200_OK
        result = response.json()
        assert result.get("detail") == messages.BALANCE_WITHDRAW
        assert float(result.get("deposit")) == 100 - 10

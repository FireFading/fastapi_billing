from app.utils.messages import messages
from fastapi import status
from tests.settings import Urls, top_up_balance_schema, withdraw_balance_schema


class TestBalance:
    async def test_create_balance(self, auth_client):
        response = auth_client.post(Urls.create_balance)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.json().get("detail") == messages.BALANCE_CREATED

    async def test_top_up_balance(self, create_balance, auth_client):
        response = auth_client.post(Urls.top_up_balance, json=top_up_balance_schema)
        assert response.status_code == status.HTTP_200_OK
        result = response.json()
        assert result.get("detail") == messages.BALANCE_TOP_UP
        assert float(result.get("deposit")) == 100

        response = auth_client.get(Urls.history)
        assert response.status_code == status.HTTP_200_OK
        assert response.json() is not None

        response = auth_client.get(Urls.deposit)
        assert response.status_code == status.HTTP_200_OK
        assert float(response.json().get("deposit")) == top_up_balance_schema.get("amount")

    async def test_withdraw_balance(self, create_balance, auth_client):
        response = auth_client.post(Urls.top_up_balance, json=top_up_balance_schema)
        assert response.status_code == status.HTTP_200_OK
        assert response.json().get("detail") == messages.BALANCE_TOP_UP

        response = auth_client.post(Urls.withdraw_balance, json=withdraw_balance_schema)
        assert response.status_code == status.HTTP_200_OK
        result = response.json()
        assert result.get("detail") == messages.BALANCE_WITHDRAW
        assert float(result.get("deposit")) == top_up_balance_schema.get("amount") + withdraw_balance_schema.get(
            "amount"
        )

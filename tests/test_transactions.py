from app.utils.messages import messages
from fastapi import status
from tests.settings import Urls, User, balance_after_transactions, top_up_balance_schema, withdraw_balance_schema


class TestTransaction:
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
        assert float(result.get("deposit")) == balance_after_transactions

    async def test_failed_withdraw_balance(self, create_balance, auth_client):
        response = auth_client.post(Urls.withdraw_balance, json=withdraw_balance_schema)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json().get("detail") == messages.INSUFFICIENT_FUNDS

    async def test_get_transactions(self, create_transactions, auth_client):
        response = auth_client.get(Urls.history)
        assert response.status_code == status.HTTP_200_OK
        result = response.json()
        assert len(result) == 2
        assert {
            tuple(
                element.get("user").values(),
            )
            for element in result
        } == {(User.email,)}
        assert sum(element.get("amount") for element in result) == balance_after_transactions

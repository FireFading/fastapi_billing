import pytest
from app.utils.messages import messages
from fastapi import status
from tests.settings import (
    Urls,
    balance_after_transactions,
    top_up_balance_schema,
    transfer_schema,
    withdraw_balance_schema,
)


class TestTransfer:
    async def test_transfer_to_another_user(self, another_user, create_transactions, auth_client):
        response = auth_client.get(Urls.deposit)
        assert response.status_code == status.HTTP_200_OK
        assert float(response.json().get("deposit")) == top_up_balance_schema.get(
            "amount"
        ) + withdraw_balance_schema.get("amount")

        response = auth_client.post(Urls.transfer, json=transfer_schema)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.json().get("detail") == messages.TRANSFER_SUCCESSFUL

        response = auth_client.get(Urls.history)
        assert response.status_code == status.HTTP_200_OK
        assert response.json() is not None

        response = auth_client.get(Urls.deposit)
        assert response.status_code == status.HTTP_200_OK
        assert float(response.json().get("deposit")) == balance_after_transactions + transfer_schema.get("amount")

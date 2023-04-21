from app.utils.messages import messages
from fastapi import status
from pytest_mock import MockerFixture
from tests.settings import Urls, User


class TestBalance:
    async def test_top_up_balance(self, auth_client):
        response = auth_client.post(Urls.top_up_balance, json={"amount": 100})
        assert response.status_code == status.HTTP_200_OK
        assert response.json().get("detail") == messages.BALANCE_TOP_UP

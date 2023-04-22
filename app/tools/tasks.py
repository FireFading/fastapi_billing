import asyncio

import aiohttp
import orjson
from app.config import settings
from app.database import async_session
from app.models.currencies import Currency as CurrencyModel
from celery import shared_task


async def get_async(url: str, headers: dict):
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(limit=100)) as session:
        async with session.get(url=url, headers=headers) as response:
            return await response.text()


async def load_currency_data(name: str, full_name: str, symbol: str):
    async with async_session() as session:
        await CurrencyModel(name=name, full_name=full_name, symbol=symbol).get_or_create(session=session)
        print("ADD")


@shared_task(name="update_currencies")
def update_currencies():
    url = "https://api.freecurrencyapi.com/v1/currencies"
    headers = {"apikey": settings.api_currency_key}
    response = asyncio.run(
        get_async(
            url=url,
            headers=headers,
        )
    )
    data = orjson.loads(response).get("data")

    for values in data.values():
        full_name = values.get("name", "1")
        symbol = values.get("symbol")
        code = values.get("code")
        asyncio.run(load_currency_data(name=code, full_name=full_name, symbol=symbol))

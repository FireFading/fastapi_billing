import asyncio
import orjson

import aiohttp
from app.config import settings
from celery import shared_task


async def get_async(url: str, headers: dict):
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(limit=100)) as session:
        async with session.get(url=url, headers=headers) as response:
            return await response.text()


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
    data = orjson.loads(response)
    print(data.get("data").keys())

import asyncio

import aiohttp
import orjson
from app.config import settings
from app.controllers.currencies import currency_controller
from app.database import async_session
from app.models.currencies import Currency as CurrencyModel
from celery import shared_task


async def get_async(url: str, headers: dict, params: dict | None = None):
    async with aiohttp.ClientSession(
        connector=aiohttp.TCPConnector(limit=100)
    ) as session:
        async with session.get(url=url, headers=headers, params=params) as response:
            return await response.text()


async def load_currency_data(currency_data: set):
    async with async_session() as session:
        instances = []
        for data in currency_data:
            full_name, symbol, code = data
            currency = await CurrencyModel(
                name=code, full_name=full_name, symbol=symbol
            )
            instances.append(currency)
        await CurrencyModel.bulk_create(session=session, instances=instances)


async def update_currency_data(currency_data: dict):
    async with async_session() as session:
        await currency_controller.update_prices(
            session=session, currency_data=currency_data
        )


async def get_currency_list():
    [currency.name for currency in await currency_controller.get_all_available()]


@shared_task(name="get_currencies")
def get_currencies():
    url = "https://api.freecurrencyapi.com/v1/currencies"
    headers = {"apikey": settings.api_currency_key}
    response = asyncio.run(
        get_async(
            url=url,
            headers=headers,
        )
    )
    data = orjson.loads(response).get("data")

    currency_data = set()
    for values in data.values():
        full_name = values.get("name", "1")
        symbol = values.get("symbol")
        code = values.get("code")
        currency_data.add((full_name, symbol, code))
    asyncio.run(load_currency_data(currency_data=currency_data))


@shared_task(name="update_currency_prices")
def update_currency_prices(
    base_currency: str = "USD", currency_list: list[str] | None = None
):
    url = "https://api.freecurrencyapi.com/v1/latest"
    headers = {"apikey": settings.api_currency_key}
    if not currency_list:
        currency_list = asyncio.run(get_currency_list())
    params = {"base_currency": base_currency, "currencies": currency_list}
    response = asyncio.run(get_async(url=url, headers=headers, params=params))
    currency_data = orjson.loads(response).get("data")
    asyncio.run(update_currency_data(currency_data=currency_data))

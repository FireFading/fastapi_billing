from collections.abc import Iterable
from datetime import datetime, timedelta

from app.models.currencies import Currency as CurrencyModel
from app.models.currencies import CurrencyPrice as CurrencyPriceModel
from app.repositories.currencies import currency_repository
from app.utils.messages import messages
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession


class CurrencyController:
    @classmethod
    async def get_by_name(cls, session: AsyncSession, name: str) -> CurrencyModel | None:
        return await currency_repository.get(session=session, name=name)

    @classmethod
    async def get_all_available(cls, session: AsyncSession) -> Iterable[CurrencyModel] | None:
        return await currency_repository.all(session=session)

    @classmethod
    async def get_price_history(
        cls,
        session: AsyncSession,
        name: str,
        start_time: datetime | None = None,
        end_time: datetime = datetime.now(),
    ):
        if not (currency := await cls.get_by_name(session=session, name=name)):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=messages.CURRENCY_NOT_FOUND,
            )
        return await currency_repository.get_prices(
            currency_id=currency.id,
            session=session,
            start_time=start_time,
            end_time=end_time,
        )

    @classmethod
    async def get_current_price(cls, session: AsyncSession, name: str):
        start_time = datetime.now() - timedelta(days=3)
        prices: list[CurrencyPriceModel] = await cls.get_price_history(
            session=session, start_time=start_time, name=name
        )
        return prices[0].price

    @classmethod
    async def get_current_prices_for_all(cls, session):
        currencies = await cls.get_all_available(session=session)
        prices = {}
        for currency in currencies:
            prices[currency.name] = await cls.get_current_price(session=session, name=currency.name)
        return prices

    @classmethod
    async def add_new_price(cls, session: AsyncSession, name: str, price: float):
        currency = await cls.get_by_name(session=session, name=name)
        currency_price = CurrencyPriceModel(currency=currency, price=price)
        await currency_repository.create(instance=currency_price, session=session)

    @classmethod
    async def update_prices(cls, session: AsyncSession, currency_data: dict):
        for currency_name, price in currency_data.items():
            await cls.add_new_price(session=session, name=currency_name, price=price)


currency_controller = CurrencyController()

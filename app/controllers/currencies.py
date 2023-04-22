from datetime import datetime, timedelta

from app.models.currencies import Currency as CurrencyModel
from app.models.currencies import CurrencyPrice as CurrencyPriceModel
from sqlalchemy.ext.asyncio import AsyncSession


class CurrencyController:
    @classmethod
    async def get_by_name(cls, session: AsyncSession, name: str) -> CurrencyModel | None:
        return await CurrencyModel.get(session=session, name=name)

    @classmethod
    async def get_all_available(cls, session: AsyncSession) -> list[CurrencyModel]:
        return await CurrencyModel.all(session=session)

    @classmethod
    async def get_price_history(
        cls,
        session: AsyncSession,
        name: str,
        start_time: datetime | None = None,
        end_time: datetime = datetime.now(),
    ):
        currency = await cls.get_by_name(session=session, name=name)
        return await currency.get_prices(session=session, start_time=start_time, end_time=end_time)

    @classmethod
    async def get_current_price(cls, session: AsyncSession, name: str):
        start_time = datetime.now() - timedelta(days=3)
        prices: list[CurrencyPriceModel] = await cls.get_price_history(
            session=session, start_time=start_time, name=name
        )
        return prices[0].price


currency_controller = CurrencyController()

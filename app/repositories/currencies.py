import uuid
from collections.abc import Iterable
from datetime import datetime

from app.models.currencies import Currency as CurrencyModel
from app.models.currencies import CurrencyPrice as CurrencyPriceModel
from app.repositories.base import BaseRepository
from sqlalchemy.ext.asyncio import AsyncSession


class CurrencyRepository(BaseRepository):
    def __init__(self):
        super().__init__(model=CurrencyModel)

    async def get_prices(
        self,
        session: AsyncSession,
        currency_id: uuid.UUID,
        start_time: datetime | None = None,
        end_time: datetime = datetime.now(),
    ) -> Iterable[CurrencyPriceModel] | None:
        return (
            await self.filter(
                currency_id=currency_id,
                session=session,
                order_by="-timestamp",
                timestamp__gte=start_time,
                timestamp__lte=end_time,
            )
            if start_time
            else await self.filter(
                currency_id=currency_id,
                session=session,
                order_by="-timestamp",
                timestamp__lte=end_time,
            )
        )


currency_repository = CurrencyRepository()

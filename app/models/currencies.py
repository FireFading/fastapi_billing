import uuid
from datetime import datetime

from app.crud import CRUD
from app.database import Base
from sqlalchemy import Column, DateTime, Float, String
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import relationship
from sqlalchemy_utils import CurrencyType, UUIDType


class Currency(Base, CRUD):
    __tablename__ = "currencies"

    guid = Column(UUIDType(binary=False), primary_key=True, index=True, default=uuid.uuid4)
    name = Column(CurrencyType, nullable=False)
    symbol = Column(String, nullable=True)

    async def get_prices(
        self,
        session: AsyncSession,
        start_time: datetime | None = None,
        end_time: datetime = datetime.now(),
    ) -> list["CurrencyPrice"]:
        return (
            await self.filter(
                currency_id=self.id,
                session=session,
                order_by="-timestamp",
                timestamp__gte=start_time,
                timestamp__lte=end_time,
            )
            if start_time
            else await self.filter(
                currency_id=self.id,
                session=session,
                order_by="-timestamp",
                timestamp__lte=end_time,
            )
        )


class CurrencyPrice(Base, CRUD):
    __tablename__ = "currency_prices"

    guid = Column(UUIDType(binary=False), primary_key=True, index=True, default=uuid.uuid4)
    currency_id = Column(UUIDType(binary=False))
    price = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)

    currency = relationship("Currency", backref="prices")

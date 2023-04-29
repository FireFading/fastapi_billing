import uuid
from datetime import datetime

from app.database import Base
from sqlalchemy import Column, DateTime, Float, ForeignKey, String
from sqlalchemy.orm import relationship
from sqlalchemy_utils import CurrencyType, UUIDType


class Currency(Base):
    __tablename__ = "currencies"

    guid = Column(UUIDType(binary=False), primary_key=True, index=True, default=uuid.uuid4)
    name = Column(CurrencyType, nullable=False)
    full_name = Column(String, nullable=False)
    symbol = Column(String, nullable=True)


class CurrencyPrice(Base):
    __tablename__ = "currency_prices"

    guid = Column(UUIDType(binary=False), primary_key=True, index=True, default=uuid.uuid4)
    currency_id = Column(UUIDType(binary=False), ForeignKey("currencies.guid"))
    price = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)

    currency = relationship("Currency", backref="prices")

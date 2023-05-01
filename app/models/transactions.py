import uuid
from datetime import datetime

from app.database import Base
from sqlalchemy import Column, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy_utils import CurrencyType, UUIDType


class Transaction(Base):
    __tablename__ = "transactions"

    guid = Column(UUIDType(binary=False), primary_key=True, index=True, default=uuid.uuid4)
    amount = Column(Float)
    currency = Column(CurrencyType, nullable=False, default="USD")
    timestamp = Column(DateTime, default=datetime.utcnow)

    user_id = Column(UUIDType(binary=False), ForeignKey("users.guid"), nullable=False)

    balance_id = Column(UUIDType(binary=False), ForeignKey("balances.guid"), nullable=False)

    user = relationship("User")
    balance = relationship("Balance", back_populates="transactions")

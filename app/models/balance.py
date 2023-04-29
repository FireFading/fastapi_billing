import uuid
from datetime import datetime

from app.database import Base
from sqlalchemy import Column, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy_utils import CurrencyType, UUIDType


class Balance(Base):
    __tablename__ = "balances"

    guid = Column(UUIDType(binary=False), primary_key=True, index=True, default=uuid.uuid4)
    deposit = Column(Float, default=0)
    currency = Column(CurrencyType, nullable=False, default="USD")

    user_id = Column(UUIDType(binary=False), ForeignKey("users.guid"))

    user = relationship("User", back_populates="balance", lazy="selectin")
    transactions = relationship("Transaction", back_populates="balance", lazy="selectin")

    def __repr__(self):
        return f"Deposit of {self.user} in {self.currency}"


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

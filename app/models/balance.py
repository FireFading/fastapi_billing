import uuid
from datetime import datetime

from app.crud import CRUD
from app.database import Base
from sqlalchemy import Column, DateTime, Float, ForeignKey
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import relationship
from sqlalchemy_utils import UUIDType


class Balance(Base, CRUD):
    __tablename__ = "balances"

    guid = Column(
        UUIDType(binary=False), primary_key=True, index=True, default=uuid.uuid4
    )
    deposit = Column(Float, default=0)

    user_id = Column(UUIDType(binary=False), ForeignKey("users.guid"))

    user = relationship("User", back_populates="balance", lazy="selectin")
    transactions = relationship(
        "Transaction", back_populates="balance", lazy="selectin"
    )

    def __repr__(self):
        return f"Deposit of {self.user}"

    async def update(self, transaction_amount: float, session: AsyncSession):  # type: ignore
        self.deposit += transaction_amount
        return await super().update(session=session)


class Transaction(Base, CRUD):
    __tablename__ = "transactions"

    guid = Column(
        UUIDType(binary=False), primary_key=True, index=True, default=uuid.uuid4
    )
    amount = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)

    user_id = Column(UUIDType(binary=False), ForeignKey("users.guid"), nullable=False)

    balance_id = Column(
        UUIDType(binary=False), ForeignKey("balances.guid"), nullable=False
    )

    user = relationship("User")
    balance = relationship("Balance", back_populates="transactions")

    async def create(self, session: AsyncSession, transfer: bool = False):
        print(transfer)
        if transfer:
            await self.user.balance.update(
                transaction_amount=self.amount, session=session
            )
            await self.balance.update(
                transaction_amount=abs(self.amount), session=session
            )
        else:
            await self.balance.update(transaction_amount=self.amount, session=session)
        return await super().create(session=session)

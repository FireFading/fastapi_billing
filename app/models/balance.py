import uuid

from app.crud import CRUD
from app.database import Base
from sqlalchemy import Column, String, Float, ForeignKey, Integer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy_utils import UUIDType
from sqlalchemy.orm import relationship


class Balance(Base, CRUD):
    __tablename__ = "balance"

    guid = Column(
        UUIDType(binary=False), primary_key=True, index=True, default=uuid.uuid4
    )
    user_id = Column(UUIDType(binary=False), ForeignKey("users.guid"))
    user = relationship("User", back_populates="balance")
    transaction_id = Column(UUIDType(binary=False), ForeignKey("transactions.guid"), nullable=True)
    transaction = relationship("Transaction", back_populates="balance")
    deposit = Column(Float, default=0)


class Transaction(Base):
    __tablename__ = "transactions"

    guid = Column(UUIDType(binary=False), primary_key=True, index=True)
    amount = Column(Float)
    user_id = Column(UUIDType(binary=False), ForeignKey("users.guid"))
    user = relationship("User", back_populates="transactions")
    balance = relationship("Balance", back_populates="transaction", uselist=False)

    async def add_money_to_balance(self, session: AsyncSession):
        session.add(self)
        await session.flush()
        await session.commit()
        self.balance.deposit += self.amount
        self.balance.transaction = self
        await self.balance.update(session)

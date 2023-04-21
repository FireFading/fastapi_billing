import uuid

from app.crud import CRUD
from app.database import Base
from sqlalchemy import Column, Float, ForeignKey
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import relationship
from sqlalchemy_utils import UUIDType


class Balance(Base, CRUD):
    __tablename__ = "balances"

    guid = Column(UUIDType(binary=False), primary_key=True, index=True, default=uuid.uuid4)
    user_id = Column(UUIDType(binary=False), ForeignKey("users.guid"))
    user = relationship("User", back_populates="balance")
    deposit = Column(Float, default=0)

    transactions = relationship("Balance",  lazy="joined", backref="balance")


class Transaction(Base):
    __tablename__ = "transactions"

    guid = Column(UUIDType(binary=False), primary_key=True, index=True)
    amount = Column(Float)
    user_id = Column(UUIDType(binary=False), ForeignKey("users.guid"))
    user = relationship("User", back_populates="transactions")

    balance_id = Column(UUIDType(binary=False), ForeignKey("balances.guid"))
    balance = relationship("User", back_populates="transactions")

    async def add_money_to_balance(self, session: AsyncSession):
        session.add(self)
        await session.flush()
        await session.commit()
        self.balance.deposit += self.amount
        self.balance.transaction = self
        await self.balance.update(session)

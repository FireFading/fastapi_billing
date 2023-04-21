import uuid

import bcrypt
from app.crud import CRUD
from app.database import Base
from sqlalchemy import Column, String
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import relationship
from sqlalchemy_utils import UUIDType


class User(Base, CRUD):
    __tablename__ = "users"

    guid = Column(UUIDType(binary=False), primary_key=True, index=True, default=uuid.uuid4)
    email = Column(String, unique=True)
    phone = Column(String, unique=True, nullable=True)
    password = Column(String)
    name = Column(String, unique=False, nullable=True)

    balance = relationship("Balance", back_populates="user", uselist=False, lazy="joined")
    transactions = relationship("Transaction", back_populates="user", lazy="selectin")

    def __repr__(self):
        return f"User {self.email}"

    def get_hashed_password(self) -> str:
        hashed_password = bcrypt.hashpw(self.password.encode(), bcrypt.gensalt())
        return hashed_password.decode()

    def verify_password(self, password: str) -> bool:
        return bcrypt.checkpw(password=password.encode(), hashed_password=self.password.encode())

    async def create(self, session: AsyncSession):
        self.password = self.get_hashed_password()
        return await super().create(session=session)

    async def update(self, session: AsyncSession):
        self.password = self.get_hashed_password()
        return await super().update(session=session)

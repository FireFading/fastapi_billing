from datetime import datetime

from app.schemas.base import CustomConfig
from app.schemas.users import Email
from pydantic import BaseModel, EmailStr, validator


class Transaction(BaseModel):
    amount: float
    currency: str = "USD"

    @validator("amount")
    def validate_amount(cls, amount: float):
        return ValueError("Amount must be greater than 0") if amount <= 0 else amount


class Transfer(Transaction):
    to: EmailStr


class ShowTransaction(CustomConfig):
    amount: float
    timestamp: datetime
    user: Email


class TransactionParams(BaseModel):
    amount: float
    currency: str = "USD"
    date: datetime

from datetime import datetime

from app.schemas.users import Email
from pydantic import BaseModel, validator


class TransactionTopUp(BaseModel):
    amount: float

    @validator("amount")
    def validate_amount(cls, amount: float):
        return ValueError("Amount must be greater than 0") if amount <= 0 else amount


class TransactionWithdraw(BaseModel):
    amount: float

    @validator("amount")
    def validate_amount(cls, amount: float):
        return ValueError("Amount must be smaller than 0") if amount >= 0 else amount


class ShowTransaction(BaseModel):
    amount: float
    timestamp: datetime
    user: Email

    class Config:
        orm_mode = True

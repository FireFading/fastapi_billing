import uuid

from pydantic import BaseModel


class Transaction(BaseModel):
    amount: float


class Balance(BaseModel):
    user_id: uuid.UUID

from pydantic import BaseModel
import uuid

class Transaction(BaseModel):
    amount: float


class Balance(BaseModel):
    user_id: uuid.UUID

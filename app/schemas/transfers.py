from pydantic import BaseModel


class Transfer(BaseModel):
    to: str
    amount: float

from app.schemas.base import CustomConfig
from pydantic import BaseModel


class Balance(CustomConfig):
    deposit: float
    currency: str = "USD"


class CreateBalance(BaseModel):
    currency: str = "USD"

from pydantic import BaseModel


class Balance(BaseModel):
    deposit: float
    currency: str = "USD"

    class Config:
        orm_mode = True


class CreateBalance(BaseModel):
    currency: str = "USD"

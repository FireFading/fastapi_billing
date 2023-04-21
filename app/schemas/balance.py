from pydantic import BaseModel


class Balance(BaseModel):
    deposit: float

    class Config:
        orm_mode = True

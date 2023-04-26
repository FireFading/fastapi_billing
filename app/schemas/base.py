from pydantic import BaseModel


class CustomConfig(BaseModel):
    class Config:
        orm_mode = True

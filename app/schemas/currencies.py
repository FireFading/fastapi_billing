from pydantic import BaseModel


class Currency(BaseModel):
    name: str
    full_name: str
    symbol: str | None = None

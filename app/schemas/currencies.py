from datetime import datetime

from pydantic import BaseModel


class Currency(BaseModel):
    name: str
    full_name: str
    symbol: str | None = None


class TimeParams(BaseModel):
    start_time: datetime | None = None
    end_time: datetime = datetime.now()

from datetime import datetime

from pydantic import BaseModel


class Entry(BaseModel):
    source: str
    dt: datetime
    relevant_period: str
    title: str
    url: str


__all__ = ["Entry"]

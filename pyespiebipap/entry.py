from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel


class Entry(BaseModel):
    source: str
    ts: datetime
    period: Any
    title: str
    url: str


__all__ = ["Entry"]

from datetime import datetime
from typing import Any

from pydantic import BaseModel

__all__ = ["Entry"]


class Entry(BaseModel):
    source: str
    ts: datetime
    period: Any
    title: str
    url: str

from pydantic import Field

from src.domain.entities.base import Entity


class TickerData(Entity):
    name: str = Field(..., min_length=1)
    price: float
    timestamp: int

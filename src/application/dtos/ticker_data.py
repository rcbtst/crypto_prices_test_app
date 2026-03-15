from pydantic import BaseModel


class TickerDataDTO(BaseModel):
    name: str
    price: float
    timestamp: int

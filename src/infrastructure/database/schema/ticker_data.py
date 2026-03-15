from uuid import UUID, uuid4

from sqlalchemy import Uuid
from sqlalchemy.orm import Mapped, mapped_column

from src.infrastructure.database.schema.base import Base


class TickerData(Base):
    __tablename__ = "tickers_data"

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid4)
    name: Mapped[str]
    price: Mapped[float]
    timestamp: Mapped[int]

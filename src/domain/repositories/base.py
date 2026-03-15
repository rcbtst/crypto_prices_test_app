from abc import ABC, abstractmethod
from typing import Generic, TypeVar

T = TypeVar("T")


class IRepository(Generic[T], ABC):
    @abstractmethod
    async def save(self, obj: T) -> None:
        """Persist/update entity"""
        pass

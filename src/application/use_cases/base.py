from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from pydantic import BaseModel

CommandType = TypeVar("CommandType", bound=BaseModel)
ResultType = TypeVar("ResultType", bound=BaseModel)


class IUseCase(Generic[CommandType, ResultType], ABC):
    async def __call__(self, command: CommandType) -> ResultType:
        return await self.execute(command)

    @abstractmethod
    async def execute(self, command: CommandType) -> ResultType:
        pass

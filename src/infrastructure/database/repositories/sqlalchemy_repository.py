from typing import Generic, Type, TypeVar

from sqlalchemy.ext.asyncio import AsyncSession

from src.application.ports import ILogger
from src.domain.repositories.base import IRepository
from src.infrastructure.database.mappers.base import IDBMapper

DomainObject = TypeVar("DomainObject")
ORMObject = TypeVar("ORMObject")


class SQLAlchemyRepository(Generic[ORMObject, DomainObject], IRepository[DomainObject]):
    def __init__(
        self,
        session: AsyncSession,
        mapper: IDBMapper[DomainObject, ORMObject],
        model: Type[ORMObject],
        logger: ILogger,
    ):
        self.session = session
        self.mapper = mapper
        self.model = model
        self._logger = logger.with_name(__name__)

    async def save(self, obj: DomainObject) -> None:
        logger = self._logger.with_context({"model": self.model.__name__})

        logger.debug("Saving object to db")
        try:
            orm_obj = self.mapper.to_orm(obj)
            await self.session.merge(orm_obj)
            await self.session.flush()
            logger.info("Object saved to db")
        except Exception:
            logger.exception("Failed to save object to db")
            raise

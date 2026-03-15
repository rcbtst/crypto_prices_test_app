from src.domain.entities import TickerData as TickerDataDomain
from src.infrastructure.database.mappers.base import IDBMapper
from src.infrastructure.database.schema import TickerData as TickerDataORM


class SQLAlchemyTickerDataMapper(IDBMapper[TickerDataDomain, TickerDataORM]):
    def to_orm(self, domain_obj: TickerDataDomain) -> TickerDataORM:
        return TickerDataORM(
            id=domain_obj.id,
            name=domain_obj.name,
            price=domain_obj.price,
            timestamp=domain_obj.timestamp,
        )

    def to_domain(self, orm_obj: TickerDataORM) -> TickerDataDomain:
        return TickerDataDomain(
            id=orm_obj.id,
            name=orm_obj.name,
            price=orm_obj.price,
            timestamp=orm_obj.timestamp,
        )

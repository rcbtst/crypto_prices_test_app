from abc import ABC, abstractmethod
from typing import Generic, TypeVar

DomainObject = TypeVar("DomainObject")
ORMObject = TypeVar("ORMObject")


class IDBMapper(ABC, Generic[DomainObject, ORMObject]):
    @abstractmethod
    def to_orm(self, domain_obj: DomainObject) -> ORMObject:
        """
        Map a domain object to an ORM object
        """
        pass

    @abstractmethod
    def to_domain(self, orm_obj: ORMObject) -> DomainObject:
        """
        Map an ORM object to a domain object
        """
        pass

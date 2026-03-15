from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class Entity(BaseModel):
    id: UUID = Field(default_factory=uuid4)

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Entity) and self.id == other.id

    def __hash__(self) -> int:
        return hash(self.id)

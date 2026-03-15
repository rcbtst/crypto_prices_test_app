from uuid import UUID, uuid4

import pytest
from pydantic import ValidationError

from src.domain.entities.base import Entity


class TestEntity:
    def test_create_entity(self):
        test_entity = Entity()

        assert test_entity.id is not None
        assert isinstance(test_entity.id, UUID)

    def test_entity_correct_custom_id(self):
        custom_id = uuid4()
        test_entity = Entity(id=custom_id)

        assert test_entity.id == custom_id
        assert isinstance(test_entity.id, UUID)

    def test_entity_incorrect_custom_id(self):
        with pytest.raises(ValidationError):
            Entity.model_validate({"id": "test"})

    def test_entity_equality(self):
        entity_id = uuid4()
        entity1 = Entity(id=entity_id)
        entity2 = Entity(id=entity_id)
        entity3 = Entity()

        assert entity1 == entity2
        assert entity1 != entity3
        assert entity2 != entity3

    def test_entity_hash(self):
        entity_id = uuid4()
        entity1 = Entity(id=entity_id)
        entity2 = Entity(id=entity_id)
        entity3 = Entity()

        assert hash(entity1) == hash(entity2)
        assert hash(entity1) == hash(entity_id)
        assert hash(entity1) != hash(entity3)
        assert hash(entity2) != hash(entity3)

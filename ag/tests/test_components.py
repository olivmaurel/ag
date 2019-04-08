import pytest
from ag.factory import RecipeBook
from ag.components import *


class TestComponents(object):

    @pytest.fixture
    def recipe(self):
        return RecipeBook()

    @pytest.fixture
    def entity(self):
        return Entity('e')

    def test_component_becomes_attr(self, recipe, entity):

        recipe.attach(entity, 'health')
        assert hasattr(entity, 'health')
        assert entity.health.entity == entity

    def test_component_becomes_attr_no_factory(self, entity):

        entity.health = Health(entity)
        assert hasattr(entity, 'health')
        assert entity.health.entity == entity

    def test_position(self, recipe, entity):

        recipe.attach(entity, 'geo', pos=(0, 0))
        assert entity.geo.entity == entity
        assert entity.pos == (0, 0)

    def test_container_custom_units(self, recipe):

        e = recipe.entity('e', components=[{'liquidcontainer': {'unit': 'litre', 'size': 5}}])
        assert e.liquidcontainer.unit == 'litre'

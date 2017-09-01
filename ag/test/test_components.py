import pytest
from ag.ECS import Entity
from ag.Factory import Factory
from ag.components import *

class TestComponents(object):

    @pytest.fixture
    def factory(self):
        return Factory()

    @pytest.fixture
    def e(self):
        return Entity('e')

    def test_component_becomes_attr(self, factory, e):

        factory.assign_component(e, 'health')
        assert hasattr(e, 'health')
        assert e.health.entity == e

    def test_component_becomes_attr_no_factory(self, e):

        e.health = Health(e)
        assert hasattr(e, 'health')
        assert e.health.entity == e

    def test_position(self, factory, e):

        factory.assign_component(e, 'position', coords=(0, 0))
        assert e.position.entity == e
        assert e.position.coords == (0, 0)
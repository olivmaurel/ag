import pytest
from ag.factory import Factory
from ag.components import *


class TestArea(object):

    @pytest.fixture
    def factory(self):
        return Factory()

    @pytest.fixture
    def entity(self):
        return Entity('e')

    @pytest.fixture
    def plains(self, factory):

        return factory.area_creation(pos=(4, 2),
                                     name="Some plains",
                                     terrain='plains',
                                     climate='continental')
    @pytest.fixture
    def island(self, factory):

        return factory.area_creation(pos=(1, 2),
                                       name="Nice Island",
                                       terrain='island',
                                       climate='tropical')
    @pytest.fixture
    def location(self, factory):

        return factory.location_creation('river', (1, 2))

    @pytest.fixture
    def world(self, factory):

        return factory.world_system_creation('world')

    def test_create_area(self, factory):

        island = factory.area_creation(pos=(1, 2),
                                       name="Nice Island",
                                       terrain='island',
                                       climate='tropical')
        assert island.terrain.type == 'island'
        assert "<Nice Island" in island.name
        assert island.climate.type == 'tropical'

    def test_basic(self):
        assert 2 == 2

    def test_assign_area_to_entity(self, factory, entity, plains):

        factory.assign_component(entity, 'geo')
        factory.assign_component(entity, 'mov')
        assert entity.geo.pos == (0, 0)
        entity.enter_area(plains, (0, 0))

    def test_geo(self, factory, entity, plains):

        factory.assign_component(entity, 'geo')
        factory.assign_component(entity, 'mov')
        entity.enter_area(plains, (0, 0))
        assert entity.area == plains
        assert entity.area.pos == (4, 2)
        assert entity in plains.map[(0, 0)].entities

    def test_location_creation(self, factory, plains):

        river = factory.location_creation('river', (1, 1), plains)
        assert plains.map[(1, 1)] == river

    def test_active_area_and_inactive_area_update(self, factory, world, plains, island):
        pass

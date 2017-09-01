import pytest
from ag.ECS import Entity
from ag.Factory import Factory
from ag.components import *


class TestArea(object):

    @pytest.fixture
    def factory(self):
        return Factory()

    @pytest.fixture
    def e(self):
        return Entity('e')

    @pytest.fixture
    def area(self, factory):

        return factory.make_area(geo={'area': (1, 2), 'local': (0, 0)},
                                 terrain='plaines',
                                 climate='continental')

    def test_create_area(self, factory):

        island = factory.make_area(geo={'coords': {'area': (1, 2), 'local': (0, 0)}},
                                   terrain='island',
                                   climate='tropical')
        assert island.terrain.type == 'island'
        assert "<Area (1, 2):island/tropical" in island.name

    def test_assign_area_to_entity(self, factory, e, area):

        factory.assign_component(e, 'position')
        assert e.position.coords == (0, 0)
        e.enter_area(e, area)

    def test_geo(self, factory, e, area):

        factory.assign_component(e, 'geo')
        e.enter_area(e, area)
        assert e.area_coords == area.coords
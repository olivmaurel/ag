import pytest
from ag.factory import Factory
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

        return factory.area_creation(pos=(4, 2),
                                     name="Some plains",
                                     terrain='plains',
                                     climate='continental')

    def test_create_area(self, factory):

        island = factory.area_creation(pos=(1, 2),
                                       name="Nice Island",
                                       terrain='island',
                                       climate='tropical')
        assert island.terrain.type == 'island'
        assert "<Nice Island" in island.name
        assert island.climate.type == 'tropical'

    def test_assign_area_to_entity(self, factory, e, area):

        factory.assign_component(e, 'geo')
        assert e.geo.loc == (0, 0)
        e.enter_area(area)

    def test_geo(self, factory, e, area):

        factory.assign_component(e, 'geo')
        e.enter_area(area)
        assert e.area == area
        assert e.area.pos == (4, 2)
        assert e in area.entities

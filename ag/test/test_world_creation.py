import pytest
from ag.ECS import Entity
from ag.factory import Factory
from ag.components import *
from ag.systems import *

class TestWorldCreation(object):

    @pytest.fixture
    def factory(self):
        return Factory()

    @pytest.fixture
    def island(self, factory):

        return factory.area_creation(pos=(1, 2),
                                       name='Skull Island',
                                       terrain='island',
                                       climate='tropical')

    @pytest.fixture
    def world(self, factory):

        return factory.world_system_creation()

    def test_create_world_no_args(self):

        w = WorldSystem()
        assert(isinstance(w, System))
        assert hasattr(w, 'name')
        assert hasattr(w, 'map')

    def test_create_world_system(self, factory, world, island):

        world.set_active_area(island)

        for system in world.active_area.systems:
            if isinstance(system, BiologicalNeedsSystem):
                return True
        else:
            return False


    def test_set_active_area(self, factory, island, world):

        world.map[island.pos] = island
        world.set_active_area(island)

        assert world.active_area == island
        assert world.map[(0,0)] != island


    def test_100_turns_update(self, factory, island):

        albonpin = factory.human_creation('albonpin')
        skeleton = factory.entity_creation('skeleton', components=['health'])

        albonpin.enter_area(island, pos=(1, 1))
        skeleton.enter_area(island, pos=(1, 1))

        world = factory.world_system_creation()
        world.set_active_area(island)

        for i in range(100):
            world.update()

        assert albonpin.health.alive is False
        assert skeleton.health.alive is True
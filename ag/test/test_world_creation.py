import pytest
from ag.ECS import Entity
from ag.factory import Factory
from ag.components import *
from ag.systems import *

class TestWorldCreation(object):

    @pytest.fixture
    def factory(self):
        return Factory()

    def test_create_world_no_args(self):

        w = WorldSystem()
        assert(isinstance(w, System))
        assert hasattr(w, 'name')
        assert hasattr(w, '_map')

    def test_create_world_system(self, factory):

        world = factory.world_system_creation()
        bio_s = BiologicalNeedsSystem()
        active_area = world.active_area
        world.add_system(world.active_coords, bio_s)
        assert isinstance(active_area.systems[0], BiologicalNeedsSystem)

    def test_100_turns_update(self, factory):

        albonpin = factory.human_creation('albonpin')
        skeleton = factory.entity_creation('skeleton', components=['health'])

        world = factory.world_system_creation()

        bio_s = BiologicalNeedsSystem()
        world.add_system(world.active_coords, bio_s)

        a = world.active_area
        for i in range(100):
            for sys in a.systems:
                sys.update()

        assert albonpin.health.alive is False
        assert skeleton.health.alive is True
from ag.ECS import System
from ag.systems.needs import NeedsSystem
from ag.systems.world import WorldSystem
from ag.tests.base_tests import BaseTest


class TestWorldCreation(BaseTest):

    def test_create_world_no_args(self):

        w = WorldSystem()
        assert (isinstance(w, System))
        assert hasattr(w, 'name')
        assert hasattr(w, 'map')

    def test_create_world_system(self, world, island):

        world.set_active_area(island)

        for system in world.active_area.systems:
            if isinstance(system, NeedsSystem):
                return True
        else:
            return False

    def test_set_active_area(self, world, island):

        world.map[island.pos] = island
        world.set_active_area(island)

        assert world.active_area == island
        assert world.map[(0, 0)] != island

    def test_100_turns_update(self, recipe, island, world):

        albonpin = recipe.human('albonpin')
        skeleton = recipe.entity('skeleton', components=['health', 'mov'])

        world.set_active_area(island)

        albonpin.enter_area(island, pos=(1, 1))
        skeleton.enter_area(island, pos=(1, 1))

        for i in range(100):
            world.update()

        assert albonpin.health.alive is False
        assert skeleton.health.alive is True

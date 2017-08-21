import pytest
from ag.ECS import Entity
from ag.Factory import GameObjectFactory
from ag.components import *
from ag.World import World
from ag.systems import *

class TestWorldCreation(object):

    @pytest.fixture
    def factory(self):
        return GameObjectFactory()

    def test_instantiate_world(self, factory):
        x_size, y_size = 4, 4
        w = factory.make_world('world', x_size, y_size)
        assert isinstance(w, World)
        assert isinstance(w, Entity)
        assert isinstance(w.map, Map)
        assert len(w.map.grid) == x_size*y_size
        assert hasattr(w, 'name')

    def test_create_world_no_args(self):

        w = World()
        assert hasattr(w, 'name')
        assert hasattr(w, 'uid')

    def test_create_world_system(self, factory):

        world = factory.make_world_sytem()
        bio_s = BiologicalNeedsSystem()
        world.add_system(bio_s)
        assert hasattr(world, 'biological_needs_system')

# w.add_system(BiologicalNeedsSystem())
#
# player = factory.make_human('player')
# skeleton = factory.make_object('skeleton', components=[Health()])
#
# active_area = w.map.grid[(0,0)][0]
#
# for i in range(100):
#     w.active_area.update()
#     if not player.health.alive:
#         break
#
# print(player.health.current)
# print(player.hunger.status)
# print(player.thirst.status)
# print(player.health.alive)

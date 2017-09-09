import pytest
from ag.ECS import Entity
from ag.factory import Factory
from ag.components import *

class TestInventory(object):

    @pytest.fixture
    def factory(self):
        return Factory()

    @pytest.fixture
    def e(self):
        return Entity('e')

    def test_pickup_item(self, e, factory):

        e.inv = Inv(e)
        bottle = factory.item_creation('container', 'bottle')
        e.pickup(bottle)
        assert e.inv.space_left == e.inv.capacity - bottle.size

    def test_drop_item(self, e, factory):

        e.inv = Inv(e)
        bottle = factory.item_creation('container', 'bottle')
        e.pickup(bottle)
        e.drop(bottle)
        assert e.inv.space_left == e.inv.capacity

    def test_pickup_move_update_itemgeo(self, Battleflip, factory):

        Battleflip.inv = Inv(Battleflip)
        Battleflip.geo = Geo(Battleflip)
        Battleflip.mov = Mov(Battleflip)
        Battleflip.moveto((0, 0))
        bottle = factory.item_creation('container', 'bottle')
        Battleflip.pickup(bottle)
        Battleflip.moveto((1, 1))
        assert bottle.pos == (1, 1)

    def test_cant_pickup_in_different_pos(self, Battleflip, factory):

        Battleflip.inv = Inv(Battleflip)
        Battleflip.moveto((0, 0))
        bottle = factory.item_creation('container', 'bottle')
        bottle.pos((1, 1))

        assert Battleflip.pickup(bottle) == False
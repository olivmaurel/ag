import pytest
from ag.ECS import Entity
from ag.factory import Factory
from ag.components import *

class TestInventory(object):

    @pytest.fixture
    def factory(self):
        return Factory()

    @pytest.fixture
    def e(self, factory):
        e = Entity('e')
        factory.assign_components(e, ['inv', 'mov', 'geo'])
        return e

    def test_pickup_item(self, e, factory):

        bottle = factory.item_creation('container', 'bottle')
        e.pickup(bottle)
        assert e.inv.space_left == e.inv.capacity - bottle.size

    def test_drop_item(self, e, factory):

        bottle = factory.item_creation('container', 'bottle')
        e.pickup(bottle)
        e.drop(bottle)
        assert e.inv.space_left == e.inv.capacity

    def test_pickup_move_update_itemgeo(self, e, factory):

        e.moveto((0, 0))
        bottle = factory.item_creation('container', 'bottle')
        e.pickup(bottle)
        e.moveto((1, 1))

        assert bottle.pos == False
        assert bottle.area == False
        assert bottle.geo == False

    def test_cant_pickup_in_different_pos(self, e, factory):

        e.moveto((0, 0))
        bottle = factory.item_creation('container', 'bottle')
        bottle.pos = (1, 1)
        assert e.pickup(bottle) == False

    def test_drop_then_move(self, e, factory):

        e.moveto((0, 0))
        bottle = factory.item_creation('container', 'bottle')
        e.pickup(bottle)
        e.moveto((1, 1))
        e.drop(bottle)
        e.moveto((2, 2))

        assert bottle.pos == (1, 1)

    def test_create_item_twice(self, factory):

        firstpouch = factory.item_creation('container', 'pouch')
        secondpouch = factory.item_creation('container', 'pouch')

        assert isinstance (firstpouch, Entity)
        assert firstpouch != secondpouch
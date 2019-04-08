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
        assert bottle.carriable is not False
        assert e.pickup(bottle) is not False
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

        assert bottle.pos is False
        assert bottle.area is False
        assert bottle.geo is False

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

        assert isinstance(firstpouch, Entity)
        assert isinstance(secondpouch, Entity)
        assert firstpouch != secondpouch

    def test_fill_one_the_other_is_empty(self, factory):

        firstpouch = factory.item_creation('container', 'pouch')
        secondpouch = factory.item_creation('container', 'pouch')
        water = factory.item_creation('liquid', 'water')
        firstpouch.fill(water)

        assert firstpouch.is_full()
        assert firstpouch.liquidcontainer.is_full()
        assert firstpouch.get_status() == ContainerStatus.full

        assert secondpouch.is_empty()
        assert secondpouch.liquidcontainer.is_empty()
        assert secondpouch.get_status() == ContainerStatus.empty


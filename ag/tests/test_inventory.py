import pytest

from ag.factory import RecipeBook
from ag.components import *

class TestInventory(object):

    @pytest.fixture
    def recipe(self):
        return RecipeBook()

    @pytest.fixture
    def entity(self, recipe):
        e = Entity('e')
        recipe.attach(e, ['inv', 'mov', 'geo'])
        return e

    @pytest.fixture
    def bottle(self, recipe):
        return recipe.container('bottle')

    def test_pickup_item(self, entity, bottle):

        assert bottle.carriable is not False
        assert entity.pickup(bottle) is not False
        assert entity.inv.space_left == entity.inv.capacity - bottle.size

    def test_drop_item(self, entity, recipe, bottle):

        entity.pickup(bottle)
        entity.drop(bottle)
        assert entity.inv.space_left == entity.inv.capacity

    def test_pickup_move_update_itemgeo(self, entity, bottle):

        entity.moveto((0, 0))
        entity.pickup(bottle)
        entity.moveto((1, 1))

        assert bottle.pos is False
        assert bottle.area is False
        assert bottle.geo is False

    def test_cant_pickup_in_different_pos(self, entity, bottle):

        entity.moveto((0, 0))
        bottle.pos = (1, 1)
        assert entity.pickup(bottle) is False

    def test_drop_then_move(self, entity, recipe, bottle):

        entity.moveto((0, 0))
        entity.pickup(bottle)
        entity.moveto((1, 1))
        entity.drop(bottle)
        entity.moveto((2, 2))

        assert bottle.pos == (1, 1)

    def test_create_item_twice(self, recipe):

        firstpouch = recipe.container('pouch')
        secondpouch = recipe.container('pouch')

        assert isinstance(firstpouch, Entity)
        assert isinstance(secondpouch, Entity)
        assert firstpouch != secondpouch

    def test_fill_one_the_other_is_empty(self, recipe):

        firstpouch = recipe.container('pouch')
        secondpouch = recipe.container('pouch')
        water = recipe.liquid('water')
        firstpouch.fill(water)

        assert firstpouch.is_full()
        assert firstpouch.liquidcontainer.is_full()
        assert firstpouch.get_status() == ContainerStatus.full

        assert secondpouch.is_empty()
        assert secondpouch.liquidcontainer.is_empty()
        assert secondpouch.get_status() == ContainerStatus.empty


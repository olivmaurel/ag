import pytest

from ag.exceptions.exceptions import *
from ag.factory import Factory
from ag.systems import *


class TestNeeds(object):

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

    @pytest.fixture
    def water(self, island, factory):
        return factory.item_creation('liquid', 'water', area=island, pos=(1, 2))

    @pytest.fixture
    def oil(self, island, factory):
        return factory.item_creation('liquid', 'oil', area=island, pos=(1, 2))

    @pytest.fixture
    def human(self, island, factory):
        human = factory.human_creation('human')
        human.enter_area(island, pos=(1, 1))

        return human

    def get_bottle_and_drink(self, character, bottle):

        character.moveto(bottle.pos)
        character.pickup(bottle)
        character.do_drink(bottle)

    def test_human_gets_thirsty(self, world, island, human):

        world.set_active_area(island)

        for i in range(10):
            world.update()

        assert human.conditions is not False
        assert 'thirsty' in human.conditions

    def test_drink(self, factory, water, world, island, human):
        world.set_active_area(island)
        bottle = factory.item_creation('container', 'bottle', area=island, pos=(1, 2))
        for i in range(10):
            world.update()

        assert human.conditions is not False
        assert 'thirsty' in human.conditions

        bottle.fill(water)
        assert bottle.is_full()

        self.get_bottle_and_drink(human, bottle)

        assert 'thirsty' not in human.conditions

    def test_drink_wait_fill_and_drink_again(self, factory, water, world, island, human):

        bottle = factory.item_creation('container', 'bottle', area=island, pos=(1, 2))
        world.set_active_area(island)

        for i in range(10):
            world.update()

        assert human.conditions is not False
        assert 'thirsty' in human.conditions

        bottle.fill(water)
        self.get_bottle_and_drink(human, bottle)

        assert 'thirsty' not in human.conditions

        for i in range(11):
            world.update()

        assert 'thirsty' in human.conditions

        bottle.fill(water)
        self.get_bottle_and_drink(human, bottle)

        assert 'thirsty' not in human.conditions

    def test_drink_empty_bottle_still_thirsty(self, factory, world, island, human):

        world.set_active_area(island)
        bottle = factory.item_creation('container', 'bottle', area=island, pos=(1, 2))

        for i in range(10):
            world.update()

        assert human.conditions is not False
        assert 'thirsty' in human.conditions
        assert bottle.is_empty()

        with pytest.raises(NoSuchComponentException):
            self.get_bottle_and_drink(human, bottle)

        assert 'thirsty' in human.conditions

    def test_drink_oil_still_thirsty(self, world, island, human, factory, oil):

        world.set_active_area(island)
        bottle = factory.item_creation('container', 'bottle', area=island, pos=(1, 2))

        for i in range(10):
            world.update()

        assert human.conditions is not False
        assert 'thirsty' in human.conditions

        bottle.fill(oil)

        with pytest.raises(NoSuchComponentException):
            self.get_bottle_and_drink(human, bottle)

        assert 'thirsty' in human.conditions

    def test_fill_water_then_oil(self, factory, world, island, human, oil, water):

        world.set_active_area(island)

        for i in range(10):
            world.update()

        assert human.conditions is not False
        assert 'thirsty' in human.conditions

        bottle = factory.item_creation('container', 'bottle', area=island, pos=(1, 2))
        bottle.fill(water)
        with pytest.raises(MixedLiquidsException):
            bottle.fill(oil)

    def test_two_for_one_bottle(self, factory, world, island, water):

        human = factory.human_creation('human')
        human.enter_area(island, pos=(1, 1))
        other = factory.human_creation('other')
        other.enter_area(island, pos=(1, 1))
        bottle = factory.item_creation('container', 'bottle', area=island, pos=(1, 2))

        world.set_active_area(island)

        for i in range(10):
            world.update()

        assert human.conditions is not False
        assert 'thirsty' in human.conditions
        assert 'thirsty' in other.conditions

        bottle.fill(water)

        assert bottle.is_full()

        self.get_bottle_and_drink(human, bottle)

        assert 'thirsty' not in human.conditions
        assert 'thirsty' in other.conditions

        assert bottle.is_empty()

        with pytest.raises(EmptyContainerException):
            self.get_bottle_and_drink(other, bottle)

        assert other.conditions is not False
        assert 'thirsty' in other.conditions

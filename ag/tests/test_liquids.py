import pytest
from ag.exceptions.exceptions import *
from ag.tests.base_tests import BaseTest


class TestLiquids(BaseTest):

    @staticmethod
    def get_bottle_and_drink(character, bottle):

        character.moveto(bottle.pos)
        character.pickup(bottle)
        character.do_drink(bottle)

    def test_human_gets_thirsty(self, world, island, human):

        world.set_active_area(island)
        human.enter_area(island, pos=(1, 1))

        for i in range(10):
            world.update()

        assert human.conditions is not False
        assert 'thirsty' in human.conditions

    def test_drink_not_possible_if_different_pos(self, water, world, island, human, recipe):
        world.set_active_area(island)

        for i in range(10):
            world.update()

        assert human.conditions is not False
        assert 'thirsty' in human.conditions

        human.moveto((1, 1))
        bottle = recipe.container('bottle', area=island, pos=(2, 2))
        water = recipe.liquid('water', area=island, pos=(2, 2))
        bottle.fill(water)
        assert bottle.is_full()

        with pytest.raises(DifferentPositionException):
            human.do_drink(bottle)

    def test_filling_bottle_not_possible_if_different_pos(self, recipe, island):

        bottle = recipe.container('bottle', area=island, pos=(2, 2))
        water = recipe.liquid('water', area=island, pos=(2, 3))
        with pytest.raises(DifferentPositionException):
            bottle.fill(water)

    def test_drink(self, world, island, human, recipe):
        world.set_active_area(island)

        for i in range(10):
            world.update()

        assert human.conditions is not False
        assert 'thirsty' in human.conditions

        bottle = recipe.container('bottle', area=island, pos=(2, 2))
        water = recipe.liquid('water', area=island, pos=(2, 2))
        bottle.fill(water)
        assert bottle.is_full()

        self.get_bottle_and_drink(human, bottle)

        assert 'thirsty' not in human.conditions
    #
    # def test_drink_wait_fill_and_drink_again(self, water, world, island, human, bottle):
    #
    #     world.set_active_area(island)
    #
    #     for i in range(10):
    #         world.update()
    #
    #     assert human.conditions is not False
    #     assert 'thirsty' in human.conditions
    #
    #     bottle.fill(water)
    #     self.get_bottle_and_drink(human, bottle)
    #
    #     assert 'thirsty' not in human.conditions
    #
    #     for i in range(11):
    #         world.update()
    #
    #     assert 'thirsty' in human.conditions
    #
    #     bottle.fill(water)
    #     self.get_bottle_and_drink(human, bottle)
    #
    #     assert 'thirsty' not in human.conditions

    def test_drink_empty_bottle_still_thirsty(self, world, island, human, bottle):

        world.set_active_area(island)

        for i in range(10):
            world.update()

        assert human.conditions is not False
        assert 'thirsty' in human.conditions
        assert bottle.is_empty()

        with pytest.raises(EmptyContainerException):
            self.get_bottle_and_drink(human, bottle)

        assert 'thirsty' in human.conditions

    def test_drink_oil_still_thirsty(self, world, island, human, oil, bottle):

        world.set_active_area(island)

        for i in range(10):
            world.update()

        assert human.conditions is not False
        assert 'thirsty' in human.conditions

        bottle.fill(oil)

        with pytest.raises(NoSuchPropertyException):
            self.get_bottle_and_drink(human, bottle)

        assert 'thirsty' in human.conditions
        assert bottle.empty is False
    #
    #
    # def test_fill_water_then_oil(self, factory, world, island, human, oil, water, bottle):
    #
    #     world.set_active_area(island)
    #
    #     for i in range(10):
    #         world.update()
    #
    #     assert human.conditions is not False
    #     assert 'thirsty' in human.conditions
    #
    #     bottle.fill(water)
    #     with pytest.raises(MixedLiquidsException):
    #         bottle.fill(oil)

    def test_two_for_one_bottle(self, recipe, world, island, water):

        human = recipe.human('foo')
        human.enter_area(island, pos=(1, 1))
        other = recipe.human('bar')
        other.enter_area(island, pos=(1, 1))
        bottle = recipe.container('bottle', area=island, pos=(1, 2))

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

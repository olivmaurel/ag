from ag.tests.base_tests import BaseTest
from ag.constants import Conditions as C


class TestNeeds(BaseTest):

    def test_human_wants_to_drink(self, recipe, world, island):
        #  after 10 turns, human should get thirsty
        #  he should do nothing until he gets thirsty
        # when thirsty, he should look around for a drink
        human = recipe.human('human')
        human.enter_area(island, pos=(2, 2))
        world.set_active_area(island)
        for i in range(10):
            world.update()

        assert human.conditions is not False
        assert C.thirsty in human.conditions
        assert C.hungry in human.conditions

        bottle = recipe.container('bottle', area=island, pos=(2, 2))

        bottle.fill(recipe.liquid('water', area=island, pos=(2, 2)))
        assert human.decide() == 'drink'
        human.do_drink(bottle)
        assert human.decide() == 'eat'

    def test_human_moves_to_drink_when_thirsty(self, world, island, human, recipe):
        world.set_active_area(island)
        human = recipe.human('human')
        human.enter_area(island, pos=(0, 2))

        for i in range(10):
            world.update()

        assert human.conditions is not False
        assert C.thirsty in human.conditions
        assert C.hungry in human.conditions

        bottle = recipe.container('bottle', area=island, pos=(2, 2))
        bottle.fill(recipe.liquid('water', area=island, pos=(2, 2)))
        assert human.decide() == 'drink'
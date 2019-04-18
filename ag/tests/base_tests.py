import pytest
from ag.factory import RecipeBook


class BaseTest(object):

    @pytest.fixture
    def recipe(self):
        return RecipeBook()

    @pytest.fixture
    def entity(self, recipe):
        return recipe.entity('e')

    @pytest.fixture
    def plains(self, recipe):
        return recipe.area(pos=(4, 2),
                           name="Some plains",
                           terrain='plains',
                           climate='continental')

    @pytest.fixture
    def island(self, recipe):
        return recipe.area(pos=(1, 2),
                           name='Skull Island',
                           terrain='island',
                           climate='tropical')

    @pytest.fixture
    def world(self, recipe):
        return recipe.world('new world')

    @pytest.fixture
    def water(self, island, recipe):
        return recipe.liquid('water', area=island, pos=(1, 2))

    @pytest.fixture
    def oil(self, island, recipe):
        return recipe.liquid('oil', area=island, pos=(1, 2))

    @pytest.fixture
    def bottle(self, island, recipe):
        return recipe.container('bottle', area=island, pos=(1, 2))

    @pytest.fixture
    def human(self, island, recipe):
        human = recipe.human('human')
        human.enter_area(island, pos=(1, 1))

        return human

    @pytest.fixture
    def location(self, recipe):

        return recipe.location('river', (1, 2))


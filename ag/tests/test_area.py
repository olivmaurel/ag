from ag.tests.base_tests import BaseTest


class TestArea(BaseTest):

    def test_create_area(self, recipe):

        island = recipe.area(pos=(1, 2),
                                       name="Nice Island",
                                       terrain='island',
                                       climate='tropical')
        assert island.terrain.type == 'island'
        assert "<Nice Island" in island.name
        assert island.climate.type == 'tropical'

    def test_assign_area_to_entity(self, recipe, entity, plains):

        recipe.attach(entity, 'geo')
        recipe.attach(entity, 'mov')
        assert entity.geo.pos == (0, 0)
        entity.enter_area(plains, (0, 0))

    def test_geo(self, recipe, entity, plains):

        recipe.attach(entity, 'geo')
        recipe.attach(entity, 'mov')
        entity.enter_area(plains, (0, 0))
        assert entity.area == plains
        assert entity.area.pos == (4, 2)
        assert entity in plains.map[(0, 0)].entities

    def test_location_creation(self, recipe, plains):

        river = recipe.location('river', (1, 1), plains)
        assert plains.map[(1, 1)] == river

    def test_active_area_and_inactive_area_update(self, recipe, world, plains, island):
        pass

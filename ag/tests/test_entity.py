import pytest
import uuid

from ag.factory import RecipeBook
from ag.components import *


class TestEntities(object):

    @pytest.fixture
    def recipe(self):
        return RecipeBook()

    def test_basic_entity(self):

        e = Entity()
        assert hasattr(e, 'name')
        assert hasattr(e, 'uid')
        assert type(e.uid) == uuid.UUID

    def test_create_entity_no_recipe_no_binding(self):
        skeleton = Entity('skeleton')
        skeleton.health = Health(skeleton)
        assert skeleton.health.entity == skeleton

    def test_create_entity_recipe(self, recipe):
        lowercase = recipe.entity('lowercase', components=['health'])
        assert lowercase.health.entity == lowercase
        capitalize = recipe.entity('capitalize', components=['Health'])
        assert capitalize.health.entity == capitalize
        in_dict_form = recipe.entity('in_dict_form', components=[{'Health': [100, 100]}])
        assert in_dict_form.health.entity == in_dict_form

    def test_create_two_entities_same_name(self, recipe):

        skeleton = recipe.entity('skeleton', components=['health'])
        skeletwo = recipe.entity('skeleton', components=['health'])
        assert skeleton == skeletwo

    def test_create_two_entities_same_name_binding_entity(self):

        skeleton = Entity('skeleton')
        skeleton.health = Health(skeleton)
        skeletwo = Entity('skeleton')
        skeletwo.health = Entity(skeletwo)
        assert skeleton == skeletwo

    def test_entities_must_be_different(self, recipe):

        skeleton = recipe.entity('skeleton', components=['health'])
        skeletwo = recipe.entity('skeletwo', components=['health'])
        assert skeleton != skeletwo

    def test_recreate_entity(self, recipe):

        first = recipe.entity('e')
        second = recipe.entity('e')
        assert first == second

    def test_recreate_entity_different_components(self, recipe):

        first = recipe.entity('e', components=[{'geo': {'pos': (0, 1)}}])
        second = recipe.entity('e', components=['Health'])
        assert 'position' not in second.components
        assert 'health' in first.components

    def test_linked_entity_is_same_as_self(self, recipe):

        e = recipe.entity('e', components=[{'geo': {'pos': (0, 1)}}])
        assert e == e.geo.entity
        assert e.pos is not False

    def test_entity_with_components_inherits_shared_functions(self, recipe):

        bottle = recipe.container('bottle')
        water = recipe.liquid('water')
        bottle.fill(water)

        # content is in the properties, water has been added to the component
        # the test fails if the entity properties are not synced with the component's
        liquid = bottle.content
        assert liquid.drinkable

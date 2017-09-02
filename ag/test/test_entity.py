import pytest
import uuid
from ag.ECS import Entity
from ag.Factory import Factory
from ag.components import *

class TestEntities(object):

    @pytest.fixture
    def factory(self):
        return Factory()

    def test_basic_entity(self):

        e = Entity()
        assert hasattr(e, 'name')
        assert hasattr(e, 'uid')
        assert type(e.uid) == uuid.UUID

    def test_create_entity_no_factory_no_binding(self):
        skeleton = Entity('skeleton')
        skeleton.health = Health(skeleton)
        assert skeleton.health.entity == skeleton

    def test_create_entity_factory(self, factory):
        lowercase = factory.entity('lowercase', components=['health'])
        assert lowercase.health.entity == lowercase
        capitalize = factory.entity('capitalize', components=['Health'])
        assert capitalize.health.entity == capitalize
        in_dict_form = factory.entity('in_dict_form', components=[{'Health': [100, 100]}])
        assert in_dict_form.health.entity == in_dict_form

    def test_create_two_entities_same_name(self,factory):

        skeleton = factory.entity('skeleton', components=['health'])
        skeletwo = factory.entity('skeleton', components=['health'])
        assert skeleton == skeletwo

    def test_create_two_entities_same_name_binding_entity(self):

        skeleton = Entity('skeleton')
        skeleton.health = Health(skeleton)
        skeletwo = Entity('skeleton')
        skeletwo.health = Entity(skeletwo)
        assert skeleton == skeletwo

    def test_entities_must_be_different(self, factory):

        skeleton = factory.entity('skeleton', components=['health'])
        skeletwo = factory.entity('skeletwo', components=['health'])
        assert skeleton != skeletwo

    def test_recreate_entity(self, factory):

        first = factory.entity('e')
        second = factory.entity('e')
        assert first == second

    def test_recreate_entity_different_components(self, factory):

        first = factory.entity('e', components=[{'Position': (0, 1)}])
        second = factory.entity('e', components=['Health'])

        assert 'position' not in second.components
        assert 'health' in first.components

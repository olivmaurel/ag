import pytest
import uuid
from ag.ECS import Entity
from ag.Factory import GameObjectFactory
from ag.components import *

class TestEntities(object):

    @pytest.fixture
    def factory(self):
        return GameObjectFactory()

    def test_basic_entity(self):

        e = Entity()
        assert hasattr(e, 'name')
        assert hasattr(e, 'uid')
        assert type(e.uid) == uuid.UUID

    def test_create_entity_no_factory_no_binding(self):
        skeleton = Entity('skeleton')
        skeleton.health = Health()
        assert skeleton.health.entity == skeleton

    def test_create_entity_factory(self, factory):
        lowercase = factory.make_object('lowercase', components=['health'])
        assert lowercase.health.entity == lowercase
        capitalize = factory.make_object('capitalize', components=['Health'])
        assert capitalize.health.entity == capitalize
        in_dict_form = factory.make_object('in_dict_form', components=[{'Health': [100, 100]}])
        assert in_dict_form.health.entity == in_dict_form

    def test_create_two_entities_same_name(self,factory):

        skeleton = factory.make_object('skeleton', components=['health'])
        skeletwo = factory.make_object('skeleton', components=['health'])
        assert skeleton == skeletwo

    def test_create_two_entities_same_name_binding_entity(self):

        skeleton = Entity('skeleton')
        skeleton.health = Health(skeleton)
        skeletwo = Entity('skeleton')
        skeletwo.health = Entity(skeletwo)
        assert skeleton == skeletwo

    def test_entities_must_be_different(self, factory):

        skeleton = factory.make_object('skeleton', components=['health'])
        skeletwo = factory.make_object('skeletwo', components=['health'])
        assert skeleton != skeletwo
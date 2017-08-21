import pytest
from ag.ECS import Entity
from ag.Factory import GameObjectFactory
from ag.components import *

class TestComponents(object):

    @pytest.fixture
    def factory(self):
        return GameObjectFactory()

    @pytest.fixture
    def player(self):
        return Entity('player')

    def test_component_becomes_attr(self, factory, player):

        factory.assign_component(player, 'health')
        assert hasattr(player, 'health')
        assert player.health.entity == player

    def test_component_becomes_attr_no_factory(self, player):

        player.health = Health()
        assert hasattr(player, 'health')
        assert player.health.entity == player
        

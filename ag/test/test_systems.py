import pytest
from ag.factory import Factory
from ag.systems import *


class TestSystems(object):

    @pytest.fixture
    def factory(self):
        return Factory()

    def test_create_system(self):

        s = System('test')
        assert s.name == 'test'

    def test_systems_catalog_updates(self):

        b = BiologicalNeedsSystem()
        w = WorldSystem()

        assert b != w
        assert len(b.Catalog) == 3

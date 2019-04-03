import pytest
from ag.factory import Factory
from ag.systems import *


class TestSystems(object):

    @pytest.fixture
    def factory(self):
        return Factory()

    def test_create_system(self):

        s = System('tests')
        assert s.name == 'tests'

    def test_systems_catalog_updates(self):

        b = BiologicalNeedsSystem()
        w = WorldSystem()

        assert b != w
        assert len(b.Catalog) == len(w.Catalog)

        assert 'tests' in b.Catalog
        assert 'world' in b.Catalog


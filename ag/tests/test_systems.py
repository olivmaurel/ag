import pytest

from ag.ECS import System
from ag.factory import Factory
from ag.systems.biological_needs import BiologicalNeedsSystem
from ag.systems.world import WorldSystem


class TestSystems(object):

    @pytest.fixture
    def factory(self):
        return Factory()

    def test_create_system(self):

        s = System('tests')
        assert s.name == 'tests'

    def test_systems_catalog_updates(self):

        b = BiologicalNeedsSystem()
        w = WorldSystem('world')

        system = System('new_system')

        assert b != w
        assert len(b.Catalog) == len(w.Catalog)

        assert system.name in b.Catalog
        assert w.name in b.Catalog


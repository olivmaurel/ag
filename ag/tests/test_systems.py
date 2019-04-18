from ag.ECS import System
from ag.systems.needs import NeedsSystem
from ag.systems.world import WorldSystem
from ag.tests.base_tests import BaseTest


class TestSystems(BaseTest):

    def test_create_system(self):

        s = System('tests')
        assert s.name == 'tests'

    def test_systems_catalog_updates(self):

        b = NeedsSystem()
        w = WorldSystem('world')

        system = System('new_system')

        assert b != w
        assert len(b.Catalog) == len(w.Catalog)

        assert system.name in b.Catalog
        assert w.name in b.Catalog


from collections import OrderedDict
from ag.ECS import Entity
import ag.components
from typing import Union, Tuple, List
from uuid import uuid4

from ag.systems.world import WorldSystem
from core import get_yaml_as_dict


class Factory(object):
    def __getattr__(self, item):

        if item not in self.__dict__:
            if 'ml_' in item:
                self.set_master_list(item)
                return super().__getattribute__(item)
            else:  # Normal behavior if not found
                raise AttributeError
        else:
            return self.item

    def set_master_list(self, listname):
        path = '../fixtures/master_lists/'
        y = get_yaml_as_dict('{}{}.yml'.format(path, listname))
        self.__setattr__(listname, y)

    def assign_components(self, e: Entity, components: List) -> None:

        for comp in components:
            self.assign_component(e, comp)

    def assign_component(self,
                         entity: Entity,
                         cname: str, *args, **kwargs) -> None:
        _c_class = getattr(ag.components, cname.capitalize())
        component = _c_class(entity, *args, **kwargs)
        entity.__setattr__(cname.lower(), component)

    def entity_creation(self, entity: Union[str, Entity], components: list = None, uid: uuid4() = None) -> Entity:

        if isinstance(entity, str):
            entity = Entity(entity, uid)
        if components:
            for component in components:
                if isinstance(component, dict):
                    for key, value, in component.items():
                        if isinstance(value, dict):
                            self.assign_component(entity, key, **value)
                        else:
                            self.assign_component(entity, key, *value)
                else:
                    self.assign_component(entity, component)

        return entity

    def human_creation(self, name: str, uid: str = None):

        e = Entity(name, uid)
        components = ['health', 'hunger', 'geo', 'thirst', 'mov', 'inv']

        return self.entity_creation(e, components)

    def area_creation(self,
                      name: Union[uuid4, str],
                      pos: Tuple[int, int],
                      terrain: str,
                      climate: str,
                      components: list = None,
                      uid: uuid4() = None,
                      map_dimensions: Tuple[int, int] = (10, 10)) -> Entity:

        name = ('<{} {}:{}/{}>'.format(name, pos, terrain, climate))
        components = components or []
        components.extend(['updater',
                           {'terrain': [terrain]},
                           {'climate': [climate]}])
        area = self.entity_creation(name, components, uid)
        area.__setattr__('pos', pos if isinstance(pos, tuple) else None)
        area.__setattr__('systems', [])
        area.__setattr__('map', OrderedDict())

        for x in range(map_dimensions[0]):
            for y in range(map_dimensions[1]):
                loc_name = "location {}".format(map_dimensions)
                location = self.entity_creation(loc_name)
                location.__setattr__('area', area)
                location.__setattr__('entities', [])
                area.map[(x, y)] = location

        return area

    def item_creation(self, reftype: str, name: str, components: List = None, **kwargs) -> Entity:

        components = components or []
        components.append('geo')

        item = self.create_from_masterlist(reftype, name, components)

        for key, value in kwargs.items():
            item.__setattr__(key, value)
        return item

    def create_from_masterlist(self, reftype: str, name: str, components: List = None):

        try:
            ml_ref = self.__getattr__('ml_{}'.format(reftype))[name]
        except AttributeError:
            ml_ref = self.__getattribute__('ml_{}'.format(reftype))[name]
        if not ml_ref:
            raise NotImplementedError('{} - {} is not in the master lists files.'.format(reftype, name))

        uid = uuid4()
        name = "{}-{}".format(name, uid)
        components = components or []

        if 'traits' in ml_ref:
            components.extend(ml_ref['traits'])

        entity = self.entity_creation(name, components, uid)

        for key, value in ml_ref.items():
            if not hasattr(entity, key) or entity.key is False:
                entity.__setattr__(key, value)

        return entity

    def location_creation(self, name: str, pos: Tuple[int, int], area: Entity, components: List = None):

        components = components or []
        location = self.create_from_masterlist('location', name, components)
        area.map[pos] = location
        return location

    def world_system_creation(self, name: str = None) -> WorldSystem:

        _map = self.world_map_creation()
        world = WorldSystem(name, _map)

        return world

    def world_map_creation(self, x_axis: int = 4, y_axis: int = 4) -> OrderedDict:
        _map = OrderedDict()
        for x in range(x_axis):
            for y in range(y_axis):
                uid = uuid4()
                area = self.area_creation(pos=(x, y),
                                          name=uid,
                                          terrain='mountains',
                                          climate='tropical',
                                          uid=uid)

                _map[(x, y)] = area

        return _map


class RecipeBook(object):

    _factory = Factory()

    @property
    def factory(self):
        return self._factory

    def entity(self, name: str = '', components: List = None, uid: uuid4() = None):
        return self.factory.entity_creation(name, components, uid)

    def human(self, name: str = '', uid: uuid4() = None):
        return self.factory.human_creation(name, uid)

    def liquid(self, name: str, components: List = None):
        return self.factory.item_creation('liquid', name, components)

    def container(self, name: str, components: List = None):
        return self.factory.item_creation('container', name, components)

    def area(self, name: Union[uuid4, str],
             pos: Tuple[int, int],
             terrain: str,
             climate: str,
             components: list = None,
             uid: uuid4() = None,
             map_dimensions: Tuple[int, int] = (10, 10)):
        return self.factory.area_creation(name, pos, terrain, climate, components, uid, map_dimensions)

    def location(self, name: str, pos: Tuple[int, int], area: Entity, components: List=None):
        return self.factory.location_creation(name, pos, area, components)

    def world(self, name: str):
        return self.factory.world_system_creation(name)

    def attach(self, entity: Entity, to_attach: Union[str,List], *args, **kwargs):

        if isinstance(to_attach, str):
            return self.factory.assign_component(entity, to_attach, args, kwargs)
        else:
            return self.factory.assign_components(entity, to_attach)

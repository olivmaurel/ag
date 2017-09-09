from collections import OrderedDict
from ag.ECS import Entity
from ag.models.item import Item
import ag.components
from ag.systems import WorldSystem
from typing import Any, Union, Tuple, List
from uuid import uuid4
from core import get_yaml_as_dict


class Factory(object):

    def __getattr__(self, item):

        if item not in self.__dict__:
            if 'ml_' in item:
                self.set_master_list(item)
                return super().__getattribute__(item)
            else: # Normal behavior if not found
                raise AttributeError
        else:
            return self.item


    def set_master_list(self, listname):
        path = 'ag/fixtures/master_lists/'
        y = get_yaml_as_dict('{}{}.yml'.format(path, listname))
        self.__setattr__(listname, y)

    def assign_component(self,
                         entity: Entity,
                         cname: str, *args, **kwargs) -> None:
        _c_class = getattr(ag.components, cname.capitalize())
        component = _c_class(entity, *args, **kwargs)
        entity.__setattr__(cname.lower(), component)

    def entity_creation(self, entity: Union[str, Entity], components: list=None, uid: uuid4()=None) -> Entity:

        if isinstance(entity, str):
            entity = Entity(entity, uid)
        if components:
            for component in components:
                if isinstance(component, dict):
                    for k, v, in component.items():
                        if isinstance(v,dict):
                            self.assign_component(entity, k, **v)
                        else:
                            self.assign_component(entity, k, *v)
                else:
                    self.assign_component(entity, component)

        return entity

    def human_creation(self, name: str, uid: str=None):

        e = Entity(name, uid)
        components = ['health', 'hunger', 'geo', 'thirst', 'inv']

        return self.entity_creation(e, components)

    def area_creation(self, name: str, pos: Tuple, terrain: str, climate: str, components: list=[], uid: uuid4()=None) -> Entity:

        name = ('<{} {}:{}/{}>'.format(name, pos, terrain, climate))
        components.extend([{'terrain': [terrain]},
                           {'climate': [climate]}])

        area = self.entity_creation(name, components, uid)
        area.__setattr__('systems', [])
        area.__setattr__('entities', set())
        area.__setattr__('pos', pos if isinstance(pos, tuple) else None)
        return area

    def item_creation(self, type: str, name: str, components: List=[]) -> Item:

        ml_ref = self.__getattr__('ml_{}'.format(type))[name] # type: dict
        uid = uuid4() # type: uuid4()
        name = "{}-{}".format(ml_ref['name'], uid) # type: str
        components.extend('geo')
        return Item(name, uid, ml_ref, components)

    def loc(self, name: str, pos: Tuple, area: Entity, uid: uuid4()=None):
        # TODO
        loc = self.entity_creation(name, area.components, uid)
        return loc

    def world_system_creation(self, name: str=None) -> WorldSystem:

        _map = self.world_map_creation()
        world = WorldSystem(name, _map)

        return world

    def world_map_creation(self, x_axis: int=4, y_axis: int=4)-> OrderedDict:
        _map = OrderedDict()  # type: OrderedDict[Any,Any]
        for x in range(x_axis):
            for y in range(y_axis):
                uid = uuid4()
                area = self.area_creation(pos=(x, y),
                                 name=uid,
                                 terrain='mountains',
                                 climate='tropical',
                                 uid=uid)

                _map[(x,y)] = area

        return _map

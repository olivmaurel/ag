from collections import OrderedDict
from ag.ECS import Entity
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

    def assign_components(self, e: Entity, components: List) -> None:

        for comp in components:
            self.assign_component(e, comp)

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
        components = ['health', 'hunger', 'geo', 'thirst', 'mov', 'inv']

        return self.entity_creation(e, components)

    def area_creation(self, name: str, loc: Tuple, terrain: str, climate: str, components: list=[], uid: uuid4()=None) -> Entity:

        name = ('<{} {}:{}/{}>'.format(name, loc, terrain, climate))
        components.extend([{'terrain': [terrain]},
                           {'climate': [climate]}])

        area = self.entity_creation(name, components, uid)
        area.__setattr__('systems', [])
        area.__setattr__('entities', set())
        area.__setattr__('loc', loc if isinstance(loc, tuple) else None)
        return area

    def item_creation(self, type: str, name: str, components: List=[]) -> Entity:

        try:
            ml_ref = self.__getattr__('ml_{}'.format(type))[name]  # type: dict
        except AttributeError:
            ml_ref = self.__getattribute__('ml_{}'.format(type))[name]  # type: dict
        components.append('geo')
        components.extend(ml_ref['traits'])
        uid = uuid4()  # type: uuid4()
        name = "{}-{}".format(ml_ref['name'], uid)  # type: str

        e = self.entity_creation(name, components)

        for k, v in ml_ref.items():
            if not hasattr(e, k) or e.k == False:
                e.__setattr__(k, v)

        return e

    def world_system_creation(self, name: str=None) -> WorldSystem:

        _map = self.world_map_creation()
        world = WorldSystem(name, _map)

        return world

    def world_map_creation(self, x_axis: int=4, y_axis: int=4)-> OrderedDict:
        _map = OrderedDict()  # type: OrderedDict[Any,Any]
        for x in range(x_axis):
            for y in range(y_axis):
                uid = uuid4()
                area = self.area_creation(loc=(x, y),
                                          name=uid,
                                          terrain='mountains',
                                          climate='tropical',
                                          uid=uid)

                _map[(x,y)] = area

        return _map

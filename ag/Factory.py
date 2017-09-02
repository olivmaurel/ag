from collections import OrderedDict
from ag.ECS import Entity
import ag.components
from ag.systems import WorldSystem
from typing import Any, Union, Tuple
from uuid import uuid4

class Factory(object):

    def assign_component(self,
                         entity: Entity,
                         cname: str, *args, **kwargs) -> None:
        _c_class = getattr(ag.components, cname.capitalize())
        component = _c_class(entity, *args, **kwargs)
        entity.__setattr__(cname.lower(), component)

    def entity(self, entity: Union[str, Entity], components: list=None, uid: uuid4()=None) -> Entity:

        if isinstance(entity, str):
            entity = Entity(entity, uid)
        if components:
            for component in components:
                if isinstance(component, dict):
                    for k, v, in component.items():
                        self.assign_component(entity, k, *v)
                else:
                    self.assign_component(entity, component)

        return entity

    def human(self, name: str, uid: str=None):

        e = Entity(name, uid)
        components = ['health', 'hunger', 'geo', 'thirst']

        return self.entity(e, components)

    def area(self,
             name: str,
             pos: Tuple,
             terrain: str,
             climate: str,
             components: list=[],
             uid: uuid4()=None) -> Entity:

        name = ('<{} {}:{}/{}>'.format(name, pos, terrain, climate))
        components.extend([{'terrain': [terrain]},
                           {'climate': [climate]}])

        area = self.entity(name, components, uid)
        area.systems = []
        area.entities = set()
        area.pos = pos if isinstance(pos, tuple) else None
        return area


    def consumable(self, name, uid=None):

        e = Entity(name, uid)

        # extract the components corresponding to the name
        # if name is unknown, return error
        components = ['item']

        return self.entity(e, components)

    def loc(self, name: str, pos: Tuple, area: Entity, uid: uuid4()=None):
        # TODO
        loc = self.entity(name, area.components, uid)
        return loc

    def make_world_system(self, name: str=None) -> WorldSystem:

        _map = self.make_world_map()
        world = WorldSystem(name, _map)

        return world

    def make_world_map(self, x_axis: int=4, y_axis: int=4)-> OrderedDict:
        _map = OrderedDict()  # type: OrderedDict[Any,Any]
        for x in range(x_axis):
            for y in range(y_axis):
                uid = uuid4()
                area = self.area(pos=((x, y)),
                                 name=uid,
                                 terrain='mountains',
                                 climate='tropical',
                                 uid=uid)

                _map[(x,y)] = area

        return _map

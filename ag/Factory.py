from collections import OrderedDict
from ag.ECS import Entity
import ag.components
from ag.systems import WorldSystem
from typing import Any, Union, Dict

class Factory(object):

    def assign_component(self,
                         entity: Entity,
                         cname: str, *args, **kwargs) -> None:
        _c_class = getattr(ag.components, cname.capitalize())
        component = _c_class(entity, *args, **kwargs)
        entity.__setattr__(cname.lower(), component)

    def make_entity(self, entity: Union[str, Entity], components: list=None) -> Entity:

        if isinstance(entity, str):
            entity = Entity(entity)
        if components:
            for component in components:
                if isinstance(component, dict):
                    for k, v, in component.items():
                        self.assign_component(entity, k, *v)
                else:
                    self.assign_component(entity, component)

        return entity

    def make_human(self, name: str, uid: str=None):

        e = Entity(name, uid)
        components = ['health', 'hunger', 'geo', 'thirst']

        return self.make_entity(e, components)

    def make_area(self,
                  geo: Dict,
                  terrain: str,
                  climate: str,
                  components: list=[]) -> Entity:

        name = ('<Area {}:{}/{}>'.format(geo, terrain, climate))
        components.extend([{'geo': [geo]},
                           {'terrain': [terrain]},
                           {'climate': [climate]}])

        area = self.make_entity(name, components)
        area.systems = []

        return area

    def make_world_system(self, name: str=None) -> WorldSystem:

        _map = self.make_world_map()
        world = WorldSystem(name, _map)

        return world

    def make_world_map(self, x_axis: int=4, y_axis: int=4)-> OrderedDict:
        _map = OrderedDict()  # type: OrderedDict[Any,Any]
        for x in range(x_axis):
            for y in range(y_axis):
                area = self.make_area(geo={"area": (x, y)},
                                      terrain='mountains',
                                      climate='tropical')

                _map[(x,y)] = area

        return _map

from collections import OrderedDict
from ag.ECS import Entity
import ag.components
from ag.World import World


class GameObjectFactory(object):

    def assign_component(self, entity, cname, *args, **kwargs):

        _c_class = getattr(ag.components, cname.capitalize())
        component = _c_class(entity, *args, **kwargs)
        entity.__setattr__(cname.lower(), component)

    def make_object(self, entity, components=None):

        if isinstance(entity, str):
            entity = Entity(entity)

        for component in components:
            if isinstance(component, dict):
                for k, v, in component.items():
                    self.assign_component(entity, k, *v)
            else:
                self.assign_component(entity, component)

        return entity

    def make_human(self, name, uid=None):

        e = Entity(name, uid)
        components = ['health', 'hunger', 'position', 'thirst']

        return self.make_object(e, components)

    def make_area(self, name, terrain, climate, uid=None):

        e = Entity(name, uid)
        components = [{'terrain': [terrain], 'climate':[climate]}]

        return self.make_object(e, components)

    def make_world(self, name, x_size, y_size, uid=None):

        components = [{'Map': [x_size, y_size]}]

        world = self.make_object(World(name, uid), components)

        for coord, content in world.map.grid.items():
            content.append(self.make_area('area', 'mountains', 'alpine'))

        return world

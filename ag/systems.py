from ag.ECS import System, Entity
from collections import OrderedDict
from typing import List, Tuple, Union


class BiologicalNeedsSystem(System):

    components = ['Hunger', 'Thirst']

    def __init__(self, name="Biological system", components=[]):
        super().__init__(name, components)

    def update(self):

        for e in self.entities:

            if e.hunger:

                if e.hunger.current >= 5:
                    e.hunger.current -= 5
                status = e.hunger.status
                if status == 'famished':
                    e.conditions['malnourished'] += 1
                if status == 'starving':
                    e.conditions['malnourished'] += 2
                    if e.health:
                        e.health.change(-10)
            if e.thirst:
                if e.thirst.current >= 5:
                    e.thirst.current -= 5
                status = e.thirst.status
                if status == 'dehydrated':
                    e.conditions['dehydrated'] += 1
                if status == 'parched':
                    e.conditions['dehydrated'] += 2
                    if e.health:
                        e.health.change(-10)


class GeoSystem(System):

    components = ['geo']

    def update(self):
        raise NotImplementedError('Not implemented')


class WorldSystem(System):

    # components = ['Map']
    Active_area_default_systems = [BiologicalNeedsSystem]

    def __init__(self, name='World', _map: OrderedDict = None, components: List = []):

        super().__init__(name, components)
        self.map = _map
        self.active_position = None

    @property
    def active_area(self):
        return self.map[self.active_position]

    def update(self):

        self.active_area.update()
        self.update_inactive_areas()

    def update_inactive_areas(self):
        pass
        # for coord in self._map.items():
        #        if coord != self.active_area:
        #           coord.update()

    def add_system(self, pos: Tuple[int, int], system: System):

        if isinstance(system, System):
            self.map[pos].systems.append(system)
        else:
            raise TypeError("The variable {} is not a System, it's a {}"
                            .format(system, type(system)))

    def add_area(self, area: Entity):

        if isinstance(area, Entity):
            self.map[area.pos] = area
        else:
            raise TypeError("The variable {} is not an Entity, it's a {}"
                            .format(area, type(area)))

    def remove_system(self, pos: Tuple[int, int], system: System):

        if isinstance(system, System):
            self.map[pos].systems.remove(system)
        else:
            raise TypeError("The variable {} is not a System, it's a {}"
                            .format(system, type(system)))

    def set_active_area(self, position: Union[Entity, Tuple[int, int]]):

        if isinstance(position, Entity):
            position = position.pos

        if position in self.map.keys():
            if self.active_position is not None:
                self.active_area.systems.clear()
            self.active_position = position
            self.assign_default_systems_to_active_area()
            self.active_area.active = True
        else:
            raise KeyError('No such coordinates in {}.map'.format(self.name))

    def assign_default_systems_to_active_area(self):

        for system in self.Active_area_default_systems:
            self.active_area.systems.append(system())

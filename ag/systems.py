from ag.ECS import System
from collections import OrderedDict
from typing import List, Tuple


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
                        e.health.current -= 10
            if e.thirst:
                if e.thirst.current >= 5:
                    e.thirst.current -= 5
                status = e.thirst.status
                if status == 'dehydrated':
                    e.conditions['dehydrated'] +=1
                if status == 'parched':
                    e.conditions['dehydrated'] += 2


class GeoSystem(System):

    components = ['geo']

    def update(self):
        raise NotImplementedError ('Not implemented')


class WorldSystem(System):

    # components = ['Map']

    def __init__(self, name='World', _map: OrderedDict=None, components: List=[]):

        super().__init__(name, components)
        self._map = _map
        self.active_coords = (0, 0)


    @property
    def active_area(self):
        return self._map[self.active_coords]

    def update(self):

        self.update_active_area()
        self.update_inactive_areas()

    def update_area(self, coords: Tuple[int, int]):

        for system in self._map[coords].systems:
            system.update()

    def update_active_area(self):
        return self.update_area(self.active_area)

    def update_inactive_areas(self):
        for coord in self._map.items():
                if coord != self.active_area:
                    self.update_area(coord)

    def add_system(self, coords: Tuple[int, int], system: System):

        if isinstance(system, System):
            self._map[coords].systems.append(system)
        else:
            raise TypeError("The variable {} is not a system, it's a {}"
                            .format(system, type(system)))

    def set_active_area(self, coords: Tuple[int, int]):

        if coords in self._map.keys():
            self.active_coords = coords
        else:
            raise KeyError('No such coordinates in {}.map'.format(self.name))

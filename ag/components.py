import math
import itertools
from collections import OrderedDict as dict
from ag.ECS import Component, System, Entity
from typing import Tuple


class Hunger(Component):

    defaults = dict([('current', 100), ('max', 100)])
    hungerscale = dict([(100, 'full'), (75, 'fed'), (50, 'hungry'), (25, 'famished'), (0, 'starving')])

    @property
    def status(self) -> str:
        c = int(math.ceil(self.current / 25.0)) * 25
        return self.hungerscale[c]


class Thirst(Component):

    defaults = dict([('current', 100), ('max', 100)])
    thirstscale = dict([(100, 'fine'), (75, 'fine'), (50, 'thirsty'), (25, 'dehydrated'), (0, 'parched')])

    @property
    def status(self) -> str:
        c = int(math.ceil(self.current / 25.0)) * 25
        return self.thirstscale[c]


class Health(Component):
    '''Contains current and max value of health for an entity

    >>> from ag.ECS import Entity
    >>> player = Entity('player', 0)
    >>> player
    <Entity player:0>
    >>> player.health = Health(player, current=80)
    >>> player.health
    <Health  entity:player.health>
    >>> print (player.health)
    {
        "current": 80,
        "max": 100
    }
    >>> print (player.health['current'])
    80
    >>> print (player.health.alive)
    True
    >>> player.health['current'] = 65
    >>> print (player.health)
    {
        "current": 65,
        "max": 100
    }
    >>> print (player.health.Catalog)
    {<Entity player:0>: <Health  entity:player.health>}
    '''
    defaults = dict([('current', 100), ('max', 100)])

    @property
    def alive(self) -> bool:
        return self.current > 0


class Geo(Component):

    defaults = dict([('loc', (0, 0))])

    def __init__(self, e: Entity, area: Entity=None, *args, **kwargs) -> None:
        super().__init__(e, *args, **kwargs)
        self.area = area
        e.area = self.area
        e.loc = self.loc
        e.enter_area = self.enter_area

    def enter_area(self, area: Entity):

        if (self.entity.area):
            self.entity.area.entities.discard(self.entity)

        self.entity.area = area
        self.area = area

        area.entities.add(self.entity)

    def enter_loc(self, loc: Tuple):

        self.loc = loc
        self.entity.loc = loc




class Movement(Component):
    pass

class Terrain(Component):

    defaults = dict([('type', 'island')])

    def dostuff(self):
        return 'Woooo!'


class Climate(Component):

    defaults = dict([('type', 'tropical')])


class Map(Component):

    def __init__(self, entity, x_size, y_size):
        super().__init__(self, entity)
        self.x_size = x_size
        self.y_size = y_size
        self.grid = dict((coord, []) for coord in
                    [g for g in itertools.product(range(x_size), range(y_size))])

    def __str__(self):
        return self.grid

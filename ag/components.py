import math
import itertools
from collections import OrderedDict as dict
from ag.ECS import Component


class Hunger(Component):

    defaults = dict([('current', 100), ('max', 100)])
    hungerscale = dict([(100, 'full'), (75, 'fed'), (50, 'hungry'), (25, 'famished'), (0, 'starving')])

    @property
    def status(self):
        c = int(math.ceil(self.current / 25.0)) * 25
        return self.hungerscale[c]


class Thirst(Component):

    defaults = dict([('current', 100), ('max', 100)])
    thirstscale = dict([(100, 'fine'), (75, 'fine'), (50, 'thirsty'), (25, 'dehydrated'), (0, 'parched')])

    @property
    def status(self):
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
    def alive(self):
        return self.current > 0


class Position(Component):

    def __init__(self, entity, x, y, area=None):
        super().__init__(self)
        self.area = area
        self.x = x
        self.y = y


class Movement(Component):

    def enter_area(self, entity, area):
        if self.entity.position:
            self.entity.position.area = area
        else:
            raise ValueError ('{} has no position component'.format(self.entity.name))


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

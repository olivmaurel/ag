import math
import itertools
from collections import OrderedDict as dict
from ag.ECS import Component, Entity
from typing import Tuple, Any

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
        e.__setattr__('area', self.area)
        e.__setattr__('loc', self.loc)

    def enter_loc(self, loc: Tuple):

        self.loc = loc
        self.entity.loc = loc


class Mov(Component):

    def __init__(self, e: Entity, *args, **kwargs) -> None:
        super().__init__(e, *args, **kwargs)
        e.__setattr__('enter_area', self.enter_area)
        e.__setattr__('moveto', self.moveto)

    def enter_area(self, area: Entity):

        if self.entity.area:
            self.entity.area.entities.discard(self.entity)

        self.entity.area = area

        area.entities.add(self.entity)

    def moveto(self, loc: Tuple[int, int]):

        self.entity.loc = loc




class Terrain(Component):

    defaults = dict([('type', 'island')])

    def dostuff(self):
        return 'Woooo!'


class Inv(Component):

    defaults = dict([('capacity', 100), ('content', []), ('filled', 0)])

    def __init__(self, e: Entity, *args, **kwargs) -> None:
        super().__init__(e, *args, **kwargs)
        e.__setattr__('pickup', self.pickup)
        e.__setattr__('drop', self.drop)

    @property
    def owner(self):
        return self.entity
    @property
    def space_left(self):
        return self.capacity - self.filled

    @property
    def full(self):
        return self.capacity <= 0

    def add(self, item: Entity):

        self.content.append(item)
        self.filled += item.size

    def remove(self, item: Entity):
        if item in self.content:
            self.content.remove(item)
            self.filled -= item.size
        else:
            return False

    def pickup(self, item: Entity):
        if self.entity.loc == item.loc and item.carriable and item.size <= self.space_left:
            self.add(item)
            item.carriedby(self.owner)
        else:
            return False

    def drop(self, item: Entity):
        self.remove(item)
        if item.carriable:
            item.dropped()

class Liquidcontainer(Component):

    defaults = dict([('capacity', 100), ('content', []), ('filled', 0), ('unit', 'litre')])

    def __init__(self, e: Entity, *args, **kwargs) -> None:
        super().__init__(e, *args, **kwargs)

    @property
    def space_left(self):
        return self.capacity - self.filled

    def fill(self, liquid):
        if not self.empty:
            if self.content.type != liquid.type:
                return False
        else:
            self.filled += liquid.volume
            if self.space_left < 0:
                self.filled = self.capacity
                self.content.volume = self.capacity

    def pour(self, volume: int, recipient: Entity):
        self.filled -= volume
        liquid = Liquid(self.content.type)
        recipient.receive(liquid)


class Liquid(Component):

    def __init__(self, e: Entity, type: str, *args, **kwargs) -> None:
        super().__init__(e, *args, **kwargs)
        self.type = type




class Climate(Component):

    defaults = dict([('type', 'tropical')])


class Carriable(Component):

    def __init__(self, e: Entity, *args, **kwargs) -> None:
        super().__init__(e, *args, **kwargs)
        self.carrier = None
        e.__setattr__('carrier', self.carrier)
        e.__setattr__('carriedby', self.carriedby)
        e.__setattr__('dropped', self.dropped)

    def carriedby(self, e: Entity):
        self.carrier = e
        self.entity.carrier = e
        if self.entity.geo != False:
            self.entity.__delattr__('area')
            self.entity.__delattr__('loc')
            del self.entity.components['geo']


    def dropped(self):

        self.entity.geo = Geo(self.entity)
        self.entity.area = self.entity.carrier.area
        self.entity.loc = self.entity.carrier.loc
        self.carrier = None
        self.entity.carrier = None

class Map(Component): # TODO deprec remove

    def __init__(self, entity, x_size, y_size):
        super().__init__(self, entity)
        self.x_size = x_size
        self.y_size = y_size
        self.grid = dict((coord, []) for coord in
                    [g for g in itertools.product(range(x_size), range(y_size))])

    def __str__(self):
        return self.grid

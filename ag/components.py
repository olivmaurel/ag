import math
from collections import OrderedDict as dict
from ag.ECS import Component, Entity
from typing import Tuple
from ag.settings import logging



class Hunger(Component):

    defaults = dict([('current', 100), ('max', 100)])
    hunger_scale = dict([(100, 'full'), (75, 'fed'), (50, 'hungry'), (25, 'famished'), (0, 'starving')])

    @property
    def status(self) -> str:
        c = int(math.ceil(self.current / 25.0)) * 25
        return self.hunger_scale[c]


class Thirst(Component):

    defaults = dict([('current', 100), ('max', 100)])
    thirst_scale = dict([(100, 'fine'), (75, 'fine'), (50, 'thirsty'), (25, 'dehydrated'), (0, 'parched')])

    @property
    def status(self) -> str:
        c = int(math.ceil(self.current / 25.0)) * 25
        return self.thirst_scale[c]


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

    defaults = dict([('pos', (0, 0))])

    def __init__(self, e: Entity, area: Entity=None, *args, **kwargs) -> None:
        super().__init__(e, *args, **kwargs)
        self.area = area
        e.__setattr__('area', self.area)
        e.__setattr__('pos', self.pos)


class Mov(Component):

    def __init__(self, e: Entity, *args, **kwargs) -> None:
        super().__init__(e, *args, **kwargs)
        e.__setattr__('enter_area', self.enter_area)
        e.__setattr__('moveto', self.moveto)

    def enter_area(self, area: Entity, pos: Tuple[int, int]):

        if self.entity.area is not None:
            self.entity.area.map[pos].entities.remove(self.entity)
        self.entity.area = area
        self.moveto(pos)
        area.map[pos].entities.append(self.entity)

    def moveto(self, pos: Tuple[int, int]):

        self.entity.pos = pos


class Location(Component):

    def __init__(self, e: Entity, area: Entity, *args, **kwargs) -> None:
        super().__init__(e, *args, **kwargs)
        self.systems = []
        self.area = area
        self.entities = []
        e.__setattr__('systems', self.systems)
        e.__setattr__('area', self.area)
        e.__setattr__('entities', self.entities)


class Per(Component):

    def __init__(self, e: Entity, *args, **kwargs) -> None:
        super().__init__(e, *args, **kwargs)
        e.__setattr__('locate', self.locate)

    def locate(self, something):
        pass
        # if isinstance(something, )


class Terrain(Component):

    defaults = dict([('type', 'island')])


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

        if item not in self.content:
            logging.error('{} is not in {} inventory'.format(item.name, self.entity.name))
            return False
        else:
            self.content.remove(item)
            self.filled -= item.size
            return True

    def pickup(self, item: Entity):

        if self.entity.pos != item.pos:
            logging.error('{}({}) is not located in {}, impossible to pickup {}'
                           .format(self.entity.name, self.entity.pos, item.pos, item.name))
            return False
        elif not item.carriable:
            logging.error('{} cannot be picked up, it is not a carriable item'.format(item.name))
            return False
        elif item.size > self.space_left:
            logging.error('Not enough space left in {} inventory. '
                          'The item is {} units big, and there is only {} space left.'
                          .format(self.entity.name, item.size, self.space_left))
            return False
        else:
            self.add(item)
            item.carriedby(self.owner)
            return True

    def drop(self, item: Entity):

        if not item.carriable:
            logging.error('{} cannot be dropped, not a carriable item.'.format(item.name))
            return False
        if item not in self.content:
            logging.error('{} is not in {} inventory'.format(item.name, self.entity.name))
            return False
        else:
            self.remove(item)
            item.dropped()
            return True

    def __repr__(self):
        return str(self.content)


class Liquidcontainer(Component):

    defaults = dict([('capacity', 100), ('content', []), ('filled', 0), ('unit', 'litre')])

    def __init__(self, e: Entity, *args, **kwargs) -> None:
        super().__init__(e, *args, **kwargs)
        e.__setattr__('filled', self.filled)

    @property
    def space_left(self):
        return self.capacity - self.filled
    def fill(self, liquid):
        if not self.empty:
            if self.content.type != liquid.type:
                logging.error("Can't add {} to a container filled with {}"
                              .format(liquid.type, self.content.type))
                return False
        else:
            self.filled += liquid.volume
            if self.space_left < 0:
                self.filled = self.capacity
                self.content.volume = self.capacity
            return True

    def pour(self, volume: int, recipient: Entity):
        self.filled -= volume
        liquid = Liquid(self.content.type)
        recipient.receive(liquid) # todo drink action with Character drinking Liquid from Liquidcontainer


class Liquid(Component):

    def __init__(self, e: Entity, type: str, *args, **kwargs) -> None:
        super().__init__(e, *args, **kwargs)
        self.type = type


class Drinkable(Liquid):

    def __init__(self, e: Entity, type: str, *args, **kwargs) -> None:
        super().__init__(e, *args, **kwargs)
    # TODO add attr drink to 'liquidcontainer' entity if possible

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
            self.entity.__delattr__('pos')
            del self.entity.components['geo']

    def dropped(self):

        self.entity.geo = Geo(self.entity)
        self.entity.area = self.entity.carrier.area
        self.entity.pos = self.entity.carrier.pos
        self.carrier = None
        self.entity.carrier = None


class Updater(Component):

    def __init__(self, e: Entity, *args, **kwargs) -> None:
        super().__init__(e, *args, **kwargs)
        self.systems = []
        e.__setattr__('systems', self.systems)
        e.__setattr__('update', self.update)

    def update(self):
        for system in self.entity.systems:
            system.update()

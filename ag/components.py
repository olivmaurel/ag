import math
from collections import OrderedDict as dict
from enum import Enum

from ag.ECS import Component, Entity
from typing import Tuple

from ag.exceptions.exceptions import EmptyContainerException, NoSuchComponentException, MixedLiquidsException
from ag.settings import logging


class Hunger(Component):

    defaults = dict([('current', 100), ('max', 100)])
    scale = dict([(100, 'full'), (75, 'fed'), (50, 'hungry'), (25, 'famished'), (0, 'starving')])

    @property
    def status(self) -> str:
        c = int(math.ceil(self.current / 25.0)) * 25
        return self.scale[c]


class Thirst(Component):

    defaults = dict([('current', 100), ('max', 100)])
    scale = dict([(100, 'fine'), (75, 'fine'), (50, 'thirsty'), (25, 'dehydrated'), (0, 'parched')])

    def __init__(self, e: Entity, *args, **kwargs) -> None:
        super().__init__(e, *args, **kwargs)

        e.__setattr__('do_drink', self.do_drink)

    def do_drink(self, item: Entity):
        if 'drinkable' not in item.components:
            raise NoSuchComponentException('drinkable', item)
        elif 'liquidcontainer' in item.components:
            if item.get_filled() <= 0:
                raise EmptyContainerException(item)
            else:
                item.do_empty()

        self.remove_thirst()
        return True


    @staticmethod
    def is_drinkable(item):
        return 'drinkable' in item.components

    def remove_thirst(self) -> None:
        self.entity.thirst.current = self.entity.thirst.max
        self.entity.conditions.pop('thirsty', None)

    @property
    def status(self) -> str:
        c = int(math.ceil(self.current / 25.0)) * 25
        return self.scale[c]


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
    defaults = dict([('current', 100), ('max', 100), ('min', 0)])

    def change(self, value):
        if self.alive:
            self.current = min(max(self.current + value, self.min), self.max)

    @property
    def alive(self) -> bool:
        return self.current > 0


class Geo(Component):

    defaults = dict([('pos', (0, 0))])

    def __init__(self, e: Entity, area: Entity = None, *args, **kwargs) -> None:
        super().__init__(e, *args, **kwargs)
        self.area = area
        e.__setattr__('area', self.area)
        e.__setattr__('pos', self.pos)
        e.__setattr__('x', self.x)
        e.__setattr__('y', self.y)

    def x(self) -> int:
        return self.pos[0]

    def y(self) -> int:
        return self.pos[1]


class Mov(Component):

    def __init__(self, e: Entity, *args, **kwargs) -> None:
        super().__init__(e, *args, **kwargs)
        e.__setattr__('enter_area', self.enter_area)
        e.__setattr__('moveto', self.moveto)

    def enter_area(self, area: Entity, pos: Tuple[int, int]):

        if not area:
            logging.error('{} mov component cannot enter area {}'.format(self, area))
            return KeyError('error')

        self.leave_area(pos)
        self.entity.area = area
        self.moveto(pos)
        area.map[pos].entities.append(self.entity)

    def leave_area(self, pos: Tuple[int, int]):

        if self.entity.area:
            self.entity.area.map[pos].entities.remove(self.entity)

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


class ContainerStatus(Enum):
    full = 0
    empty = 1
    part = 2


class Container(Component):

    def __init__(self, e: Entity, *args, capacity=100, content=[], filled=0, **kwargs) -> None:
        super().__init__(e, *args, **kwargs)
        self.status = ContainerStatus.empty
        self.capacity = capacity
        self.content = content
        self.filled = filled
        e.__setattr__('capacity', self.capacity)
        e.__setattr__('content', self.content)
        e.__setattr__('get_status', self.get_status)
        e.__setattr__('get_filled', self.get_filled)
        e.__setattr__('is_full', self.is_full)
        e.__setattr__('is_empty', self.is_empty)
        e.__setattr__('do_empty', self.do_empty)


    @property
    def space_left(self):
        return self.capacity - self.filled

    def get_status(self):
        return self.status

    def get_filled(self) -> int:
        return self.filled

    def is_empty(self) -> bool:
        return self.status == ContainerStatus.empty

    def is_full(self) -> bool:
        return self.status == ContainerStatus.full

    def do_empty(self) -> None:
        self.filled = 0
        self.update_status()

    def update_status(self) -> None:
        if self.filled <= 0:
            self.status = ContainerStatus.empty
        elif self.filled == self.capacity:
            self.status = ContainerStatus.full
        else:
            self.status = ContainerStatus.part

        self.entity.status = self.status
        self.entity.filled = self.filled

class Inv(Container):

    defaults = dict([('capacity', 100), ('content', []), ('filled', 0)])

    def __init__(self, e: Entity, *args, **kwargs) -> None:
        super().__init__(e, *args, **kwargs)
        e.__setattr__('pickup', self.pickup)
        e.__setattr__('drop', self.drop)

    @property
    def owner(self):
        return self.entity

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


class Liquidcontainer(Container):

    defaults = dict([('capacity', 100), ('content', None), ('filled', 0), ('unit', 'litre')])

    def __init__(self, e: Entity, *args, **kwargs) -> None:
        super().__init__(e, *args, **kwargs)
        e.__setattr__('fill', self.fill)

    def fill(self, content: Entity, volume=None):
        if 'liquid' not in content.components:
            raise NoSuchComponentException('liquid', content)
        elif self.is_empty():
            self.content = content
        elif self.content.name != content.name:
            raise MixedLiquidsException(self, content)

            return False

        self.filled += volume or self.capacity
        self.update_status()

    def pour(self, volume: int, recipient: Entity):
        self.filled -= volume
        liquid = Liquid(self.content.type)
        recipient.receive(liquid)  # todo drink action with Character drinking Liquid from Liquidcontainer
        self.update_status()


class Liquid(Component):

    def __init__(self, e: Entity, *args, **kwargs) -> None:
        super().__init__(e, *args, **kwargs)


class Drinkable(Liquid):

    def __init__(self, e: Entity, *args, **kwargs) -> None:
        super().__init__(e, *args, **kwargs)
    # TODO add attr drink to 'liquidcontainer' entity if possible


class Climate(Component):

    defaults = dict([('type', 'tropical')])


class Needs(Component):
    """
        Helps give priority order to entity
    """
    # list of needs with a priority order
    defaults = dict([('breathe', 'drink')])


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

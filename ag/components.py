import math
from collections import OrderedDict as dict
from enum import Enum

from ag.ECS import Component
from typing import Tuple

from ag.constants import Conditions as C, Actions
from ag.exceptions.exceptions import *
from ag.settings import logging


class Hunger(Component):

    scale = dict([(100, 'full'), (75, 'fed'), (50, 'hungry'), (25, 'famished'), (0, 'starving')])

    def __init__(self, e: Entity, *args, current: int = 100, max: int = 100, min: int = 0, **kwargs) -> None:
        self.current = current
        self.max = max
        self.min = min
        super().__init__(e, *args, **kwargs)

    def do_eat(self, item: Entity):

        if not self.same_position(item):
            logging.error('{}({}) is not located in {}, impossible to drink it {}'
                          .format(self.entity.name, self.entity.pos, item.pos, item.name))
            return False

        raise NotImplementedError('Add this component : hunger')

    @property
    def status(self) -> str:
        c = int(math.ceil(self.current / 25.0)) * 25
        return self.scale[c]


class Thirst(Component):

    scale = dict([(100, 'fine'), (75, 'fine'), (50, 'thirsty'), (25, 'dehydrated'), (0, 'parched')])

    def __init__(self, e: Entity, *args, current: int = 100, max: int = 100, min: int = 0, **kwargs) -> None:
        self.current = current
        self.max = max
        self.min = min
        super().__init__(e, *args, **kwargs)

        e.__setattr__('do_drink', self.do_drink)

    def do_drink(self, item: Entity):

        if not self.same_position(item):
            raise DifferentPositionException(self.entity, item)

        is_container = False
        if 'liquidcontainer' in item.components:
            if item.get_filled() <= 0:
                raise EmptyContainerException(item)
            liquid = item.content
            is_container = True
        else:
            liquid = item
        if not liquid.drinkable:
            raise NoSuchPropertyException('drinkable', liquid)

        if is_container:
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

    defaults = dict([('current', 100), ('max', 100), ('min', 0)])

    def __init__(self, e: Entity, *args, current=100, max = 100, min = 0, **kwargs) -> None:
        self.current = current
        self.max = max
        self.min = min
        super().__init__(e, *args, **kwargs)

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

    @property
    def x(self) -> int:
        return self.pos[0]

    @property
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


class Perception(Component):

    def __init__(self, e: Entity, *args, **kwargs) -> None:
        super().__init__(e, *args, **kwargs)
        e.__setattr__('locate', self.locate)
        raise NotImplementedError('Implement this')

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

    def __init__(self, e: Entity, *args, capacity=100, filled=0, size=1, **kwargs) -> None:
        self.status = ContainerStatus.empty
        self.capacity = capacity
        self.filled = filled
        self.size = size
        self.content = []
        super().__init__(e, *args, **kwargs)

        e.__setattr__('capacity', self.capacity)
        e.__setattr__('content', self.content)
        e.__setattr__('size', self.size)
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
            self.content = []
        elif self.filled == self.capacity:
            self.status = ContainerStatus.full
        else:
            self.status = ContainerStatus.part

        self.entity.status = self.status
        self.entity.filled = self.filled
        self.entity.content = self.content


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

        if not self.same_position(item):
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

    defaults = dict([('capacity', 100), ('filled', 0), ('unit', 'litre')])

    def __init__(self, e: Entity, *args, **kwargs) -> None:
        super().__init__(e, *args, **kwargs)
        e.__setattr__('fill', self.fill)

    @property  # only one content per liquid container
    def content(self):
        try:
            return self.__content[0]
        except IndexError:
            return self.__content

    @content.setter
    def content(self, value):
        if isinstance(value, list):
            self.__content = value
        else:
            self.__content.clear()
            self.__content.append(value)

    def fill(self, liquid: Entity, volume=None):

        if not self.same_position(liquid):
            raise DifferentPositionException(self.entity, liquid)
        if 'liquid' not in liquid.components.keys():
            raise NoSuchComponentException('liquid', liquid)
        elif self.is_empty():
            self.content = liquid
        elif self.content.name != liquid.name:
            raise MixedLiquidsException(self, liquid)

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
        if self.entity.geo:
            self.entity.__delattr__('area')
            self.entity.__delattr__('pos')
            self.entity.__delattr__('x')
            self.entity.__delattr__('y')
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


class Decision(Component):

    def __init__(self, e: Entity, *args, **kwargs):
        super().__init__(e, *args, **kwargs)

        self.needs = []
        self.hierarchy = dict() # Ordered dict !
        self.hierarchy[C.suffocating] = Actions.breathe
        self.hierarchy[C.thirsty] = Actions.drink
        self.hierarchy[C.hungry] = Actions.eat

        e.__setattr__('decide', self.decide)

    def decide(self):
        self.evaluate()
        decision = next(iter(self.needs))
        self.reset()
        return decision

    def evaluate(self):
        for condition, action in self.hierarchy.items():
            if condition in self.entity.conditions:
                self.needs.append(action)

    def reset(self):
        self.needs = []

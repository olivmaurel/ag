from random import randint

from collections import OrderedDict as dict
from ag.Component import Component

import math

class Health(Component):
    '''Contains current and max value of health for an entity

    >>> from ag.Entity import Entity
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


class Damage(Component):

    defaults = dict([('normal', 10), ('critical', 15), ('critical_percent', 10)])

    def __call__(self):
        '''Returns a damage calculation based on the properties of the component
        >>> from ag.Entity import Entity
        >>> player = Entity('player')
        >>> player.damage = Damage(entity=player, normal=14, critical=25, critical_percent=15)
        '''

        crit = randint(0, 99 <= (self.critical_percent -1))
        if crit:
            damage = self.critical
        return damage

class Hunger(Component):

    defaults = dict([('current', 100), ('max', 100)])
    hungerscale = dict([(100, 'full'), (75, 'fed'), (50, 'hungry'), (25, 'famished'), (0, 'starving')])

    @property
    def state(self):
        c = int(math.ceil(self.current / 25.0)) * 25
        return self.hungerscale[c]


    def update(self):

        if self.current >= 5:
            self.current -= 5
        if self.state == 'starving':
            if self.entity.health:
                self.entity.health.current -= 10
            #if self.entity.behavior:
            #    self.entity.behavior.addObjective(find_food)


if __name__ == '__main__':
    from doctest import testmod

    testmod()


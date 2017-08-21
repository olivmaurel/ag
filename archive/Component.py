from collections import OrderedDict as dict
import json
from ag.Entity import Entity

class Component(object):
    '''Contains a set of unique properties
    Components have a tightly coupled relationship with an entity
    >>> HealthComponent = ComponentFactory('Health', current=100, max=100)
    >>> player = Entity('Player')
    >>> player.health = HealthComponent(current=10)
    >>> player.health
    <Health entity:Player.health>
    >>> print(player.health)
    {
        "current": 10,
        "max": 100
    }
    >>> player.health.current
    10
    >>> isinstance(player.health, Component)
    True
    >>> isinstance(player.health, HealthComponent)
    True
    '''


    __slots__ = ['entity']

    defaults = dict()
    Catalog = dict()
    ComponentTypes = dict()

    def __new__(cls, entity=None, **properties):
        cname = cls.__name__
        if cname not in Component.ComponentTypes:
            Component.ComponentTypes[cname] = cls
            cls.Catalog = {}
        if entity is not None:
            if entity not in cls.Catalog:
                component = super(Component, cls).__new__(cls)
                cls.Catalog[entity] = component
            else:
                component = cls.Catalog[entity]
        else:
            component = super(Component, cls).__new__(cls)
        return component



    def __init__(self, entity=None, **properties):
        '''properties'''

        self.entity = entity
        for prop, val in self.defaults.items():
            setattr(self, prop, properties.get(prop, val))

    def __repr__(self):
        '''<Component entity_id>'''
        cname = self.__class__.__name__
        entity_name = ''
        if self.entity:
            for prop_name, component in self.entity.components.items():
                if component == self:
                    entity_name = ' entity:{}.{}'.format(self.entity.name, prop_name)
                    break
        return '<{} {}>'.format(cname, entity_name)

    def __str__(self):
        '''Dump out the JSON of the properties'''
        keys = self.defaults.keys()
        data = dict()
        for key in keys:
            if key != 'defaults':
                data[key] = getattr(self, key)
        json_string = '\n'.join(
            line.rstrip()
            for line in json.dumps(data, indent=4).split('\n')
            )
        return json_string

    def __getitem__(self, key):
        '''Allows access to attributes as a dictionary'''
        return getattr(self, key)

    def __setitem__(self, key, value):
        '''Allows access to attributes as a dictionary'''
        return setattr(self, key, value)

    def restart(self):
        for prop_name, value in self.defaults.items():
            setattr(self, prop_name, value)


class ComponentFactory(object):
    '''Factory for Component classes
    >>> HealthComponent = ComponentFactory('Health', current=100, max=100)
    >>> HealthComponent
    <class '__main__.Health'>
    '''
    Catalog = {}

    __slots__ = ()

    def __new__(cls, title, **attributes):
        '''Ties name of component to a specific instance, which is shared by
        all fixtures of the same template'''
        # new_class = type(type_name, type_class_bases, type_attributes)
        defaults = dict((k, v) for k, v in attributes.items())
        if title not in cls.Catalog:
            Component.ComponentTypes[title] = cls
            template_cls = type(title, (Component, ), attributes)
            template_cls.Catalog = {}
            template_cls.defaults = defaults
            cls.Catalog[title] = template_cls
        else:
            template_cls = cls.Catalog[title]
            for attr in attributes:
                if not hasattr(template_cls, attr):
                    msg = 'Component attribute mismatch: {} vs {}'
                    msg = msg.format(attributes, template_cls.defaults)
                    raise RuntimeError(msg)
        return template_cls
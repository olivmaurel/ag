from uuid import uuid4
from collections import OrderedDict
from collections import defaultdict
import json
from typing import Any, List, DefaultDict

class Entity(object):
    """
    More or less a container for an id

    Entities have a relationship to their fixtures.

    >>> e = Entity('player', 0)
    >>> e
    <Entity player:0>
    >>> print (e)
    OrderedDict()
    >>> e.heart = 1
    >>> print (e)
    OrderedDict([('heart', 1)])
    >>> print (e['heart'])
    1
    >>> print (e.fixtures)
    OrderedDict([('heart', 1)])
    """
    Catalog = OrderedDict() # type: OrderedDict[Any,Any]

    __slots__ = ['uid', 'name', 'components', 'conditions']

    def __new__(cls, name: str=None, uid: str=None, *args) -> Any:
        '''We only want one entity with the same name
        >>> player1 = Entity('player1')
        >>> player2 = Entity('player2')
        >>> player3 = Entity('player1')
        >>> player1 == player2
        False
        >>> player1 == player3
        True
        '''

        if name not in cls.Catalog:
            entity = super().__new__(cls)
            cls.Catalog[name] = entity
        else:
            entity = cls.Catalog[name]
        return entity

    def __hash__(self):
        return hash(self.uid)

    def __init__(self, name=None, uid=None, *args) -> None:
        self.uid = uuid4() if uid is None else uid
        self.name = name or ''
        self.components = OrderedDict()  # type: OrderedDict[Any,Any]
        self.conditions = defaultdict(int)  # type: DefaultDict[int,Any]

    def __repr__(self) -> str:
        cname = self.__class__.__name__
        name = self.name or self.uid
        if name != self.uid:
            name = '{}'.format(name)
        return '<{} {}>'.format(cname, name)

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, self.__class__):
            return self.uid == other.uid
        elif isinstance(other, self.uid.__class__):
            return self.uid == other
        return False

    def __str__(self) -> str:
        return str(self.components)

    def __getitem__(self, key):
        return self.components[key]

    def __setitem__(self, key, value) -> None:
        self.components[key] = value

    def __getattr__(self, key, *args, **kwds):
        '''Allows access to properties as an attribute:
        '''
        if key in super().__getattribute__('__slots__'):
            return super().__getattribute__(key)
        else:
            try:
                return self.components[key]
            except KeyError:
                return False

    def __delattr__(self, key):

        try:
            return super().__delattr__(key)
        except AttributeError:
            try:
                del self.components[key]
            except KeyError: # if the attr is not in the components dict, turn back to a normal AttributeError
                raise AttributeError


    def __setattr__(self, key, value):
        '''Allows access to the properties/fixtures as an attribute'''

        if key in super(Entity, self).__getattribute__('__slots__'):
            super(Entity, self).__setattr__(key, value)
        else:
            # Create relationships between the entity and fixtures
            if isinstance(value, Component):
                vCatalog = value.__class__.Catalog
                if value.entity is None:
                    value.entity = self
                    # Update the component catalog with the entry
                    for entity, comp in vCatalog.items():
                        if comp == value:
                            if entity in vCatalog:
                                vCatalog.pop(entity)
                            vCatalog[self] = value
            # Even if it is not technically a component, still add it
            #  as a simple 'attribute' component.
            self.components[key] = value


class Component:
    """Contains a set of unique properties
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
    """

    __slots__ = ['entity']

    defaults = OrderedDict()  # type: OrderedDict[Any,Any]
    Catalog = OrderedDict()  # type: OrderedDict[Any,Any]
    ComponentTypes = OrderedDict()  # type: OrderedDict[Any,Any]

    def __new__(cls, entity: Entity=None, *args: List, **properties: dict) -> Any:
        cname = cls.__name__
        if cname not in Component.ComponentTypes:
            Component.ComponentTypes[cname] = cls
            cls.Catalog = OrderedDict()  # type: OrderedDict[Any,Any]
        if entity not in cls.Catalog:
            component = super().__new__(cls)
            cls.Catalog[entity] = component
        else:
            component = cls.Catalog[entity]
        return component

    def __init__(self, entity: str=None, *args: List, **properties: dict) -> None:

        self.entity = entity
        for prop_name, value in self.defaults.items():
            if prop_name in properties.keys():
                value = properties[prop_name]
            setattr(self, prop_name, value)

    def __repr__(self):
        """<Component entity_id>"""
        cname = self.__class__.__name__
        entity_name = ''
        if self.entity:
            for prop_name, component in self.entity.components.items():
                if component == self:
                    entity_name = ' entity:{}.{}'.format(self.entity.name, prop_name)
                    break

        return '<{} : {}>'.format(cname, entity_name)

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


class System(object):
    '''Identifies a set of fixtures that need to be processed

    System has a loose coupling with Components and Entities.
    '''
    components = list() # type: List[str]
    Catalog = OrderedDict()  # type: OrderedDict[Any,Any]

    def __new__(cls, name: str=None, components: list=[]) -> Any:
        '''Add systems to the catalog'''

        name = cls.__name__ if name is None else name

        if name not in System.Catalog:
            system = super().__new__(cls)
            System.Catalog[name] = system
        else:
            system = System.Catalog[name]
        return system

    def __init__(self, name: str=None, components: list=[]) -> None:

        self.name = self.__class__.__name__ if name is None else name
        if components:
            self.components = components

    def __repr__(self) -> str:

        return '<{} : {}>'.format(self.__class__.__name__, self.components)

    @property
    def entities(self) -> list:
        ents = list(set(entity for component_cls in self.component_classes
                        for entity in component_cls.Catalog.keys()
                        if entity is not None))
        return ents

    @property
    def component_classes(self) -> list:
        return list(set(Component.ComponentTypes.get(component_name)
                        for component_name in self.components
                        if component_name in Component.ComponentTypes
                        ))

    def get_components(self):
        '''Creates a dictionary of component classes'''

    def update(self):
        raise NotImplemented('update has not been implemented')


if __name__ == '__main__':
    from doctest import testmod

    testmod()
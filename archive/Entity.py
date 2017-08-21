from uuid import uuid4
from collections import OrderedDict as dict

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
    Catalog = {}

    __slots__ = ['uid', 'name', 'components']

    def __new__(cls, name=None, uid=None):
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
            entity = super(Entity, cls).__new__(cls)
            cls.Catalog[name] = entity
        else:
            entity = cls.Catalog[name]
        return entity

    def __hash__(self):
        return hash(self.uid)

    def __init__(self, name=None, uid=None):
        self.uid = uuid4() if uid is None else uid
        self.name = name or ''
        self.components = dict()

    def __repr__(self):
        cname = self.__class__.__name__
        name = self.name or self.uid
        if name != self.uid:
            name = '{}:{}'.format(name, self.uid)
        return  '<{} {}>'.format(cname, name)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.uid == other.uid
        elif isinstance(other, self.uid.__class__):
            return self.uid == other
        return False

    def __str__(self):
        return str(self.components)

    def __getitem__(self, key):
        return self.components[key]

    def __setitem__(self, key, value):
        self.components[key] = value

    def __getattr__(self, key, *args, **kwds):
        '''Allows access to properties as an attribute:
        '''
        if key in super().__getattribute__('__slots__'):
            return super().__getattribute__(key)
        else:
            return self.components[key]

    def __setattr__(self,key, value):
        '''Allows access to the properties/fixtures as an attribute'''
        from ag.Component import Component

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


if __name__ == '__main__':
    from doctest import testmod

    testmod()


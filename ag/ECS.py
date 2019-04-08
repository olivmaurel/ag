from uuid import uuid4
from collections import OrderedDict
from collections import defaultdict
import json
from typing import Any, List, Union


class Entity(object):

    Catalog = OrderedDict()

    __slots__ = ['uid', 'name', 'components', 'conditions', 'properties']

    def __new__(cls, name: str = None, uid: str = None, *args) -> Any:

        if name not in cls.Catalog:
            entity = super().__new__(cls)
            cls.Catalog[name] = entity
        else:
            entity = cls.Catalog[name]
        return entity

    def __hash__(self):
        return hash(self.uid)

    def __init__(self, name=None, uid=None, *args) -> None:
        self.uid = uid or uuid4()
        self.name = name or ''
        self.components = OrderedDict()
        self.conditions = defaultdict(int)
        self.properties = OrderedDict()

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
        return self.__repr__()

    def __getitem__(self, key):
        return self.components[key]

    def __setitem__(self, key, value) -> None:
        self.components[key] = value

    def __getattr__(self, key, *args, **kwds):

        if key in super().__getattribute__('__slots__'):
            return super().__getattribute__(key)
        elif key in self.properties.keys():
            return self.properties[key]
        else:
            try:
                return self.components[key]
            except KeyError:
                return False

    def __delattr__(self, key):

        if key in self.properties.keys():
            del self.properties[key]
        else:
            try:
                return super().__delattr__(key)
            except AttributeError:
                try:
                    del self.components[key]
                # if the attr is not in the components dict, turn back to a normal AttributeError
                except KeyError:
                    raise AttributeError

    def __setattr__(self, key, value):

        if key in super(Entity, self).__getattribute__('__slots__'):
            super(Entity, self).__setattr__(key, value)
        else:
            # Create relationships between the entity and fixtures
            if isinstance(value, Component):
                v_catalog = value.__class__.Catalog
                if value.entity is None:
                    value.entity = self
                    # Update the component catalog with the entry
                    for entity, comp in v_catalog.items():
                        if comp == value:
                            if entity in v_catalog:
                                v_catalog.pop(entity)
                            v_catalog[self] = value
                self.components[key] = value
            # Even if it is not technically a component, still add it
            #  as a simple 'property'.
            else:
                self.properties[key] = value


class Component:

    __slots__ = ['entity', 'Catalog']

    defaults = OrderedDict()
    ComponentTypes = OrderedDict()

    def __new__(cls, entity: Entity = None, *args: List, **properties: dict) -> Any:
        cname = cls.__name__
        if cname not in Component.ComponentTypes:
            Component.ComponentTypes[cname] = cls
            cls.Catalog = OrderedDict()
        if entity not in cls.Catalog:
            component = super().__new__(cls)
            cls.Catalog[entity] = component
        else:
            component = cls.Catalog[entity]
        return component

    def __init__(self, entity: Union[Entity, str] = None, *args: List, **properties: dict) -> None:

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

        return getattr(self, key)

    def __setitem__(self, key, value):

        return setattr(self, key, value)


class System(object):

    components = []
    Catalog = OrderedDict()

    def __new__(cls, name: str = None, components: list = None) -> Any:

        name = cls.__name__ if name is None else name

        if name not in System.Catalog:
            system = super().__new__(cls)
            System.Catalog[name] = system
        else:
            system = System.Catalog[name]
        return system

    def __init__(self, name: str = None, components: list = None) -> None:
        self.name = self.__class__.__name__ if name is None else name
        if components:
            self.components = components

    def __repr__(self) -> str:
        return '<{} : {}>'.format(self.__class__.__name__, self.components)

    @property
    def entities(self) -> list:
        return list(set(entity for component_cls in self.component_classes
                        for entity in component_cls.Catalog.keys()
                        if entity is not None))

    @property
    def component_classes(self) -> list:
        return list(set(Component.ComponentTypes.get(component_name)
                        for component_name in self.components
                        if component_name in Component.ComponentTypes
                        ))

    def update(self):
        raise NotImplemented('update has not been implemented')

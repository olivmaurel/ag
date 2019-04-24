from ag.ECS import Entity
from ag.settings import *


class Error(Exception):
    """Base class for other exceptions"""
    def __init__(self, msg):
        logging.error(msg)
        Exception.__init__(self, msg)


class EmptyContainerException(Error):
    """When a char tries to empty an empty container"""
    def __init__(self, e: Entity):
        msg = "{} is empty".format(e.name)
        Error.__init__(self, msg)


class MixedLiquidsException(Error):
    def __init__(self, container, other_liquid: Entity):
        msg = "Cannot mix {} and {} in {}".format(container.content.name, other_liquid.name, container.entity.name)
        Error.__init__(self, msg)


class NoSuchComponentException(Error):
    """When a function cannot be executed if a component is missing, stop here"""
    def __init__(self, component: str, e: Entity):
        msg = "The component {} is missing from {} (uid:{})".format(component, e.name, e.uid)
        Error.__init__(self, msg)


class NoSuchPropertyException(Error):
    def __init__(self, prop: str, e: Entity):
        msg = "The property {} is missing from {} (uid:{})".format(prop, e.name, e.uid)
        Error.__init__(self, msg)


class DifferentPositionException(Error):

    def __init__(self, e: Entity, other: Entity):
        msg = "The entities cannot interact, the positions are different on the map {} and {}".format(e.pos, other.pos)
        Error.__init__(self, msg)


class ActionNotFoundError(Error):

    def __init__(self, action: str):
        msg = "The action {} is not registered in the system".format(action)
        Error.__init__(self, msg)

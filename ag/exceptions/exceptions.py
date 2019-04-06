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
    def __init__(self, item: Entity, other_liquid: Entity):
        msg = "Cannot mix {} and {} in {}".format(item.content.name, other_liquid.name, item.entity.name)
        Error.__init__(self, msg)


class NoSuchComponentException(Error):
    """When a function cannot be executed if a component is missing, stop here"""
    def __init__(self, component: str, e: Entity):
        msg = "The component {} is missing from {} (uid:{})".format(component, e.name, e.uid)
        Error.__init__(self, msg)
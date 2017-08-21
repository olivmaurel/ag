class System(object):
    '''Identifies a set of fixtures that need to be processed

    System has a loose coupling with Components and Entities.
    '''
    components = []
    Catalog = {}

    def __new__(cls, name=None, components=[]):
        '''Add systems to the catalog'''
        name = cls.__name__ if name is None else name
        if name not in System.Catalog:
            system = super().__new__(cls)
            System.Catalog[name] = system
        else:
            system = System.Catalog[name]
        return system

    def __init__(self, name=None, components=[]):
        self.name = name
        if components:
            self.components = components

    def __repr__(self):
        cname = self.__class__.__name__
        name = self.name
        return '<{} {}>'.format(cname, name)

    @property
    def entities(self):
        ents = list(set(entity for component_cls in self.component_classes
                        for entity in component_cls.Catalog.keys()
                        if entity is not None))
        return ents

    @property
    def component_classes(self):
        return list(set(Component.ComponentTypes.get(component_name)
                        for component_name in self.components
                        if component_name in Component.ComponentTypes
                        ))

    def get_components(self):
        '''Creates a dictionary of component classes'''

    def update(self, dt=None):
        raise NotImplemented('update has not been implemented')


class CombatSystem(System):
    '''
    >>> from ag.Entity import Entity
    >>> from ag.Component import Component
    >>> from ag.fixtures import Health, Damage
    >>> player = Entity('player')
    >>> skeleton = Entity('skeleton')
    >>> player.health = Health()
    >>> player.damage = Damage()
    >>> skeleton.health = Health()
    >>> skeleton.damage = Damage()

    >>> combat_sim  = CombatSystem()
    >>> player.health.current
    100
    >>> skeleton.health.current
    100
    >>> combat_sim.update()

    >>> player.health.current
    90
    >>> skeleton.health.current
    1
    '''
    components = ['Health', 'Damage']
    def update(self, dt=None):
        '''Updates the relevant data'''
        entityA, entityB = self.entities
        entityA.health.current -= entityB.damage
        entityB.health.current -= entityA.damage

if __name__ == '__main__':
    from doctest import testmod

    testmod()


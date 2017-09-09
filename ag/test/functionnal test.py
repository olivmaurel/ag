from ag.factory import Factory
from ag.components import *
from ag.systems import *
from ag.ECS import *
import ag.components

factory = Factory()


island = factory.area_creation(pos=(1, 2),
                      name='Skull Island',
                      terrain='island',
                      climate='tropical')

skeleton = factory.entity_creation('skeleton', components=['health'])
albonpin = factory.human_creation('albonpin')
pouch = factory.item_creation('container', 'pouch')

factory.assign_component(skeleton, 'geo')


skeleton.enter_area(island)
albonpin.enter_area(island)

print(island.entities)

bio_s = BiologicalNeedsSystem()

world = factory.world_system_creation()

pouch = factory.item_creation('container', 'pouch')

print(albonpin.inv)
# {}
albonpin.pickup(pouch) # todo

print(albonpin.inv)
# {pouch}
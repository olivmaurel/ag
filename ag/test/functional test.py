from ag.factory import Factory
from ag.components import *
from ag.systems import *
from ag.ECS import *
import ag.components

factory = Factory()
pouch = factory.item_creation('container', 'pouch')

island = factory.area_creation(loc=(1, 2),
                               name='Skull Island',
                               terrain='island',
                               climate='tropical')

skeleton = factory.entity_creation('skeleton', components=['health'])
albonpin = factory.human_creation('albonpin')
albonpin.enter_area(island)
pouch = factory.item_creation('container', 'pouch')

albonpin.pickup(pouch)



factory.assign_component(skeleton, 'geo')


skeleton.enter_area(island)
albonpin.enter_area(island)

print(island.entities)

bio_s = BiologicalNeedsSystem()

world = factory.world_system_creation()



print(albonpin.inv)
# {}
albonpin.pickup(pouch) # todo

print(albonpin.inv)
# {pouch}
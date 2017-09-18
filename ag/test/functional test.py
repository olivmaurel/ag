from ag.factory import Factory
from ag.components import *
from ag.systems import *
from ag.ECS import *
import ag.components

factory = Factory()
world = factory.world_system_creation()

island = factory.area_creation(pos=(1, 2),
                               name='Skull Island',
                               terrain='island',
                               climate='tropical')
world.map[island.pos] = island
world.set_active_area(island.pos)



skeleton = factory.entity_creation('skeleton', components=['health'])
albonpin = factory.human_creation('albonpin')
albonpin.enter_area(island)

pouch = factory.item_creation('container', 'pouch')
amphora = factory.item_creation('container', 'amphora')

albonpin.pickup(pouch)
albonpin.pickup(amphora)
water_supply = albonpin.locate('WaterSupply')
albonpin.moveto(water_supply)
albonpin.fill(pouch, 'water')
albonpin.drink(pouch)

albonpin.locate(Liquid, 'oil')
albonpin.fill(amphora, 'oil')
albonpin.drink(amphora) # false

factory.assign_component(skeleton, 'geo')


skeleton.enter_area(island)
albonpin.enter_area(island)

print(island.entities)

bio_s = BiologicalNeedsSystem()




print(albonpin.inv)
# {}
albonpin.pickup(pouch) # todo

print(albonpin.inv)
# {pouch}
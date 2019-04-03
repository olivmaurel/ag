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

mountains = factory.area_creation(pos=(1, 1),
                               name='Black Mountains',
                               terrain='mountains',
                               climate='alpine')

world.map[island.pos] = island
world.map[mountains.pos] = mountains



world.set_active_area(island)
world.set_active_area(mountains)
world.set_active_area(island)


albonpin = factory.human_creation('albonpin')
grok = factory.human_creation('grok')
skeleton = factory.entity_creation('skeleton', components=['health', 'geo', 'mov'])

albonpin.enter_area(island, pos=(1, 1))
grok.enter_area(island, pos=(1, 1))
skeleton.enter_area(island, pos=(1, 2))
grok.enter_area(mountains, pos=(1, 1))



# todo 2) biosystem updates everybody, not just within the area



for i in range(20): # 0680191N
    island.update()

assert albonpin.thirst.status == 'parched'

pouch = factory.item_creation('container', 'pouch')
amphora = factory.item_creation('container', 'amphora')
cask = factory.item_creation('container', 'cask')
albonpin.moveto((0,0))
albonpin.pickup(pouch)
albonpin.pickup(amphora)

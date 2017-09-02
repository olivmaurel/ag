from ag.Factory import Factory
from ag.components import *
from ag.systems import *
from ag.ECS import *
import ag.components

factory = Factory()


island = factory.area(pos=(1, 2),
                      name='Skull Island',
                      terrain='island',
                      climate='tropical')

skeleton = factory.entity('skeleton', components=['health'])
albonpin = factory.human('albonpin')

factory.assign_component(skeleton, 'geo')

skeleton.enter_area(island)
albonpin.enter_area(island)

print(island.entities)

bio_s = BiologicalNeedsSystem()

world = factory.make_world_system()

world.active_area = island


for i in range(100):
    for sys in a.systems:
        sys.update()

assert skeleton.health.alive is True


skeleton.enter_area(skeleton, island)
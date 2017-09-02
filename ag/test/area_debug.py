from ag.Factory import Factory
from ag.components import *
from ag.systems import *
from ag.ECS import *
import ag.components

factory = Factory()

first = Entity('first')


island = factory.area(geo={'area':(1, 2), 'local': (0, 0)},
                      terrain='island',
                      climate='tropical')

albonpin = factory.human('albonpin')
skeleton = factory.entity('skeleton', components=['health'])

world = factory.make_world_system()

bio_s = BiologicalNeedsSystem()
world.add_system(world.active_coords, bio_s)

a = world.active_area
for i in range(100):
    for sys in a.systems:
        sys.update()

assert albonpin.health.alive is False
assert skeleton.health.alive is True

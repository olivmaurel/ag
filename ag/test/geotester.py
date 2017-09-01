from ag.Factory import Factory
from ag.components import *
from ag.systems import *
from ag.ECS import *
import ag.components

factory = Factory()


island = factory.make_area(geo=[{'coords':{'area':(1, 2),
                                           'local': (0, 0)}}
                                ],
                           terrain='island',
                           climate='tropical')

skeleton = factory.make_entity('skeleton', components=['health'])

factory.assign_component(skeleton, 'geo')



world = factory.make_world_system()

bio_s = BiologicalNeedsSystem()
world.add_system(world.active_coords, bio_s)

a = world.active_area
for i in range(100):
    for sys in a.systems:
        sys.update()

assert skeleton.health.alive is True


skeleton.enter_area(skeleton, island)
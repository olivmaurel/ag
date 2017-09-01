from ag.Factory import Factory
from ag.components import *
from ag.systems import *
from ag.ECS import *

factory = Factory()


world = factory.make_world_system()

mountains = factory.make_area('mountain_range', 'mountains', 'alpine')
island = factory.make_area('treasure island', 'island', 'tropical')

assert island.active == False
assert mountains.active == True

e = factory.make_human('e')
skeleton = factory.make_entity('skeleton', ['health'])


for i in range(100):
    world.update()

assert e.health.alive == False
assert skeleton.health.alive


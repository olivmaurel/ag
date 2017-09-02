from ag.Factory import Factory
from ag.components import *
from ag.systems import *
from ag.ECS import *

factory = Factory()


world = factory.make_world_system()

mountains = factory.area('mountain_range', 'mountains', 'alpine')
island = factory.area('treasure island', 'island', 'tropical')

assert island.active == False
assert mountains.active == True

e = factory.human('e')
skeleton = factory.entity('skeleton', ['health'])


for i in range(100):
    world.update()

assert e.health.alive == False
assert skeleton.health.alive


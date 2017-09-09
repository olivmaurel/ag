from ag.factory import Factory
from ag.components import *
from ag.systems import *
from ag.ECS import *

factory = Factory()


world = factory.world_system_creation()

mountains = factory.area_creation('mountain_range', 'mountains', 'alpine')
island = factory.area_creation('treasure island', 'island', 'tropical')

assert island.active == False
assert mountains.active == True

e = factory.human_creation('e')
skeleton = factory.entity_creation('skeleton', ['health'])


for i in range(100):
    world.update()

assert e.health.alive == False
assert skeleton.health.alive


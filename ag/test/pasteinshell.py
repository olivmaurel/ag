from ag.Factory import GameObjectFactory
from ag.components import *
from ag.systems import BiologicalNeedsSystem

factory = GameObjectFactory()

w = factory.make_world('world', 4, 4)
w.add_system(BiologicalNeedsSystem())

player = factory.make_human('player')
skeleton = factory.make_object('skeleton', components=[Health()])

active_area = w.map.grid[(0,0)][0]

for i in range(100):
    w.update()
    if not player.health.alive:
        break

print(player.health.current)
print(player.hunger.status)
print(player.thirst.status)
print(player.health.alive)


########

from ag.ECS import *
from ag.components import *

e = Entity('area')
t = Terrain(e, 'mountains')

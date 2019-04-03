from ag.factory import Factory

factory = Factory()


world = factory.world_system_creation()

mountains = factory.area_creation('mountain range', (0, 0), 'mountains', 'alpine')
island = factory.area_creation('treasure island', (0, 1), 'island', 'tropical')

world.add_area(mountains)

world.set_active_area((0, 0))

assert island.active is False
assert mountains.active is True

e = factory.human_creation('e')
skeleton = factory.entity_creation('skeleton', ['health'])


for i in range(100):
    print(e.health.status)
    world.update()

assert e.health.alive is False
assert skeleton.health.alive


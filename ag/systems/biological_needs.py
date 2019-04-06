from ag.ECS import System


class BiologicalNeedsSystem(System):

    components = ['Hunger', 'Thirst']

    def __init__(self, name="Biological system", components=[]):
        super().__init__(name, components)

    def update(self):

        for e in self.entities:

            if e.hunger:
                if e.hunger.current >= 5:
                    e.hunger.current -= 5
                status = e.hunger.status
                if e.hunger.current <= 50:
                    e.conditions['thirsty'] = True
                if status == 'famished':
                    e.conditions['malnourished'] += 1
                if status == 'starving':
                    e.conditions['malnourished'] += 2
                    if e.health:
                        e.health.change(-10)
            if e.thirst:
                if e.thirst.current >= 5:
                    e.thirst.current -= 5
                status = e.thirst.status
                if status == 'dehydrated':
                    e.conditions['dehydrated'] += 1
                if status == 'parched':
                    e.conditions['dehydrated'] += 2
                    if e.health:
                        e.health.change(-10)
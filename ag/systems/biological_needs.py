from ag.ECS import System


class BiologicalNeedsSystem(System):

    components = ['Hunger', 'Thirst']

    def __init__(self, name="Biological system", components=None):
        super().__init__(name, components)

    def update(self):

        for e in self.entities:

            self.hunger_tick(e)
            self.thirst_tick(e)



    @staticmethod
    def hunger_tick(entity):

        if entity.hunger:
            if entity.hunger.current >= 5:
                entity.hunger.current -= 5
            status = entity.hunger.status
            if entity.hunger.current <= 50:
                entity.conditions['hungry'] = True
            if status == 'famished':
                entity.conditions['malnourished'] += 1
            if status == 'starving':
                entity.conditions['malnourished'] += 2
                if entity.health:
                    entity.health.change(-10)

    @staticmethod
    def thirst_tick(entity):
        if entity.thirst:
            if entity.thirst.current >= 5:
                entity.thirst.current -= 5
            status = entity.thirst.status
            if entity.thirst.current <= 50:
                entity.conditions['thirsty'] = True
            if status == 'dehydrated':
                entity.conditions['dehydrated'] += 1
            if status == 'parched':
                entity.conditions['dehydrated'] += 2
                if entity.health:
                    entity.health.change(-10)
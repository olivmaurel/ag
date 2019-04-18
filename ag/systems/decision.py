from ag.ECS import System


class DecisionSystem(System):

    components = ['Hunger', 'Thirst']

    def __init__(self, name="Decision System", components=None):
        super().__init__(name, components)

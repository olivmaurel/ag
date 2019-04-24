from ag.ECS import System
from ag.actions.drink_action import DrinkAction
from ag.exceptions.exceptions import ActionNotFoundError


class ActionSystem(System):

    def __init__(self, name="Action System", components=None):
        super().__init__(name, components)
        self.actions = dict()
        self.actions['drink'] = DrinkAction()

    def execute(self, action_name: str):
        if action_name in self.actions:
            action = self.actions[action_name]
            return action.execute()
        else:
            raise ActionNotFoundError(action_name)




# class ActionsCatalogue(object):


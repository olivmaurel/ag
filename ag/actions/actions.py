from abc import abstractmethod


class Action(object):

    @abstractmethod
    def execute(self):
        raise NotImplementedError('Action not executable!')

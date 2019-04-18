from ag.ECS import System


class StrategySystem(System):

    components = ['geo']

    def update(self):
        raise NotImplementedError('Not implemented')

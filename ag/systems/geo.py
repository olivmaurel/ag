from ag.ECS import System


class GeoSystem(System):

    components = ['geo']

    def update(self):
        raise NotImplementedError('Not implemented')

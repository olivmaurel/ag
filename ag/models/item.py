from ag.ECS import Entity
from uuid import uuid4


class Item(Entity):
    """
    convert yml mapping into object ready to instanciate as Entity with Components
    """

    def __init__(self, name: str, uid: uuid4(), ml_ref: dict, *args):
        super().__init__(name, uid, *args)

        for k, v in ml_ref.items():
            if not hasattr(self, k) or self.k == False:
                self.__setattr__(k, v)

    def __repr__(self):
        return '[{}] {}'.format(self.type, self.name)

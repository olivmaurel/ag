from typing import List

class MyGeo(object):

    defaults = dict([('avalue', 1), ('area', (0, 0)), ('local', (0, 0))])

    def __init__(self, entity: str=None, *args: List, **properties: dict) -> None:

        self.entity = entity
        for prop_name, value in self.defaults.items():
            if prop_name in properties.keys():
                value = properties[prop_name]
            setattr(self, prop_name, value)
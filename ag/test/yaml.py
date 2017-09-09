import yaml
from ag.factory import Factory


factory = Factory()


def parse_yaml(file):
    y = ""
    with open(file, "r") as stream:
        try:
            y = yaml.load_all(stream)
        except yaml.YAMLError as exc:
            return exc
    return y

def get_consumable():
    y = parse_yaml("ag/fixtures/ml_consumable.yml")
    # transform parsed yaml string into entity with attached components
    consumable = factory.consumable_creation(y)


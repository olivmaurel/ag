# YAML fixtures
import yaml
from ag.Factory import Factory


factory = Factory()


def parse_yaml(file):

    with open(file, "r") as stream:
        try:
            print(yaml.load_all(stream))
        except yaml.YAMLError as exc:
            print(exc)
    y = ""
    return y


def get_consumable():
    y = parse_yaml("ag/fixtures/consumables.yml")
    # transform parsed yaml string into entity with attached components
    consumable = factory.consumable(y)





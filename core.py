import yaml


# YAML fixtures
def parse_yaml(file):

    with open(file, "r") as stream:
        try:
            yaml.load_all(stream, Loader=yaml.SafeLoader)
        except yaml.YAMLError as exc:
            return exc


def get_yaml_as_dict(filepath):
    y = {}
    with open(filepath, "r") as stream:
        for name in yaml.load_all(stream, Loader=yaml.SafeLoader):
            for k,v in name.items():
                y[k] = v

    return y
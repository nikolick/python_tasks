# create configuration class that can be used to access configuration through attributes.
# Configuration data can be passed in yaml or json format.
# e.g config.a.b.c < = > config[‘a’][‘b’][‘c’] < = > config[‘a’].b.c < = > config.a[‘b.c’] < = > config[‘a.b.c’]
# Tips: try to implement __getattr__ and __getitem__ magic methods.

from os import strerror
import json


class Config:
    def __init__(self, attr_dict: dict):
        # self.__dict__ = attr_dict
        for k, v in attr_dict.items():
            if isinstance(v, dict):
                v = Config(v)
            type(self).__setattr__(self, k, v)

    def __getitem__(self, item):
        return self.__dict__[item]

    def __str__(self):
        return str(self.__dict__)


def load_json(fpath):
    try:
        with open(fpath, 'r') as obj_file:
            return json.load(obj_file)
    except (IOError, OSError) as e:
        print("Failed to open/read file")
        print(strerror(e.errno))
    except json.JSONDecodeError as jse:
        print("Invalid JSON file")
        print(jse)


if __name__ == '__main__':
    object_as_dict = load_json("object.json")
    conf = Config(object_as_dict)

    print(conf['b.c'])
#    print(conf['b'])

#    print(object_as_dict['niz'][0])

import json

from utils.Utils import readFile, writeFile


class Config:
    def __init__(self, path: str, defaults: dict):
        self.path = path
        self.defaults = defaults if defaults else {}
        self.data = self.read(path)

    def get(self, property_name):
        if property_name in self.data:
            return self.data[property_name]
        elif property_name in self.defaults:
            return self.defaults[property_name]
        else:
            return None

    def set(self, property_name, value):
        self.data[property_name] = value
        self.write(self.path, self.data)

    @staticmethod
    def read(path):
        cfgString = readFile(path)
        return json.loads(cfgString) if cfgString else {}

    @staticmethod
    def write(path, data):
        dump = json.dumps(data, sort_keys=True, indent=4)
        print("save config:\n", dump, "\n")
        writeFile(path, dump)

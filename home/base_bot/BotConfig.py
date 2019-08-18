import json


class BotConfig:
    def __init__(self, path):
        file = open(path)

        self.__data = json.loads(file.read())

        file.close()

    def get(self, prop):
        return self.__data.get(prop, None)

    @property
    def bot_token(self):
        return self.__data.get("bot_token", None)

    @property
    def use_proxy(self):
        return self.__data.get("use_proxy", None)

    @property
    def superuser(self):
        return self.__data.get("superuser", None)

import json
import os

from telegram.ext import Updater

import proxy


class Config:
    def __init__(self):
        path = os.path.join("config.json")
        file = open(path)

        self.__data = json.loads(file.read())

        file.close()

    def get(self, prop):
        return self.__data.get(prop, None)

    @property
    def bot_token(self):
        return self.__data.get("bot_token", None)

    @property
    def steam_api(self):
        return self.__data.get("steam_api", None)

    @property
    def use_proxy(self):
        return self.__data.get("use_proxy", None)

    @property
    def superuser(self):
        return self.__data.get("superuser", None)

    @property
    def steam_request_delay(self):
        return self.__data.get("steam_request_delay", None)


class Env:
    def __init__(self):
        self.config = Config()

        REQUEST_KWARGS = {}
        if self.config.use_proxy:
            REQUEST_KWARGS.update({'proxy_url': proxy.get_proxy()})

        self.updater = Updater(self.config.bot_token, request_kwargs=REQUEST_KWARGS, use_context=True)
        self.dispatcher = self.updater.dispatcher

from telegram.ext import Updater

import proxy


class BotEnv:
    def __init__(self, config):
        self.config = config

        REQUEST_KWARGS = {}
        if self.config.use_proxy:
            REQUEST_KWARGS.update({'proxy_url': proxy.get_proxy()})

        self.updater = Updater(self.config.bot_token, request_kwargs=REQUEST_KWARGS, use_context=True)
        self.dispatcher = self.updater.dispatcher

from telegram.ext import Updater, Dispatcher

from home_bot import proxy
from home_bot.config import BOT_TOKEN

REQUEST_KWARGS = {'proxy_url': proxy.get_proxy()}


class Env:
    def __init__(self):
        self.updater: Updater = Updater(BOT_TOKEN, request_kwargs=REQUEST_KWARGS, use_context=True)
        self.dispatcher: Dispatcher = self.updater.dispatcher

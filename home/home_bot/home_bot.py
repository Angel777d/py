import logging
import os

import OpenHandler
import UnknownHandler
from BotConfig import BotConfig
from BotEnv import BotEnv


def run():
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

    config_path = os.path.join("config.json")
    env = BotEnv(BotConfig(config_path))

    # open remove link
    OpenHandler.init(env)

    # Must be the last handler
    UnknownHandler.init(env)

    # start bot
    env.updater.start_polling()

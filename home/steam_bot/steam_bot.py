import logging
import os

import SteamHandler
import UnknownHandler
from BorEnv import BotEnv
from SteamBotConfig import SteamBotConfig


def run():
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

    config_path = os.path.join("config.json")
    env = BotEnv(SteamBotConfig(config_path))

    # Steam commands
    SteamHandler.init(env)

    # Must be the last handler
    UnknownHandler.init(env)

    # start bot
    env.updater.start_polling()

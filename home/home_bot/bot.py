import logging

from env import Env
from handlers import BasicCommandsHandler, OpenHandler, UnknownHandler
from handlers.steam import SteamHandler


def run():
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

    env = Env()

    # basic commands
    BasicCommandsHandler.init(env)

    # tutorial items
    # EchoHandler.init(dispatcher)
    # CapsHandler.init(dispatcher)

    # project handlers
    OpenHandler.init(env)
    SteamHandler.init(env)

    # inline functions
    # InlineHandler.init(dispatcher)

    # Note: This handler must be added last.
    # If you added it sooner, it would be triggered before the CommandHandlers had a chance to look at the update.
    # Once an update is handled, all further handlers are ignored.
    # To circumvent this, you can pass the keyword argument group (int) to add_handler with a value other than 0.
    UnknownHandler.init(env)

    # start bot
    env.updater.start_polling()

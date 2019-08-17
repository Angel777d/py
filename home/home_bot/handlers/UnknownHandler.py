from telegram import Update
from telegram.ext import CallbackContext, MessageHandler, Filters

from env import Env


class UnknownHandler:

    def get_handler(self):
        return MessageHandler(Filters.command, self.handle)

    def handle(self, update: Update, context: CallbackContext):
        context.bot.send_message(chat_id=update.message.chat_id, text="Sorry, I didn't understand that command.")


def init(env: Env):
    env.dispatcher.add_handler(UnknownHandler().get_handler())

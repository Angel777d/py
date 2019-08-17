import logging

from telegram import Update
from telegram.ext import CommandHandler, CallbackContext

from env import Env


class StartHandler:
    def get_handler(self):
        return CommandHandler('start', self.handle)

    def handle(self, update: Update, context: CallbackContext):
        logging.log(logging.INFO, "/start  called")
        message = update.message
        chat_id = message.chat_id
        context.bot.send_message(chat_id=chat_id, text="I'm a bot, please talk to me!")


class HelpHandler:
    def get_handler(self):
        return CommandHandler('help', self.handle)

    def handle(self, update: Update, context: CallbackContext):
        logging.log(logging.INFO, "/help  called")
        context.bot.send_message(chat_id=update.message.chat_id, text="Help placeholder")


class SettingsHandler:
    def get_handler(self):
        return CommandHandler('settings', self.handle)

    def handle(self, update: Update, context: CallbackContext):
        logging.log(logging.INFO, "/settings  called")
        context.bot.send_message(chat_id=update.message.chat_id, text="settings placeholder")


def init(env: Env):
    env.dispatcher.add_handler(StartHandler().get_handler())
    env.dispatcher.add_handler(HelpHandler().get_handler())
    env.dispatcher.add_handler(SettingsHandler().get_handler())

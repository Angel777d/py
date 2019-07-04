import logging

from telegram import Update
from telegram.ext import CommandHandler, CallbackContext, Dispatcher


class CapsHandler:
    def get_handler(self):
        return CommandHandler('caps', self.handle)

    def handle(self, update: Update, context: CallbackContext):
        logging.log(logging.INFO, "/caps  called")
        text_caps = ' '.join(context.args).upper()
        context.bot.send_message(chat_id=update.message.chat_id, text=text_caps)


def init(dispatcher: Dispatcher):
    dispatcher.add_handler(CapsHandler().get_handler())

import logging

from telegram import Update
from telegram.ext import CallbackContext, MessageHandler, Filters, Dispatcher


class EchoHandler:
    def get_handler(self):
        return MessageHandler(Filters.text, self.handle)

    def handle(self, update: Update, context: CallbackContext):
        logging.log(logging.INFO, "/echo  called", update.message.text)
        context.bot.send_message(chat_id=update.message.chat_id, text=update.message.text)


def init(dispatcher: Dispatcher):
    dispatcher.add_handler(EchoHandler().get_handler())

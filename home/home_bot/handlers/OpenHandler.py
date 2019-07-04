import os
import subprocess
import sys

from telegram import Update
from telegram.ext import CommandHandler, CallbackContext

from home_bot.env import Env

ALLOWED_USERS = ["173774267"]


class OpenHandler:

    def get_handler(self):
        return CommandHandler("open", self.handle)

    def handle(self, update: Update, context: CallbackContext):
        if update.message.from_user.id not in ALLOWED_USERS:
            return "You are not allowed"

        url = ' '.join(context.args)
        context.bot.send_message(chat_id=update.message.chat_id, text="open a link: " + url)

        if not url.startswith("http"):
            url = "http://" + url

        if sys.platform == 'win32':
            os.startfile(url)
        elif sys.platform == 'darwin':
            subprocess.Popen(['open', url])
        else:
            try:
                subprocess.Popen(['xdg-open', url])
            except OSError:
                print('Please open a browser on:', url)


def init(env: Env):
    env.dispatcher.add_handler(OpenHandler().get_handler())

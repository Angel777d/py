import json

from telegram_api import API
from telegram_api import Pooling
from telegram_api import Update

print("Good morning, master.")


class ButlerBot:
	def __init__(self, config):
		self.config = config
		self.api = API(config.get("token"))
		self.pooling = Pooling(self.api, self.handler, 1)
		self.pooling.start()

	def handler(self, update: Update):
		pass


with open("config.json") as json_data_file:
	config = json.load(json_data_file)

bot = ButlerBot(config)

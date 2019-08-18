import logging
import sqlite3
import threading
from functools import partial
from time import sleep

from telegram import Update
from telegram.ext import CommandHandler, CallbackContext

import SteamMessages
import steam_api
from BorEnv import BotEnv


class SteamStorage:
    def __init__(self, path: str):
        self.path = path
        self.conn = None
        self.cursor = None

    def init(self):
        self.conn = sqlite3.connect(self.path)
        self.cursor = self.conn.cursor()

    def fini(self):
        self.cursor.close()
        self.cursor = None
        self.conn.close()
        self.conn = None

    def create_table(self):
        self.cursor.execute(
            """ CREATE TABLE IF NOT EXISTS steam_service (
                uid INTEGER UNIQUE, 
                steam_id TEXT, 
                chat_id TEXT, 
                language_code TEXT, 
                enabled INTEGER
            ) """
        )

    def insert(self, uid, steam_id, chat_id, language_code):
        sql = """   INSERT INTO steam_service(uid, steam_id, chat_id, language_code, enabled) 
                    VALUES (?, ?, ?, ?, ?)"""
        self.cursor.execute(sql, (uid, steam_id, chat_id, language_code, 1))
        self.conn.commit()

    def update_enabled(self, uid, enabled):
        sql = "UPDATE steam_service SET enabled=?  WHERE uid=?"
        self.cursor.execute(sql, (1 if enabled else 0, uid))
        self.conn.commit()

    def get(self, uid):
        sql = "SELECT * FROM steam_service WHERE uid=?"
        self.cursor.execute(sql, [uid])
        result = self.cursor.fetchone()
        return result

    def get_active(self):
        sql = "SELECT * FROM steam_service WHERE enabled=1"
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        return result

    def delete(self, uid):
        sql = "DELETE FROM steam_service WHERE uid=?"
        self.cursor.execute(sql, [uid])


class SteamService:
    def __init__(self, env: BotEnv):
        self.updater = env.updater
        self.storage = SteamStorage("mydatabase.db")
        self.commands = []
        self.delay = env.config.steam_request_delay

        env.dispatcher.add_handler(CommandHandler('help', partial(self.handle, "help")))
        env.dispatcher.add_handler(CommandHandler('start', partial(self.handle, "start")))
        env.dispatcher.add_handler(CommandHandler('stop', partial(self.handle, "stop")))
        env.dispatcher.add_handler(CommandHandler('settings', partial(self.handle, "settings")))
        env.dispatcher.add_handler(CommandHandler('remove', partial(self.handle, "remove")))
        env.dispatcher.add_handler(CommandHandler('reload', partial(self.handle, "reload")))

    def run(self):
        self.storage.init()
        self.storage.create_table()
        while True:
            self.process_commands()

            active = self.storage.get_active()
            steam_ids = [steam_id for _, steam_id, _, _, _ in active]
            steam_players = steam_api.get_players(steam_ids)

            for uid, steam_id, chat_id, language_code, enabled in active:
                player = steam_players[steam_id]
                self.send_note(player, chat_id, language_code)

            sleep(self.delay)

    def handle(self, command: str, update: Update, context: CallbackContext):
        logging.log(logging.INFO, "/%s called. args: %s", command, context.args)
        self.commands.append((command, update, context))

    def process_commands(self):
        for command, update, context in self.commands:

            # to avoid "edit message" cases
            if not update.message:
                # print("something wrong with message", update)
                continue

            parse_mode = None
            if command == "help":
                result = self.info()
            elif command == "start":
                result, parse_mode = self.process_start(update, context)
            elif command == "stop":
                result = self.process_stop(update)
            elif command == "settings":
                result = self.process_settings(update, context)
            elif command == "remove":
                result = self.process_remove(update)
            elif context.args[0] == "reload":
                # TODO: add superuser check
                result = self.reload()
            else:
                result = self.info()
            self.updater.bot.send_message(chat_id=update.message.chat_id, text=result, parse_mode=parse_mode)
        self.commands.clear()

    def process_settings(self, update, context):
        if len(context.args) == 0:
            return self.info()

        result = self.info()
        parse_mode = None

        args = context.args
        option_name = args[0]

        if option_name == "id":
            steam_id = args[1]
            player = steam_api.get_players([steam_id])[steam_id]
            if player:
                uid = update.message.from_user.id
                chat_id = update.message.chat_id
                language_code = update.message.from_user.language_code
                self.storage.insert(uid, steam_id, chat_id, language_code)

                nick = player.personaname
                name = player.realname
                show_name = "%s %s %s." % (name, "aka" if name and nick else "", nick)
                result = "%s\n[%s](%s)" % ("Steam started successfully.", show_name, player.profileurl)
                parse_mode = "markdown"
            else:
                result = "Sorry, cant find user by id %s" % steam_id
        elif option_name == "remove":
            result = self.process_remove(update)

        return result, parse_mode

    def process_start(self, update, context):
        parse_mode = None
        uid = update.message.from_user.id
        stored_info = self.storage.get(uid)
        if stored_info:
            self.storage.update_enabled(uid, True)
            result = "Service enabled"
        else:
            result = self.info()

        return result, parse_mode

    def setup_steam_id(self, steam_id):

        pass

    @staticmethod
    def reload():
        SteamMessages.MESSAGES = SteamMessages.reload()
        return "[Sys] Reload done"

    @staticmethod
    def info():
        return """To use steam advice bot provide your steam ID with /settings command.
To find ID open your page in browser and get last digits from address.
ID for https://steamcommunity.com/profiles/100500 is 100500.
Commands:
/settings id <your steam id>  # setup your steam id
/settings remove  # remove your steam id
/start  # start steam advice bot
/stop  # stop steam advice bot
/help  # to show this message"""

    def process_stop(self, update: Update):
        uid = update.message.from_user.id
        self.storage.update_enabled(uid, False)
        return "steam stopped"

    def process_remove(self, update: Update):
        uid = update.message.from_user.id
        self.storage.delete(uid)
        return "Oh! Hello friend. Sorry I can't remember your name..."

    def send_note(self, player, chat_id, language_code):
        if player and player.gameid:
            message = SteamMessages.get_note(player.gameid, language_code)
            self.updater.bot.send_message(chat_id=chat_id, text=message)


def init(env: BotEnv):
    steam_api.set_steam_api_key(env.config.steam_api)
    service = SteamService(env)

    # start service
    threading.Thread(target=service.run, name="steam_service").start()

import logging
import sqlite3
import threading
from time import sleep

from telegram import Update
from telegram.ext import CommandHandler, CallbackContext

from env import Env
from handlers.steam import SteamMessages, steam_api


class SteamStorage:
    def __init__(self, path: str):
        self.path = path
        # noinspection PyTypeChecker
        self.conn = None
        # noinspection PyTypeChecker
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
    def __init__(self, env: Env):
        self.updater = env.updater
        self.storage = SteamStorage("mydatabase.db")
        self.commands = []
        self.delay = env.config.steam_request_delay
        env.dispatcher.add_handler(CommandHandler('steam', self.handle))

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

    def handle(self, update: Update, context: CallbackContext):
        logging.log(logging.INFO, "/steam called. args: %s", context.args)
        self.commands.append((update, context))

    def process_commands(self):
        for update, context in self.commands:

            # to avoid "edit message" cases
            if not update.message:
                # print("something wrong with message", update)
                continue

            parse_mode = None
            if len(context.args) == 0:
                result = self.info()
            elif context.args[0] == "start":
                result, parse_mode = self.process_start(update, context)
            elif context.args[0] == "stop":
                result = self.process_stop(update)
            elif context.args[0] == "remove":
                result = self.process_remove(update)
            elif context.args[0] == "reload":
                result = self.reload()
            else:
                result = self.info()
            self.updater.bot.send_message(chat_id=update.message.chat_id, text=result, parse_mode=parse_mode)
        self.commands.clear()

    def process_start(self, update, context):
        parse_mode = None
        uid = update.message.from_user.id
        stored_info = self.storage.get(uid)
        if stored_info:
            self.storage.update_enabled(uid, True)
            result = "I remember you. Service enabled"
        elif len(context.args) < 2:
            result = "Were is your steam id?"
        else:
            chat_id = update.message.chat_id
            steam_id = context.args[1]
            player = steam_api.get_players([steam_id])[steam_id]
            if player:
                language_code = update.message.from_user.language_code
                self.storage.insert(uid, steam_id, chat_id, language_code)

                nick = player.personaname
                name = player.realname
                show_name = "%s %s %s." % (name, "aka" if name and nick else "", nick)
                result = "%s\n[%s](%s)" % ("Steam started successfully.", show_name, player.profileurl)
                parse_mode = "markdown"

            else:
                result = "Sorry, cant find user by id %s" % steam_id
        return result, parse_mode

    @staticmethod
    def reload():
        SteamMessages.MESSAGES = SteamMessages.reload()
        return "[Sys] Reload done"

    @staticmethod
    def info():
        info_message = "usage:\n /steam start <your steam id>\n"
        info_message += "/steam stop\n"
        info_message += "/steam reload"
        return info_message

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


def init(env: Env):
    steam_api.set_steam_api_key(env.config.steam_api)
    service = SteamService(env)

    # start service
    threading.Thread(target=service.run, name="steam_service").start()

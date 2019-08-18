import json
import os
import random

EN = "en"
RU = "ru"

DEFAULT_LOCALE = EN
DEFAULT_GAME = "default"


def reload():
    result = {}
    lookup_dir = os.path.join(os.path.dirname(__file__), "notes")

    for dirname, dirnames, filenames in os.walk(lookup_dir):
        for file in filenames:
            path = os.path.join(dirname, file)
            with open(path, encoding='utf-8') as json_file:
                data = json.load(json_file)
                game_id = data.get("game_id")
                messages = data.get("messages")
                for loc, notes in messages.items():
                    all_games = result.setdefault(loc, {})
                    all_games.update({game_id: notes})
    return result


MESSAGES = reload()


def get_note(game_id, locale=""):
    locale = locale if locale in MESSAGES.keys() else DEFAULT_LOCALE
    games = MESSAGES.get(locale)
    game_id = game_id if str(game_id) in games.keys() else DEFAULT_GAME
    notes = games.get(game_id)
    return random.choice(notes)

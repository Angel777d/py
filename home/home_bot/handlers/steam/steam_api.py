import json
import urllib.request
from enum import Enum

import home_bot.config
from home_bot.config import STEAM_API

# "http://api.steampowered.com/IPlayerService/IsPlayingSharedGame/v0001/?key=%s&steamid=%s&appid_playing=%s"
GET_PLAYER_SUMMARIES = "http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key=%s&steamids=%s"


def set_steam_api_key(steam_api_key):
    home_bot.config.STEAM_API = steam_api_key


class PersonaState(Enum):
    OFFLINE = 0
    ONLINE = 1
    BUSY = 2
    AWAY = 3
    SNOOZE = 4
    LOOKING_TO_TRADE = 5
    LOOKING_TO_PLAY = 6


class SteamPlayer:
    def __init__(self, src):
        # Public data
        self.steamid: str = src.get("steamid")
        self.personaname: str = src.get("personaname")
        self.profileurl: str = src.get("profileurl")
        self.avatar: str = src.get("avatar")
        self.avatarmedium: str = src.get("avatarmedium")
        self.avatarfull: str = src.get("avatarfull")
        self.personastate: PersonaState = PersonaState(src.get("personastate", 0))
        self.communityvisibilitystate: int = src.get("communityvisibilitystate")
        self.profilestate: int = src.get("profilestate")
        self.lastlogoff: int = src.get("lastlogoff")
        self.commentpermission: int = src.get("commentpermission")

        # Private data
        self.realname: str = src.get("realname")
        self.primaryclanid: str = src.get("primaryclanid")
        self.timecreated: int = src.get("timecreated")
        self.gameid: int = src.get("gameid")
        self.gameserverip: int = src.get("gameserverip")
        self.gameextrainfo: int = src.get("gameextrainfo")
        self.cityid: int = src.get("cityid")
        self.loccountrycode: str = src.get("loccountrycode")
        self.locstatecode: str = src.get("locstatecode")
        self.loccityid: int = src.get("loccityid")

        # some event data?
        self.personastateflags: int = src.get("personastateflags")


def get_player(steam_id):
    url = GET_PLAYER_SUMMARIES % (STEAM_API, steam_id)
    with urllib.request.urlopen(url) as response:
        result = json.loads(response.read())

        players = result.get("response").get("players")
        player = next((player for player in players if player.get("steamid") == steam_id), None)
        return SteamPlayer(player) if player else None

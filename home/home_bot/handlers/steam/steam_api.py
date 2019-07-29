import json
import urllib.request
from encodings import utf_8
from enum import Enum

__STEAM_API = ""

# "http://api.steampowered.com/IPlayerService/IsPlayingSharedGame/v0001/?key=%s&steamid=%s&appid_playing=%s"
GET_PLAYER_SUMMARIES = "http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key=%s&steamids=%s"


def set_steam_api_key(steam_api_key):
    global __STEAM_API
    __STEAM_API = steam_api_key


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
        self.steamid = src.get("steamid")
        self.personaname = src.get("personaname")
        self.profileurl = src.get("profileurl")
        self.avatar = src.get("avatar")
        self.avatarmedium = src.get("avatarmedium")
        self.avatarfull = src.get("avatarfull")
        self.personastate = PersonaState(src.get("personastate", 0))
        self.communityvisibilitystate = src.get("communityvisibilitystate")
        self.profilestate = src.get("profilestate")
        self.lastlogoff = src.get("lastlogoff")
        self.commentpermission = src.get("commentpermission")

        # Private data
        self.realname = src.get("realname")
        self.primaryclanid = src.get("primaryclanid")
        self.timecreated = src.get("timecreated")
        self.gameid = src.get("gameid")
        self.gameserverip = src.get("gameserverip")
        self.gameextrainfo = src.get("gameextrainfo")
        self.cityid = src.get("cityid")
        self.loccountrycode = src.get("loccountrycode")
        self.locstatecode = src.get("locstatecode")
        self.loccityid = src.get("loccityid")

        # some event data?
        self.personastateflags = src.get("personastateflags")


def get_players(steam_ids):
    steam_ids = ",".join(steam_ids)
    url = GET_PLAYER_SUMMARIES % (__STEAM_API, steam_ids)
    with urllib.request.urlopen(url) as response:
        result = utf_8.decode(response.read())[0]
        result = json.loads(result)
        players = result.get("response").get("players")
        return {player.get("steamid"): SteamPlayer(player) for player in players}

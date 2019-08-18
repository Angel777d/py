from BotConfig import BotConfig


class SteamBotConfig(BotConfig):
    def __init__(self, path):
        BotConfig.__init__(self, path)

    @property
    def steam_request_delay(self):
        return self.get("steam_request_delay")

    @property
    def steam_api(self):
        return self.get("steam_api")

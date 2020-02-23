from yandex_music import Client
from yandex_music.exceptions import Unauthorized

from contexts.IContext import IContext
from model import Events
from utils import Defaults
from utils.Utils import readFile, writeFile


def tryLoginWithToken():
    token = readFile(Defaults.YANDEX_TOKEN_PATH)
    if not token:
        return None
    try:
        client = Client.from_token(token)
    except Unauthorized as ex:
        return None
    return client


class YandexLoginContext(IContext):
    def __init__(self, env, data=None):
        self.yandexData = env.data.setdefault("yandex", {})
        IContext.__init__(self, env, data)
        client = tryLoginWithToken()
        if client:
            self.onClientReady(client)
        else:
            self.addEventListener("yandex.login", self.starLogin)
            self.addEventListener("yandex.login.apply", self.onLoginApply)

    def starLogin(self, ev):
        self.sendEvent(Events.WINDOW_OPEN, name="window.yandex.login")

    def onLoginApply(self, ev):
        login, password = ev.get("login"), ev.get("password")
        try:
            token = Client().generate_token_by_username_and_password(login, password)
        except Unauthorized:
            # TODO: send status to window
            # self.window.showError("Wrong login or password")
            return

        writeFile(Defaults.YANDEX_TOKEN_PATH, token)
        self.removeEventListener("yandex.login", self.starLogin)
        self.removeEventListener("yandex.login.apply", self.onLoginApply)
        self.onClientReady(Client.from_token(token))

    def onClientReady(self, client):
        self.yandexData["client"] = client
        self.openContext("yandex.client.dataChanged")
        self.openContext("context.yandex.start")

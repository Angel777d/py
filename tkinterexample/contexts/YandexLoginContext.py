from yandex_music import Client
from yandex_music.exceptions import Unauthorized

from contexts.IContext import IContext
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

    def getListenersConfig(self):
        return {
            "yandex.login": self.starLogin,
            "yandex.login.apply": self.onLoginApply
        }

    def starLogin(self, eventName, eventData):
        client = tryLoginWithToken()
        if client:
            self.onClientReady(client)
        else:
            self.openWindow("window.yandex.login")

    def onLoginApply(self, eventName, eventData):
        login, password = eventData.get("login"), eventData.get("password")
        try:
            token = Client().generate_token_by_username_and_password(login, password)
        except Unauthorized:
            # TODO: send status to window
            # self.window.showError("Wrong login or password")
            return

        writeFile(Defaults.YANDEX_TOKEN_PATH, token)
        self.closeWindow()

        self.onClientReady(Client.from_token(token))

    def onClientReady(self, client):
        self.yandexData["client"] = client
        self.openContext("context.yandex.start")
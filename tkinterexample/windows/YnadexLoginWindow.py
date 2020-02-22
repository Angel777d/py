from windows.widgets.SimpleLoginWidget import SimpleLogin
from windows.IWindow import IWindow


class YandexLoginWindow(IWindow):
    def initUI(self):
        SimpleLogin(self, self.onLoginApply, self.goBack)

    def onLoginApply(self, login, password):
        self.sendEvent("yandex.login.apply", {"login": login, "password": password})

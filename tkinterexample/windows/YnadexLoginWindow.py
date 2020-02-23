from windows.IWindow import IWindow
from windows.SimpleLoginWidget import SimpleLogin


class YandexLoginWindow(IWindow):
    def initUI(self):
        SimpleLogin(self, self.onLoginApply, self.goBack)

    def onLoginApply(self, login, password):
        self.sendEvent2("yandex.login.apply", login=login, password=password)

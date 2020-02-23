from tkinter import TOP
from tkinter.ttk import Button

from windows.IWindow import IWidget


class MenuWidget(IWidget):

    def initUI(self):
        home = Button(self, text="Home", command=lambda: self.sendEvent2("win.open", name="window.localTracks"))
        home.pack(side=TOP)

        yandexLogin = Button(self, text="Yandex Login", command=lambda: self.sendEvent2("yandex.login"))
        yandexLogin.pack(side=TOP)

        yandexShow = Button(self, text="Yandex", command=lambda: self.sendEvent2("yandex.start"))
        yandexShow.pack(side=TOP)

        config = Button(self, text="Config", command=lambda: self.sendEvent2("app.showConfig"))
        config.pack(side=TOP)

        return {}

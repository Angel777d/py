from tkinter import TOP
from tkinter.ttk import Button

from model import Events
from windows.widgets.CaptionEntryWidget import CaptionEntry
from windows.IWindow import IWidget


class MenuWidget(IWidget):

    def initUI(self):
        home = Button(self, text="Home", command=lambda: self.sendEvent(Events.WINDOW_OPEN, name="window.localTracks"))
        home.pack(side=TOP)

        yandexLogin = Button(self, text="Yandex Login", command=lambda: self.sendEvent("yandex.login"))
        yandexLogin.pack(side=TOP)

        yandexShow = Button(self, text="Yandex", command=lambda: self.sendEvent("yandex.start"))
        yandexShow.pack(side=TOP)

        config = Button(self, text="Config", command=lambda: self.sendEvent("app.showConfig"))
        config.pack(side=TOP)

        search = CaptionEntry(self, "Yandex Search")
        search.bind('<Return>', self.onSearch)
        search.pack()

        return {"search": search}

    def onSearch(self, ev):
        search: CaptionEntry = self.getElement("search")
        searchStr = search.get()
        print("got search string:", searchStr)
        self.sendEvent("yandex.request.search", entry=searchStr)
        self.sendEvent("yandex.request.search", entry=searchStr)

        return {}

from tkinter import BOTTOM, Listbox, BOTH, TOP, END
from tkinter.ttk import Button
from typing import List

from yandex_music import Track

from windows.IWindow import IWindow


class WindowYandexPlaylist(IWindow):
    def initUI(self):
        button = Button(self, text="Download", command=self.download)
        button.pack(side=BOTTOM)

        listbox = Listbox(self)
        listbox.pack(side=TOP, fill=BOTH, pady=5, expand=True)

        # self.pack(fill=BOTH, expand=True)

        # button = Button(self, text="GoBack", command=self.close)
        # button.pack(side=BOTTOM)

        # playlistWidget.doUpdate(resultList)
        return {"listbox": listbox}

    def getListenersConfig(self):
        return {"yandex.tracks.dataChanged": self.onTracksLoaded}

    def onInitialized(self):
        self.onTracksLoaded()

    def onTracksLoaded(self, *args):
        self.doUpdate(self.trackList)

    def doUpdate(self, trackList):
        listbox = self.getElement("listbox")
        listbox.delete(0, END)

        if not trackList:
            return

        for info in trackList:
            listbox.insert(END, info.title)

    def download(self):
        listbox = self.getElement("listbox")
        trackList = self.trackList
        items = [trackList[index] for index in listbox.curselection()]
        self.sendEvent("yandex.download", items=items)

    @property
    def trackList(self):
        trackList: List[Track] = self.env.data.get("yandex").get("tracks")
        return trackList

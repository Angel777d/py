from tkinter import Listbox, TOP, BOTH, END

from model import Events
from model.MediaLibEntry import MediaLibEntry
from windows.IWindow import IWindow


class WindowTracksAll(IWindow):

    def getListenersConfig(self):
        return {
            "mediaLib.allTracksLoaded": self.onAllTracksLoaded,
        }

    def initUI(self):
        listbox = Listbox(self)
        listbox.bind('<Double-Button-1>', self.onPlay)
        listbox.pack(side=TOP, fill=BOTH, pady=5, expand=True)

        return {"listbox": listbox}

    def onInitialized(self):
        self.showTracks()

    def onAllTracksLoaded(self, *args):
        self.showTracks()

    def getTracks(self):
        return self.env.data.get("mediaLib").get("allTracks", [])

    def showTracks(self):
        listbox = self.getElement("listbox")
        listbox.delete(0, END)
        trackList = self.getTracks()
        for info in trackList:
            listbox.insert(END, info.title)

    def onPlay(self, ev):
        listbox: Listbox = self.getElement("listbox")
        selection = listbox.curselection()
        if not selection:
            return

        trackList = self.getTracks()
        track: [MediaLibEntry, None] = trackList[selection[0]]
        self.sendEvent(Events.PLAYER_PLAY, entry=track)

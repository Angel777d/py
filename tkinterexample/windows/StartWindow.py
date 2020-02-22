from tkinter import Listbox, TOP, BOTH, END
from tkinter.ttk import Button

from windows.IWindow import IWindow


class StartWindow(IWindow):
    def addListeners(self, config):
        self.addEventListener("mediaLib.allTracksLoaded", self.onAllTracksLoaded)

    def removeListeners(self):
        self.removeEventListener("mediaLib.allTracksLoaded", self.onAllTracksLoaded)

    def initUI(self):
        button = Button(self, text="Show Yandex", command=self.onStartClick)
        button.pack()

        config = Button(self, text="Config", command=lambda: self.sendEvent2("app.showConfig"))
        config.pack()

        listbox = Listbox(self)
        listbox.pack(side=TOP, fill=BOTH, pady=5, expand=True)

        play = Button(self, text="Play", command=self.onPlay)
        play.pack()

        stop = Button(self, text="Stop", command=self.onStop)
        stop.pack()

        return {"listbox": listbox}

    def onStartClick(self):
        self.env.eventBus.dispatch("yandex.login")

    def onInitialized(self, data):
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

    def onPlay(self):
        listbox: Listbox = self.getElement("listbox")
        selection = listbox.curselection()
        trackList = self.getTracks()
        if selection:
            self.sendEvent2("audioPlayer.play", entry=trackList[selection[0]])

    def onStop(self):
        self.sendEvent("audioPlayer.stop")

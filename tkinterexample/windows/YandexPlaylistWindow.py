from tkinter import BOTTOM
from tkinter.ttk import Button

from windows.IWindow import IWindow
from windows.widgets.PlaylistWidget import PlaylistWidget


class YandexPlaylistWindow(IWindow):

    def addListeners(self, config):
        self.addEventListener("yandex.tracksLoaded", self.onTracksLoaded)

    def removeListeners(self):
        self.removeEventListener("yandex.tracksLoaded", self.onTracksLoaded)

    def onInitialized(self, data):
        self.onTracksLoaded()

    def initUI(self):
        playlistWidget = PlaylistWidget(self, lambda: self.download(playlistWidget))
        button = Button(self, text="GoBack", command=self.goBack)
        button.pack(side=BOTTOM)

        # playlistWidget.setData(resultList)
        return {"playlist": playlistWidget}

    def onTracksLoaded(self, *args):
        tracks = self.env.data.get("yandex").get("tracks")
        self.getElement("playlist").setData(tracks)

    def download(self, playlistWidget):
        self.sendEvent("yandex.download", {"items": [info for info in playlistWidget.getSelectedItems()]})

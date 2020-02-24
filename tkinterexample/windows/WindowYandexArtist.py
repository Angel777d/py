from tkinter import TOP
from tkinter.ttk import Label

from windows.IWindow import IWindow
from windows.widgets.YandexTilesWidgets import ArtistWidget


class WindowYandexArtist(IWindow):
	def initUI(self):
		label = Label(self, text="Artist Window")
		label.pack(side=TOP)
		return {"label": label}

	def getListenersConfig(self):
		return {"yandex.artist.dataChanged": self.onArtistChanged}

	def onInitialized(self):
		self.onArtistChanged()

	def onArtistChanged(self, *args):
		artist = self.env.data.get("yandex").get("artist")
		artist_brief = self.env.data.get("yandex").get("artist_brief")
		artist_albums = self.env.data.get("yandex").get("artist_albums")
		artist_tracks = self.env.data.get("yandex").get("artist_tracks")

		ArtistWidget(self).show(artist)

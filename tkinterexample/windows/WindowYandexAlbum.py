from tkinter import TOP
from tkinter.ttk import Label

from windows.IWindow import IWindow
from windows.widgets.YandexTilesWidgets import AlbumWidget


class WindowYandexAlbum(IWindow):
	def initUI(self):
		label = Label(self, text="Album Window")
		label.pack(side=TOP)
		return {"label": label}

	def getListenersConfig(self):
		return {"yandex.album.dataChanged": self.onAlbumChanged}

	def onInitialized(self):
		self.onAlbumChanged()

	def onAlbumChanged(self, *args):
		album = self.env.data.get("yandex").get("album")
		# artist_brief = self.env.data.get("yandex").get("artist_brief")
		# artist_albums = self.env.data.get("yandex").get("artist_albums")
		# artist_tracks = self.env.data.get("yandex").get("artist_tracks")

		AlbumWidget(self).show(album)

from tkinter import TOP, X
from tkinter.ttk import Label, Frame

from yandex_music import Album

from utils.Utils import clearItem
from windows.IWindow import IWindow
from windows.widgets.TrackListWidget import TrackListWidget
from windows.widgets.YandexTilesWidgets import AlbumWidget


class WindowYandexAlbum(IWindow):
	def initUI(self):
		label = Label(self, text="Album Window")
		label.pack(side=TOP)

		info = Frame(self)
		info.pack(side=TOP, fill=X)

		tracks = TrackListWidget(self.env, self)
		tracks.pack(side=TOP, fill=X)

		return {"label": label, "info": info, "tracks": tracks}

	def getListenersConfig(self):
		return {"yandex.album.dataChanged": self.onAlbumChanged}

	def onInitialized(self):
		self.onAlbumChanged()

	def onAlbumChanged(self, *args):
		album:Album = self.env.data.get("yandex").get("album")
		# artist_brief = self.env.data.get("yandex").get("artist_brief")
		# artist_albums = self.env.data.get("yandex").get("artist_albums")
		# artist_tracks = self.env.data.get("yandex").get("artist_tracks")

		info = self.getElement("info")
		clearItem(info)
		AlbumWidget(info).show(album)

		if album.volumes:
			tracks = self.getElement("tracks")
			tracks.doUpdate(sum(album.volumes, []))

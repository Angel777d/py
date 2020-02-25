from tkinter import TOP, X, BOTTOM
from tkinter.ttk import Label, Frame, Button

from yandex_music import Album, Track

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

		button = Button(self, text="Download", command=self.onDownload)
		button.pack(side=BOTTOM)
		return {"label": label, "info": info, "tracks": tracks}

	def getListenersConfig(self):
		return {"yandex.album.dataChanged": self.onAlbumChanged}

	def onInitialized(self):
		self.onAlbumChanged()

	def onAlbumChanged(self, *args):
		album: Album = self.env.data.get("yandex").get("album")
		# artist_brief = self.env.data.get("yandex").get("artist_brief")
		# artist_albums = self.env.data.get("yandex").get("artist_albums")
		# artist_tracks = self.env.data.get("yandex").get("artist_tracks")

		info = self.getElement("info")
		clearItem(info)
		AlbumWidget(info).show(album)

		if album.volumes:
			tracks = self.getElement("tracks")
			tracks.doUpdate(sum(album.volumes, []))

	def onDownload(self, *args):
		album: Album = self.env.data.get("yandex").get("album")
		if album.volumes:
			items = sum(album.volumes, [])
			self.sendEvent("yandex.download", items=[item.track_id for item in items])

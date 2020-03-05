from tkinter import TOP, X, RIGHT
from tkinter.ttk import Frame, Button

from yandex_music import Album

from utils.Utils import clearItem
from windows.IWindow import IWindow
from windows.widgets.YandexTilesWidgets import AlbumWidget


class WindowYandexAlbum(IWindow):
	def initUI(self):
		frame = Frame(self)
		button = Button(frame, text="Download Album", command=self.onDownload)
		button.pack(side=RIGHT)
		frame.pack(side=TOP, fill=X)

		info = Frame(self)
		info.pack(side=TOP, fill=X)

		trackListWidget = TrackListWidget(self.env, self, 6)
		trackListWidget.pack(side=TOP, fill=X)

		return {"info": info, "trackListWidget": trackListWidget}

	def getListenersConfig(self):
		return {"yandex.album.dataChanged": self.onAlbumChanged}

	def onInitialized(self):
		self.onAlbumChanged()

	def onAlbumChanged(self, *args):
		album: Album = self.env.data.get("yandex").get("album")

		info = self.getElement("info")
		clearItem(info)
		AlbumWidget(info).show(album)

		if album.volumes:
			trackListWidget = self.getElement("trackListWidget")
			trackListWidget.doUpdate(sum(album.volumes, []))

	def onDownload(self, *args):
		album: Album = self.env.data.get("yandex").get("album")
		if album.volumes:
			items = sum(album.volumes, [])
			self.sendEvent("yandex.download", items=[item.track_id for item in items])

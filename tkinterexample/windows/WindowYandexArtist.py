from tkinter import TOP, X
from tkinter.ttk import Label, Frame

from yandex_music import BriefInfo

from model import Events
from windows.IWindow import IWindow
from windows.widgets.TrackListWidget import TrackListWidget
from windows.widgets.YandexTilesWidgets import ArtistWidget, AlbumWidget


class WindowYandexArtist(IWindow):
	def initUI(self):
		label = Label(self, text="Artist Window")
		label.pack(side=TOP)

		info = Frame(self)
		info.pack(side=TOP, fill=X)

		tracks = TrackListWidget(self.env, self)
		tracks.pack(side=TOP, fill=X)

		albums = Frame(self)
		albums.pack(side=TOP, fill=X)

		return {"label": label, "tracks": tracks, "info": info, "albums": albums}

	def getListenersConfig(self):
		return {"yandex.artist.dataChanged": self.onArtistChanged}

	def onInitialized(self):
		self.onArtistChanged()

	@staticmethod
	def clearItem(item):
		children = [c for c in item.children.values()]
		for child in children:
			child.destroy()

	def onArtistChanged(self, *args):

		artist = self.env.data.get("yandex").get("artist")
		artist_brief: BriefInfo = self.env.data.get("yandex").get("artist_brief")
		artist_albums = self.env.data.get("yandex").get("artist_albums")
		artist_tracks = self.env.data.get("yandex").get("artist_tracks")

		self.clearItem(self.getElement("info"))
		self.clearItem(self.getElement("albums"))

		# image
		frame = self.getElement("info")
		ArtistWidget(frame).show(artist)
		frame.pack(side=TOP, fill=X)

		if artist_brief:
			tracks = self.getElement("tracks")
			tracks.doUpdate(artist_brief.popular_tracks)

			frame = self.getElement("albums")
			for index in range(min(len(artist_brief.albums), 4)):
				item = artist_brief.albums[index]
				AlbumWidget(frame, self.showAlbum).show(item)

	def showAlbum(self, album):
		self.sendEvent("yandex.request.album", album=album)
		self.sendEvent(Events.WINDOW_OPEN, name="window.yandex.album")

from tkinter import TOP, X, BOTH
from tkinter.ttk import Label, Frame

from yandex_music import BriefInfo

from model import Events
from utils.Utils import clearItem
from windows.IWindow import IWindow
from windows.widgets.TrackListWidget import TrackListWidget
from windows.widgets.VerticalScrollFrame import VerticalScrolledFrame
from windows.widgets.YandexTilesWidgets import ArtistWidget, AlbumWidget


class WindowYandexArtist(IWindow):
	def initUI(self):
		scroll = VerticalScrolledFrame(self)
		scroll.pack(fill=BOTH, expand=True)

		label = Label(scroll, text="Artist Window")
		label.pack(side=TOP)

		info = Frame(scroll)
		info.pack(side=TOP, fill=X)

		trackListWidget = TrackListWidget(self.env, scroll)
		trackListWidget.pack(side=TOP, fill=X)

		albums = Frame(scroll)
		albums.pack(side=TOP, fill=X)

		return {"label": label, "trackListWidget": trackListWidget, "info": info, "albums": albums}

	def getListenersConfig(self):
		return {"yandex.artist.dataChanged": self.onArtistChanged}

	def onInitialized(self):
		self.onArtistChanged()

	def onArtistChanged(self, *args):

		artist = self.env.data.get("yandex").get("artist")
		artist_brief: BriefInfo = self.env.data.get("yandex").get("artist_brief")
		artist_albums = self.env.data.get("yandex").get("artist_albums")
		artist_tracks = self.env.data.get("yandex").get("artist_tracks")

		clearItem(self.getElement("info"))
		clearItem(self.getElement("albums"))

		# image
		frame = self.getElement("info")
		ArtistWidget(frame).show(artist)
		frame.pack(side=TOP, fill=X)

		if artist_brief:
			trackListWidget = self.getElement("trackListWidget")
			trackListWidget.doUpdate(artist_brief.popular_tracks)

			frame = self.getElement("albums")
			for index in range(min(len(artist_brief.albums), 4)):
				item = artist_brief.albums[index]
				AlbumWidget(frame, self.showAlbum).show(item)

	def showAlbum(self, album):
		self.sendEvent("yandex.request.album", album=album)
		self.sendEvent(Events.WINDOW_OPEN, name="window.yandex.album")

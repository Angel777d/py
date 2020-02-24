from tkinter import LEFT, TOP, X, BOTH, TRUE
from tkinter.tix import Label, Frame
from typing import ClassVar

from yandex_music import Search, SearchResult

from model import Events
from windows.IWindow import IWindow
from windows.widgets.VerticalScrollFrame import VerticalScrolledFrame
from windows.widgets.YandexTilesWidgets import ArtistWidget, AlbumWidget, TrackWidget, PlaylistWidget


class SearchResultFrame(Frame):
	def initUI(self, widgetClass: ClassVar, search: SearchResult, title: str, callback):
		label = Label(self, text=title)
		label.pack(side=TOP)
		for index in range(min(search.total, search.per_page, 4)):
			item = search.results[index]
			widgetClass(self, callback).show(item)

		self.pack(side=TOP, pady=5, fill=X)


class WindowYandexSearch(IWindow):
	def getListenersConfig(self):
		return {"yandex.search.dataChanged": self.onSearchComplete}

	def initUI(self):
		label = Label(self, text="Yandex search")
		label.pack()

		label = Label(self, text="Result:")
		label.pack()
		label.configure()
		return {}

	def onInitialized(self):
		self.onSearchComplete()

	def onSearchComplete(self, ev=None):
		search: Search = self.searchResult

		if not search:
			return

		children = [c for c in self.children.values()]
		for child in children:
			child.destroy()

		scrollFrame = VerticalScrolledFrame(self)
		scrollFrame.pack(side=LEFT, fill=BOTH, expand=TRUE)

		best = search.best.type
		order = ["artist", "track", "album", "playlist"]
		data = {
			"artist": (ArtistWidget, search.artists, "Artist", self.showArtist),
			"track": (TrackWidget, search.tracks, "Tracks", self.showTrack),
			"album": (AlbumWidget, search.albums, "Albums", self.showAlbum),
			"playlist": (PlaylistWidget, search.playlists, "Playlists", self.showPlaylist),
		}

		SearchResultFrame(scrollFrame).initUI(*data[best])
		for resultType in [t for t in order if t != best]:
			SearchResultFrame(scrollFrame).initUI(*data[resultType])

	def showPlaylist(self, playlist):
		self.sendEvent("yandex.request.playlist", playlist=playlist)
		self.sendEvent(Events.WINDOW_OPEN, name="window.yandex.playlist")

	def showArtist(self, artist):
		self.sendEvent("yandex.request.artist", artist=artist)
		self.sendEvent(Events.WINDOW_OPEN, name="window.yandex.artist")

	def showAlbum(self, album):
		self.sendEvent("yandex.request.album", album=album)
		self.sendEvent(Events.WINDOW_OPEN, name="window.yandex.album")

	def showTrack(self, track):
		self.sendEvent("yandex.download", items=[track])

	@property
	def searchResult(self):
		return self.env.data.get("yandex").get("search")

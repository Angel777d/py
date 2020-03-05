from tkinter import TOP, X, RIGHT, LEFT
from tkinter.ttk import Button, Frame
from typing import List

from yandex_music import Track

from windows.IWindowTk import IWindowTk
from windows.widgets.TrackListWidget import TrackListWidget
from windows.widgets.YandexTilesWidgets import EntityCover
from yandex.Extentions import getPlaylistCover


class WindowYandexPlaylist(IWindowTk):
	def initUI(self):
		frame = Frame(self)
		button = Button(frame, text="Download All", command=self.download)
		button.pack(side=RIGHT)
		frame.pack(side=TOP, fill=X)

		frame = Frame(self)
		cover = EntityCover(frame, width=200, height=200)
		cover.pack(side=LEFT)
		frame.pack(side=TOP, fill=X)

		trackListWidget = TrackListWidget(self.env, self, 7)
		trackListWidget.pack(side=TOP, fill=X)

		return {"trackListWidget": trackListWidget, "cover": cover}

	def getListenersConfig(self):
		return {"yandex.tracks.dataChanged": self.onTracksLoaded}

	def onInitialized(self):
		self.onTracksLoaded()

	def onTracksLoaded(self, *args):
		self.getElement("cover").loadCover(getPlaylistCover(self.playlist))
		self.getElement("trackListWidget").doUpdate(self.trackList)

	def download(self):
		self.sendEvent("yandex.download", items=[i.trackId for i in self.trackList])

	@property
	def trackList(self):
		trackList: List[Track] = self.env.data.get("yandex").get("tracks")
		return trackList

	@property
	def playlist(self):
		return self.env.data.get("yandex").get("playlist")

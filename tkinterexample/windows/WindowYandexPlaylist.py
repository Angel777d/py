from tkinter import TOP, X, RIGHT
from tkinter.ttk import Button, Frame
from typing import List

from yandex_music import Track

from windows.IWindow import IWindow
from windows.widgets.TrackListWidget import TrackListWidget


class WindowYandexPlaylist(IWindow):
	def initUI(self):
		frame = Frame(self)
		button = Button(frame, text="Download All", command=self.download)
		button.pack(side=RIGHT)
		frame.pack(side=TOP, fill=X)

		trackListWidget = TrackListWidget(self.env, self, 12)
		trackListWidget.pack(side=TOP, fill=X)

		return {"trackListWidget": trackListWidget}

	def getListenersConfig(self):
		return {"yandex.tracks.dataChanged": self.onTracksLoaded}

	def onInitialized(self):
		self.onTracksLoaded()

	def onTracksLoaded(self, *args):
		self.getElement("trackListWidget").doUpdate(self.trackList)

	def download(self):
		self.sendEvent("yandex.download", items=[i.trackId for i in self.trackList])

	@property
	def trackList(self):
		trackList: List[Track] = self.env.data.get("yandex").get("tracks")
		return trackList

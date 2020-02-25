from tkinter import BOTH, TOP
from tkinter.ttk import Button
from typing import List

from yandex_music import Track

from windows.IWindow import IWindow
from windows.widgets.TrackListWidget import TrackListWidget


class WindowYandexPlaylist(IWindow):
	def initUI(self):
		button = Button(self, text="Download", command=self.download)
		button.pack(side=TOP)

		trackListWidget = TrackListWidget(self.env, self)
		trackListWidget.pack(side = TOP, fill=BOTH, expand=True)
		return {"trackListWidget": trackListWidget}

	def getListenersConfig(self):
		return {"yandex.tracks.dataChanged": self.onTracksLoaded}

	def onInitialized(self):
		self.onTracksLoaded()

	def onTracksLoaded(self, *args):
		trackListWidget = self.getElement("trackListWidget")
		trackListWidget.doUpdate(self.trackList)

	def download(self):
		trackListWidget = self.getElement("trackListWidget")
		trackList = self.trackList
		items = [trackList[index] for index in trackListWidget.curselection()]
		self.sendEvent("yandex.download", items=items)

	@property
	def trackList(self):
		trackList: List[Track] = self.env.data.get("yandex").get("tracks")
		return trackList

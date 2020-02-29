import math
from itertools import count
from tkinter import TOP, X
from tkinter.ttk import Frame, Label

from yandex_music import Landing, Playlist

from model import Events
from utils.Env import Env
from utils.Utils import clearItem
from windows.IWindow import IWindow, IWindowContainer
from windows.widgets.YandexTilesWidgets import PlaylistWidget


class WindowYandexLanding(IWindow):

	def __init__(self, env: Env, name: str, parentWindow: IWindowContainer, **kwargs):
		self.widgetsToPack = []
		super().__init__(env, name, parentWindow, **kwargs)
		self.bind("<Configure>", self.onCFG)

	def initUI(self):
		personal = Frame(self, height=100)
		personal.pack(side=TOP, fill=X, expand=True)

		Label(self, text="Others").pack(side=TOP)

		other = Frame(self, height=100)
		other.pack(side=TOP, fill=X, expand=True)

		return {"personal": personal, "other": other}

	def onCFG(self, event):
		size = max(1, int(event.width / 220))
		oldSize = self.getData("size")
		if oldSize != size:
			self.setData(size, "size")
			self.packAll()

	def onInitialized(self):
		self.showLanding()

	def getListenersConfig(self):
		return {"yandex.landing.dataChanged": self.showLanding}

	def showLanding(self, ev=None):
		landing = self.landing

		if not landing:
			return
		self.widgetsToPack.clear()
		self.showPersonal()
		self.showOther()
		self.packAll()

	def showPersonal(self):
		block = [b for b in self.landing.blocks if b.type == "personal-playlists"][0]
		frame = self.getElement("personal")
		clearItem(frame)
		index = count()
		for entity in block.entities:
			playlist: Playlist = entity.data.data
			self.addPlaylist(playlist, frame, next(index))

	def showOther(self):
		frame = self.getElement("other")
		clearItem(frame)
		index = count()
		for playlist in self.otherPlaylists:
			self.addPlaylist(playlist, frame, next(index))

	def addPlaylist(self, playlist, frame, index):
		widget = PlaylistWidget(frame, self.showPlaylist)
		widget.show(playlist)
		self.widgetsToPack.append((widget, index))

	def packAll(self):
		for widget, index in self.widgetsToPack:
			self.packWidget(widget, index)

	def packWidget(self, widget, index):
		columns = self.getData("size", 3)
		row = int(math.floor(index / columns))
		col = int(math.fmod(index, columns))
		widget.grid(row=row, column=col)

	def showPlaylist(self, playlist):
		self.sendEvent("yandex.request.playlist", playlist=playlist)
		self.sendEvent(Events.WINDOW_OPEN, name="window.yandex.playlist")

	@property
	def otherPlaylists(self):
		landing = self.landing
		return [e.data for b in landing.blocks for e in b.entities if e.type == "playlist"]

	@property
	def landing(self):
		landing: Landing = self.env.data.get("yandex").get("landing")
		return landing

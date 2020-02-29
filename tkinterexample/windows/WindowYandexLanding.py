import math
from itertools import count
from tkinter import TOP, X
from tkinter.ttk import Frame, Label

from yandex_music import Landing, Playlist

from model import Events
from utils.Utils import clearItem
from windows.IWindow import IWindow
from windows.widgets.YandexTilesWidgets import PlaylistWidget


class WindowYandexLanding(IWindow):

	def initUI(self):
		personal = Frame(self, height=100)
		personal.pack(side=TOP, fill=X, expand=True)

		Label(self, text="Others").pack(side=TOP)

		other = Frame(self, height=100)
		other.pack(side=TOP, fill=X, expand=True)
		self.bind("<Configure>", self.onCFG)

		return {"personal": personal, "other": other}

	def onCFG(self, event):
		w = event.width
		h = event.height
		size = int(w / 220)
		oldSize = self.getData("size")
		self.setData(size, "size")
		# if oldSize != size:
		# 	self.showLanding()

	def onInitialized(self):
		self.showLanding()

	def getListenersConfig(self):
		return {"yandex.landing.dataChanged": self.showLanding}

	def showLanding(self, ev=None):
		landing = self.landing

		if not landing:
			return

		self.showPersonal()
		self.showOther()

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
		d = self.data
		columns = self.getData("size", 3)
		widget = PlaylistWidget(frame, self.showPlaylist)
		widget.show(playlist)
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

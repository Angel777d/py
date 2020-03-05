import math
from itertools import count
from tkinter import TOP, X
from tkinter.ttk import Frame, Label

from yandex_music import Landing, Playlist

import Events
from utils.Env import Env
from utils.IWindow import IWindowContainer
from utils.Utils import clearItem
from windows.IWindowTk import IWindowTk
from windows.widgets.YandexTilesWidgets import PlaylistWidget


class WindowYandexLanding(IWindowTk):

	def __init__(self, env: Env, name: str, parentWindow: IWindowContainer, **kwargs):
		self.playlistWidgets = {}
		super().__init__(env, name, parentWindow, **kwargs)

		p = parentWindow.viewContainer.winfo_parent()
		p = parentWindow.viewContainer.nametowidget(p)
		p.bind("<Configure>", self.onCFG)

	def destroy(self):
		for widget in self.playlistWidgets.values():
			widget.destroy()
		self.playlistWidgets.clear()
		IWindowTk.destroy(self)

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

		self.showPersonal()
		self.showOther()
		self.packAll()

	def showPersonal(self):
		block = [b for b in self.landing.blocks if b.type == "personal-playlists"][0]
		frame = self.getElement("personal")
		index = count()
		for entity in block.entities:
			playlist: Playlist = entity.data.data
			widget = self.getWidget(frame, next(index))
			widget.show(playlist)

	def showOther(self):
		frame = self.getElement("other")
		index = count()
		for playlist in self.otherPlaylists:
			widget = self.getWidget(frame, next(index))
			widget.show(playlist)

	def getWidget(self, frame, index):
		widget = self.playlistWidgets.get((frame, index))
		if widget:
			return widget
		widget = PlaylistWidget(frame, self.showPlaylist)
		self.playlistWidgets[(frame, index)] = widget
		return widget

	def packAll(self):
		for key in self.playlistWidgets:
			frame, index = key
			self.packWidget(self.playlistWidgets[key], index)

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

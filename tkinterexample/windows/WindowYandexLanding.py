from tkinter import Listbox, TOP, BOTH, END, X
from tkinter.ttk import Frame, Label

from yandex_music import Landing, Playlist

from model import Events
from utils.Utils import clearItem
from windows.IWindow import IWindow
from windows.widgets.YandexTilesWidgets import PlaylistWidget


class WindowYandexLanding(IWindow):

	def initUI(self):
		label = Label(self, text="Landing")
		label.pack()

		personal = Frame(self, height=100)
		personal.pack(side=TOP, fill=X, expand=True)

		listbox = Listbox(self)
		listbox.pack(side=TOP, fill=BOTH, pady=5, expand=True)
		listbox.bind("<<ListboxSelect>>", self.onSelectionChanged)
		listbox.bind('<Double-Button-1>', self.onListClick)

		return {"listbox": listbox, "personal": personal}

	def onInitialized(self):
		self.showLanding()

	def getListenersConfig(self):
		return {"yandex.landing.dataChanged": self.showLanding}

	def showLanding(self, ev=None):
		landing = self.landing
		listbox = self.getElement("listbox")
		listbox.delete(0, END)

		if not landing:
			return
		self.showPersonal()

		playlists = self.playlists
		for playlist in playlists:
			listbox.insert(END, "%s: [%s]" % (playlist.title, playlist.description))
		listbox.select_set(0)

	def showPersonal(self):
		block = [b for b in self.landing.blocks if b.type == "personal-playlists"][0]
		frame = self.getElement("personal")
		clearItem(frame)
		for entity in block.entities:
			playlist: Playlist = entity.data.data
			widget = PlaylistWidget(frame, self.showPlaylist)
			widget.show(playlist)

	def onListClick(self, ev):
		listbox = self.getElement("listbox")
		playlists = self.playlists
		playlist = [playlists[index] for index in listbox.curselection()][0]
		self.showPlaylist(playlist)

	def showPlaylist(self, playlist):
		self.sendEvent("yandex.request.playlist", playlist=playlist)
		self.sendEvent(Events.WINDOW_OPEN, name="window.yandex.playlist")

	def onSelectionChanged(self, ev):
		listbox = self.getElement("listbox")
		selection = listbox.curselection()
		print("Current selection:", selection, ev)
		pass

	@property
	def playlists(self):
		playlists = []
		landing = self.landing
		for block in landing.blocks:
			for entity in block.entities:
				if entity.type == "personal-playlist":
					# playlists.append(entity.data.data)
					pass
				elif entity.type == "playlist":
					playlists.append(entity.data)
				else:
					pass
		return playlists

	@property
	def landing(self):
		landing: Landing = self.env.data.get("yandex").get("landing")
		return landing

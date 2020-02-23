from tkinter import Listbox, TOP, BOTH, END
from tkinter.ttk import Frame, Label

from yandex_music import Landing

from model import Events
from windows.IWindow import IWindow


# class PersonalPlaylistWidget(Frame):
#     SIZE = 200
#
#     def __init__(self, parent, **kwargs):
#         Frame.__init__(self, parent)
#         self.canvas = Canvas(self, width=self.SIZE, height=self.SIZE)
#         self.pack()
#
#     def draw(self):
#         c = self.canvas
#
#         c.create_rectangle(0, 0, self.SIZE, self.SIZE, fill='gray', width=0)
#         c.create_text(self.SIZE / 2, self.SIZE / 2, text="Playlist Name", justify=CENTER)  # , font="Verdana 14")
#         c.create_text(self.SIZE, self.SIZE, text="Description", anchor=SE, fill="#FF00FF")
#         c.bind("<Button-1>", self.onClick)
#
#         c.pack()
#
#     def doUpdate(self, playlist: Playlist):
#         self.playlist = playlist
#
#     def onClick(self, ev):
#         pass


class WindowYandexLanding(IWindow):

	def initUI(self):
		label = Label(self, text="Landing")
		label.pack()

		personal = Frame(self, height=100)
		# personal.pack(side=TOP, fill=X, expand=True)

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

		playlists = self.playlists
		for playlist in playlists:
			listbox.insert(END, "%s: [%s]" % (playlist.title, playlist.description))
		listbox.select_set(0)

	# def showPersonal(self, block):
	#     frame = self.getElement("personal")
	#     for entity in block.entities:
	#         playlist: Playlist = entity.data.data
	#         widget = PersonalPlaylistWidget(frame)
	#         widget.doUpdate(playlist)

	def onListClick(self, ev):
		listbox = self.getElement("listbox")
		playlists = self.playlists
		playlist = [playlists[index] for index in listbox.curselection()][0]

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
					playlists.append(entity.data.data)
				elif entity.type == "playlist":
					playlists.append(entity.data)
				else:
					pass
		return playlists

	@property
	def landing(self):
		landing: Landing = self.env.data.get("yandex").get("landing")
		return landing

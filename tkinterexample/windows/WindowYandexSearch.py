from tkinter import LEFT, TOP
from tkinter.ttk import Label, Frame

from yandex_music import Artist, Track, Search, SearchResult

from windows.IWindow import IWindow


class ArtistWidget(Frame):
	def __init__(self, master=None, **kw):
		super().__init__(master, **kw)

	def show(self, artist: Artist):
		c = self.canvas

		c.create_rectangle(0, 0, self.SIZE, self.SIZE, fill='gray', width=0)
		c.create_text(self.SIZE / 2, self.SIZE / 2, text="Playlist Name", justify=CENTER)  # , font="Verdana 14")
		c.create_text(self.SIZE, self.SIZE, text="Description", anchor=SE, fill="#FF00FF")
		c.bind("<Button-1>", self.onClick)

		label = Label(self, text="Artist")
		label.pack(side=TOP)

		label = Label(self, text=artist.name)
		label.pack()
		self.pack(side=LEFT)

	def onClick(self, ev):
		pass


class TrackWidget(Frame):
	def __init__(self, master=None, **kw):
		super().__init__(master, **kw)

	def show(self, track: Track):
		label = Label(self, text="Track")
		label.pack(side=TOP)

		label = Label(self, text=track.title)
		label.pack(side=TOP)

		label = Label(self, text="[%s]" % track.artists[0].name)
		label.pack(side=TOP)

		label = Label(self, text="[%s]" % track.albums[0].title)
		label.pack(side=TOP)

		self.pack(side=LEFT)


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

		frame = Frame(self)
		if search.best.type == "artist":
			ArtistWidget(frame).show(search.best.result)
		elif search.best.type == "track":
			TrackWidget(frame).show(search.best.result)
		frame.pack(side=TOP, pady=5)

		artists: SearchResult = search.artists
		frame = Frame(self)
		for index in range(min(artists.total, artists.per_page, 4)):
			ArtistWidget(frame).show(artists.results[index])
		frame.pack(side=TOP, pady=5)

		tracks: SearchResult = search.tracks
		frame = Frame(self)
		for index in range(min(tracks.total, tracks.per_page, 4)):
			TrackWidget(frame).show(tracks.results[index])
		frame.pack(side=TOP, pady=5)

	@property
	def searchResult(self):
		return self.env.data.get("yandex").get("search")

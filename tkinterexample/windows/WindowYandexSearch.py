from tkinter import LEFT, TOP, Canvas, SE, CENTER, NW, X
from tkinter.tix import Label, Frame

from PIL import ImageTk, Image
from yandex_music import Artist, Track, Search, SearchResult, Album

from utils.Defaults import APP_PATH
from utils.SimpleThread import SimpleThread
from windows.IWindow import IWindow

SIZE = 200


def getArtistCover(artist: Artist):
	return artist.cover.download if artist.cover else None, "artist_%s.jpg" % artist.id


def getAlbumCover(album: Album):
	if album.cover_uri:
		return album.download_cover, "album_%s.jpg" % album.id
	return getArtistCover(album.artists[0])


def getTrackCover(track: Track):
	if track.cover_uri:
		return track.download_cover, "track_%s.jpg" % track.trackId
	return getAlbumCover(track.albums[0])


class ArtistWidget(Frame):
	def __init__(self, master=None, **kw):
		super().__init__(master, **kw)
		self.img = None
		self.pack(side=LEFT)

	def show(self, artist: Artist):
		download_cover, fileName = getArtistCover(artist)
		path = APP_PATH.joinpath("cover").joinpath(fileName)
		if download_cover and not path.exists():
			path.parent.mkdir(parents=True, exist_ok=True)
			print("download artist cover:", path)
			SimpleThread(lambda: download_cover(path), lambda _: self.show(artist)).start()
			return

		c = Canvas(self, width=SIZE, height=SIZE, bg='white')
		if download_cover:
			self.img = ImageTk.PhotoImage(Image.open(path.as_posix()))
			c.create_image((SIZE / 2, SIZE / 2), image=self.img)
		else:
			c.create_rectangle(0, 0, SIZE, SIZE, fill='gray', width=0)

		# c.create_text(SIZE / 2, SIZE / 2, text="Playlist Name", justify=CENTER)  # , font="Verdana 14")
		c.create_text(SIZE, SIZE, text=artist.name, anchor=SE, fill="#FF00FF")
		c.bind("<Button-1>", self.onClick)
		c.pack()

	def onClick(self, ev):
		print("Artist click")


class TrackWidget(Frame):
	def __init__(self, master=None, **kw):
		super().__init__(master, **kw)
		self.img = None
		self.pack(side=LEFT)

	def show(self, track: Track):
		download_cover, fileName = getTrackCover(track)
		path = APP_PATH.joinpath("cover").joinpath(fileName)
		if download_cover and not path.exists():
			path.parent.mkdir(parents=True, exist_ok=True)
			print("download track cover:", path)
			SimpleThread(lambda: download_cover(path), lambda _: self.show(track)).start()
			return

		c = Canvas(self, width=SIZE, height=SIZE, bg='white')
		if download_cover:
			self.img = ImageTk.PhotoImage(Image.open(path.as_posix()))
			c.create_image((SIZE / 2, SIZE / 2), image=self.img)
		else:
			c.create_rectangle(0, 0, SIZE, SIZE, fill='gray', width=0)

		c.create_text(0, 0, text=track.albums[0].title, anchor=NW, fill="#FF00FF")
		c.create_text(SIZE / 2, SIZE / 2, text=track.title, justify=CENTER, fill="#FF00FF")  # , font="Verdana 14")
		c.create_text(SIZE, SIZE, text=track.artists[0].name, anchor=SE, fill="#FF00FF")
		c.bind("<Button-1>", self.onClick)
		c.pack()

	def onClick(self, ev):
		print("Track click")


def onClick(self, ev):
	print("Track click")


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

		frame = Frame(self)
		if search.best.type == "artist":
			ArtistWidget(frame).show(search.best.result)
		elif search.best.type == "track":
			TrackWidget(frame).show(search.best.result)
		frame.pack(side=TOP, pady=5, fill=X)

		artists: SearchResult = search.artists
		frame = Frame(self)
		label = Label(frame, text="Artist")
		label.pack(side=TOP)
		for index in range(min(artists.total, artists.per_page, 4)):
			ArtistWidget(frame).show(artists.results[index])
		frame.pack(side=TOP, pady=5, fill=X)

		tracks: SearchResult = search.tracks
		frame = Frame(self)
		label = Label(frame, text="Tracks")
		label.pack(side=TOP)
		for index in range(min(tracks.total, tracks.per_page, 4)):
			TrackWidget(frame).show(tracks.results[index])
		frame.pack(side=TOP, pady=5, fill=X)

	@property
	def searchResult(self):
		return self.env.data.get("yandex").get("search")

from tkinter import Frame, LEFT, Canvas, SE, NW, CENTER

from PIL import ImageTk, Image

from utils.Defaults import APP_PATH
from utils.SimpleThread import SimpleThread
from utils.Utils import emptyHandler
from yandex.Extentions import getArtistCover, getAlbumCover, getTrackCover, getPlaylistCover

SIZE = 200


class IEntityWidget(Frame):
	def __init__(self, master=None, callback=None, **kw):
		Frame.__init__(self, master, **kw)
		self.entity = None
		self.img = None
		self.cover = ""
		self.callback = callback if callback else emptyHandler
		self.pack(side=LEFT)

	def loadCover(self, entity):
		cover = self.getCover(entity)
		if not cover:
			return False
		download_cover, fileName = cover
		path = APP_PATH.joinpath("cover").joinpath(fileName)
		self.cover = path.as_posix()
		if download_cover and not path.exists():
			path.parent.mkdir(parents=True, exist_ok=True)
			print("download cover:", path)
			SimpleThread(lambda: download_cover(path), lambda _: self.show(entity)).start()
			return True

	def show(self, entity):
		if self.loadCover(entity):
			return

		self.entity = entity
		self.draw(entity)

	def drawCover(self):
		c = Canvas(self, width=SIZE, height=SIZE, bg='white')
		if self.cover:
			self.img = ImageTk.PhotoImage(Image.open(self.cover))
			c.create_image((SIZE / 2, SIZE / 2), image=self.img)
		else:
			c.create_rectangle(0, 0, SIZE, SIZE, fill='gray', width=0)
		c.bind("<Button-1>", self.onClick)
		return c

	def onClick(self, tkEv):
		self.callback(self.entity)

	def getCover(self, entity):
		return None

	def draw(self, entity):
		pass


class ArtistWidget(IEntityWidget):
	def getCover(self, entity):
		return getArtistCover(entity)

	def draw(self, entity):
		artist = entity
		c = self.drawCover()

		c.create_text(SIZE, SIZE, text=artist.name, anchor=SE, fill="#FF00FF")

		c.pack()


class AlbumWidget(IEntityWidget):
	def getCover(self, entity):
		return getAlbumCover(entity)

	def draw(self, entity):
		album = entity
		c = self.drawCover()

		c.create_text(0, 0, text=album.title, anchor=NW, fill="#FF00FF")
		c.create_text(SIZE, SIZE, text=album.artists[0].name, anchor=SE, fill="#FF00FF")

		c.pack()


class TrackWidget(IEntityWidget):

	def getCover(self, entity):
		return getTrackCover(entity)

	def draw(self, entity):
		track = entity
		c = self.drawCover()

		c.create_text(0, 0, text=track.albums[0].title, anchor=NW, fill="#FF00FF")
		c.create_text(SIZE / 2, SIZE / 2, text=track.title, justify=CENTER, fill="#FF00FF", font="14")
		c.create_text(SIZE, SIZE, text=track.artists[0].name, anchor=SE, fill="#FF00FF")

		c.pack()


class PlaylistWidget(IEntityWidget):
	def getCover(self, entity):
		return getPlaylistCover(entity)

	def draw(self, entity):
		playlist = entity
		c = self.drawCover()

		tPos = SIZE / 2
		c.create_text(tPos, tPos, text=playlist.title, justify=CENTER, fill="#FF00FF", font="14")

		c.pack()

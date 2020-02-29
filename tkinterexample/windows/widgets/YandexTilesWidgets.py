from tkinter import LEFT, Canvas
from tkinter.ttk import Frame

from PIL import ImageTk, Image

from utils.Defaults import APP_PATH
from utils.SimpleThread import SimpleThread
from yandex.Extentions import getArtistCover, getAlbumCover, getPlaylistCover

SIZE = 200


class EntityCover(Canvas):
	def __init__(self, master=None, cnf={}, **kw):
		self.img = None
		self.w = kw.get("width")
		self.h = kw.get("height")
		super().__init__(master, cnf, **kw)
		self.create_rectangle(0, 0, self.w, self.h, fill='gray', width=0)

	def loadCover(self, cover):
		if not cover:
			return

		download_cover, fileName = cover
		path = APP_PATH.joinpath("cover").joinpath(fileName)

		def doLoadCover():
			path.parent.mkdir(parents=True, exist_ok=True)
			print("download cover:", path)
			download_cover(path)
			return path

		if path.exists():
			self.onCover(path)
		else:
			SimpleThread(doLoadCover, self.onCover).start()

	def onCover(self, path):
		self.img = ImageTk.PhotoImage(Image.open(path.as_posix()))
		self.create_image((self.w / 2, self.h / 2), image=self.img)


class IEntityWidget(Frame):
	def __init__(self, master=None, callback=None, **kw):
		self.entity = None
		self.callback = callback
		super().__init__(master, **kw)

	def show(self, entity):
		self.entity = entity

	def doShow(self, cover):
		c = EntityCover(self, width=SIZE, height=SIZE)
		c.loadCover(cover)
		c.pack(side=LEFT)
		c.bind("<Button-1>", self.onClick)

	def onClick(self, tkEv):
		self.callback(self.entity)


class AlbumWidget(IEntityWidget):
	def show(self, entity):
		super().show(entity)
		self.doShow(getAlbumCover(entity))


class ArtistWidget(IEntityWidget):
	def show(self, entity):
		super().show(entity)
		self.doShow(getArtistCover(entity))


class PlaylistWidget(IEntityWidget):
	def show(self, entity):
		super().show(entity)
		self.doShow(getPlaylistCover(entity))

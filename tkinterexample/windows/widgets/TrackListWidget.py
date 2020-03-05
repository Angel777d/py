from tkinter import TOP, LEFT, X, RIGHT, Canvas
from tkinter.ttk import Frame, Label, Button

from yandex_music import Track

from windows.ScrollSupport import ScrollElement
from utils.Utils import clearItem
from windows.IWindowTk import IWidgetTk

TRACK_ICON_SIZE = 30


class TrackIcon(IWidgetTk):
	def initUI(self):
		c = Canvas(self, width=TRACK_ICON_SIZE, height=TRACK_ICON_SIZE)
		c.create_rectangle(0, 0, TRACK_ICON_SIZE, TRACK_ICON_SIZE, outline="#fb0", fill="#fb0", width=1)
		c.pack()


class TrackItemWidget(IWidgetTk):
	def initUI(self):
		icon = TrackIcon(self.env, self)
		icon.pack(side=LEFT)

		frame = Frame(self)
		frame.pack(side=LEFT, fill=X)

		title = Label(frame, text="title")
		title.pack(side=TOP, fill=X)

		# album = Label(frame, text="album")
		# album.pack(side=LEFT)

		# artist = Label(frame, text="[%s]" % "artist")
		# artist.pack(side=TOP, fill=X)

		button = Button(self, text="click me", command=self.onClick)
		button.pack(side=RIGHT)

		return {
			"title": title,
			# "album": album,
			# "artist": artist
		}

	def setData(self, value, key="data"):
		super().setData(value, key)
		track: Track = value

		# self.elements.get("album").configure(text=track.albums[0].title)
		# self.elements.get("artist").configure(text="[%s]" % track.artists[0].name)
		self.elements.get("title").configure(text=track.title)

	def onClick(self, ev=None):
		self.sendEvent("yandex.request.playTrack", track=self.getData())


class TrackListWidget(IWidgetTk, ScrollElement):

	def __init__(self, env, parent, size=10, **kwargs):
		self._size = size
		self._tracks = []
		self._pos = 0
		self._items = []
		ScrollElement.__init__(self)
		IWidgetTk.__init__(self, env, parent, **kwargs)
		self.initScroll(self)

	def initUI(self):
		scroll = Frame(self)
		scroll.pack(side=TOP, fill=X)

		label = Label(self, text="No tracks")
		label.pack(side=TOP, fill=X)
		return {"scroll": scroll, "label": label}

	def doUpdate(self, trackList):
		scroll = self.getElement("scroll")
		clearItem(scroll)

		if not trackList:
			return

		self._items = []
		self._tracks = trackList
		self._pos = 0

		for i in range(min(self._size, len(trackList))):
			self._items.append(self.addTrack(scroll, i))

		self.updateLabel()

	def addTrack(self, parent, index):
		info = self._tracks[index]
		item = TrackItemWidget(self.env, parent)
		item.setData(info)
		item.pack(side=TOP, fill=X)
		return item

	def curselection(self):
		listbox = self.getElement("listbox")
		return listbox.curselection()

	def onScroll(self, event):
		print("TrackListWidget::_on_mousewheel")
		if event.num == 4 or event.delta > 0:
			self.doScroll(-1)
		elif event.num == 5 or event.delta < 0:
			self.doScroll(1)

	def updateLabel(self):
		label: Label = self.getElement("label")
		end = self._pos + min(self._size, len(self._tracks))
		label.configure(text="Tracks [%s - %s] of %s" % (self._pos + 1, end, len(self._tracks)))

	def doScroll(self, delta):
		end = self._pos + min(self._size, len(self._tracks))
		canScroll = self._pos + delta >= 0 and end + delta <= len(self._tracks)
		if canScroll:
			self._pos += delta
			end += delta
			for i in range(self._pos, end):
				item = self._items[i - self._pos]
				data = self._tracks[i]
				item.setData(data)
			self.updateLabel()

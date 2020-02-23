from yandex_music import TrackShort

_EXCLUDED = ":/?|;."


class YandexTrackInfo:
	def __init__(self, entry):
		self.entry: TrackShort = entry
		self.trackId = ""
		self.title = ""
		self.artist = ""
		self.album = ""

	def apply(self, value):
		t_id, title, artist, album = value
		self.trackId = t_id
		self.title = title
		self.artist = artist
		self.album = album

	@property
	def folder(self):
		artist = "".join([c for c in self.artist if c not in _EXCLUDED])
		album = "".join([c for c in self.album if c not in _EXCLUDED])

		if album:
			return "%s/%s" % (artist, album)
		return artist

	@property
	def filename(self):
		title = "".join([c for c in self.title if c not in _EXCLUDED])
		return "%s.mp3" % title

from yandex_music import TrackShort


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
    def filename(self):
        excluded = ":/?|;"
        result = "%s (%s) %s.mp3" % (self.artist, self.album, self.title)
        return "".join([c for c in result if c not in excluded])
        # return self.trackId

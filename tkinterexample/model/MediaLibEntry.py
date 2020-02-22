class MediaLibEntry:
    def __init__(self, path: str, title: str, artist: str = None, album: str = None, **kwargs):
        self.path = path
        self.title = title
        self.artist = artist
        self.album = album
        self._other = kwargs

    def getProps(self):
        return {"path": self.path, "title": self.title, "artist": self.artist, "album": self.album, }

    @staticmethod
    def fromTuple(item):
        path, title, artist, album = item
        return MediaLibEntry(path, title, artist, album)

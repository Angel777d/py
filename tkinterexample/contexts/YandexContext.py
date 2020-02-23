from pathlib import Path

from yandex_music import Client

from contexts.IContext import IContext
from model.MediaLibEntry import MediaLibEntry
from utils.Env import ConfigProps
from utils.SimpleThread import SimpleThread
from yandex import LocalTrackList

LANDING_PRIMARY = ["personal-playlists"]

LANDING_PLAYLISTS = [
    "new-releases",
    "new-playlists",
    "playlists",
]

LANDING_TARCKS = [
    "chart",
]

LANDING_SECONDARY = [
    "promotions",
    "mixes",
    "play-contexts"
    "albums",
    "artists",
]


class YandexContext(IContext):
    def __init__(self, env, data=None):
        self.yandexData = env.data.setdefault("yandex", {})
        self.client: Client = self.yandexData.get("client")
        IContext.__init__(self, env, data)
        # self.openMainWindow()

    def getListenersConfig(self):
        return {
            "yandex.download": self.downloadFiles,
            "yandex.start": self.onStart,
            "yandex.openPlayList": self.openPlayList,
            "yandex.search": self.onSearch,
        }

    def loadLanding(self):
        def doLoad():
            self.yandexData["landing"] = self.client.landing(LANDING_PRIMARY + LANDING_PLAYLISTS)
            self.sendEvent2("yandex.landingLoaded")

        thread = SimpleThread(doLoad, name="LoadLanding")
        thread.start()

    def loadPlaylist(self, playlist):
        client = self.client

        def doLoad():
            tracks = client.users_playlists(kind=playlist.kind, user_id=playlist.uid)[0].tracks
            self.yandexData["tracks"] = LocalTrackList.getTracks(tracks)
            self.sendEvent2("yandex.tracksLoaded")

        thread = SimpleThread(doLoad, name="LoadPlaylist")
        thread.start()

    def doSearch(self, entry):
        client = self.client
        print("start search:", entry)

        def doLoad():
            result = client.search(entry)
            self.yandexData["search"] = result
            self.sendEvent2("yandex.search.done")
            print("search done", result)

        thread = SimpleThread(doLoad, name="LoadPlaylist")
        thread.start()

    def onStart(self, evName, evData):
        self.sendEvent2("win.open", name="window.yandex.start")
        self.loadLanding()

    def onSearch(self, evName, evData):
        entry = evData.get("entry")
        self.doSearch(entry)

    def openPlayList(self, evName, evData):
        self.yandexData["tracks"] = []
        self.yandexData["playlist"] = playlist = evData.get("playlist")

        self.sendEvent2("win.open", name="window.yandex.playlist")
        self.loadPlaylist(playlist)

    def downloadFiles(self, evName, evData):
        items = evData.get("items")
        for info in items:
            path = Path(self.env.config.get(ConfigProps.LIBRARY_PATH), info.filename)
            if not path.exists():
                print("[Yandex] start download:", path)
                info.entry.track.download(path)
                print("[Yandex] downloaded:", path)

            libEntry = MediaLibEntry(path.as_posix(), info.title, info.artist, info.album)
            self.sendEvent2("mediaLib.add.track", entry=libEntry)

from pathlib import Path

from yandex_music import Client

from contexts.IContext import IContext
from model import Events
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
            "yandex.request.playlist": self.openPlayList,
            "yandex.request.search": self.onSearch,
        }

    def loadLanding(self):
        def doLoad():
            self.yandexData["landing"] = self.client.landing(LANDING_PRIMARY + LANDING_PLAYLISTS)
            self.sendEvent("yandex.landing.dataChanged")

        thread = SimpleThread(doLoad, name="LoadLanding")
        thread.start()

    def loadPlaylist(self, playlist):
        client = self.client

        def doLoad():
            tracks = client.users_playlists(kind=playlist.kind, user_id=playlist.uid)[0].tracks
            self.yandexData["tracks"] = LocalTrackList.getTracks(tracks)
            self.sendEvent("yandex.tracks.dataChanged")

        thread = SimpleThread(doLoad, name="LoadPlaylist")
        thread.start()

    def doSearch(self, entry):
        client = self.client
        print("start search:", entry)

        def doLoad():
            result = client.search(entry)
            self.yandexData["search"] = result
            self.sendEvent("yandex.search.dataChanged")
            print("search done", result)

        thread = SimpleThread(doLoad, name="LoadPlaylist")
        thread.start()

    def onStart(self, ev):
        self.loadLanding()
        self.sendEvent(Events.WINDOW_OPEN, name="window.yandex.landing")

    def onSearch(self, ev):
        entry = ev.get("entry")
        self.doSearch(entry)

    def openPlayList(self, ev):
        self.yandexData["playlist"] = playlist = ev.get("playlist")
        self.yandexData["tracks"] = []
        self.loadPlaylist(playlist)

    def downloadFiles(self, ev):
        items = ev.get("items")
        for info in items:
            path = Path(self.env.config.get(ConfigProps.LIBRARY_PATH), info.folder)
            import os
            os.makedirs(path, exist_ok=True)
            path.mkdir(parents=True, exist_ok=True)
            path = path.joinpath(info.filename)
            if not path.exists():
                print("[Yandex] start download:", path)
                info.entry.track.download(path)
                print("[Yandex] downloaded:", path)

            libEntry = MediaLibEntry(path.as_posix(), info.title, info.artist, info.album)
            self.sendEvent("mediaLib.add.track", entry=libEntry)

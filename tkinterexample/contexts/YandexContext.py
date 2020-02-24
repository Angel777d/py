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
			"yandex.request.search": self.requestSearch,
			"yandex.request.playlist": self.requestPlaylist,
			"yandex.request.album": self.requestAlbum,
			"yandex.request.artist": self.requestArtist,
		}

	def onStart(self, ev):
		self.requestLanding()
		self.sendEvent(Events.WINDOW_OPEN, name="window.yandex.landing")

	def requestLanding(self):
		client = self.client

		def doLoad():
			self.yandexData["landing"] = client.landing(LANDING_PRIMARY + LANDING_PLAYLISTS)
			self.sendEvent("yandex.landing.dataChanged")

		thread = SimpleThread(doLoad, name="RequestLanding")
		thread.start()

	def requestSearch(self, ev):
		entry = ev.get("entry")
		client = self.client
		print("start search:", entry)

		def doLoad():
			result = client.search(entry)
			self.yandexData["search"] = result
			self.sendEvent("yandex.search.dataChanged")
			print("search done", result)

		thread = SimpleThread(doLoad, name="LoadPlaylist")
		thread.start()

	def requestArtist(self, ev):
		client = self.client
		yd = self.yandexData
		artist = ev.get("artist")
		yd["artist"] = artist

		def doLoad():
			yd["artist"] = client.artists([artist.id])[0]
			yd["artist_brief"] = client.artists_brief_info(artist.id)
			yd["artist_albums"] = client.artists_direct_albums(artist.id)
			yd["artist_tracks"] = client.artists_tracks(artist.id)
			self.sendEvent("yandex.artist.dataChanged")
			print("got artist info")

		SimpleThread(doLoad, name="RequestArtist").start()

	def requestAlbum(self, ev):
		self.yandexData["album"] = album = ev.get("album")
		self.sendEvent("yandex.album.dataChanged")

	def requestPlaylist(self, ev):
		self.yandexData["playlist"] = playlist = ev.get("playlist")
		self.yandexData.setdefault("tracks", [])
		client = self.client

		def doLoad():
			tracks = client.users_playlists(kind=playlist.kind, user_id=playlist.uid)[0].tracks
			self.yandexData["tracks"] = LocalTrackList.getTracks(tracks)
			self.sendEvent("yandex.tracks.dataChanged")

		SimpleThread(doLoad, name="LoadPlaylist").start()

	def downloadFiles(self, ev):
		items = ev.get("items")
		for info in items:
			path = Path(self.env.config.get(ConfigProps.LIBRARY_PATH), info.folder)
			path.mkdir(parents=True, exist_ok=True)
			path = path.joinpath(info.filename)
			if not path.exists():
				def doDownload():
					print("[Yandex] start download:", path)
					info.entry.track.download(path)
					print("[Yandex] downloaded:", path)

				SimpleThread(doDownload).start()

			libEntry = MediaLibEntry(path.as_posix(), info.title, info.artist, info.album)
			self.sendEvent("mediaLib.add.track", entry=libEntry)

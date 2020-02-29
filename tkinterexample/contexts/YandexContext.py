import os
from pathlib import Path

from mutagen.mp3 import MP3
from yandex_music import Client

from contexts.IContext import IContext
from model import Events
from utils.Env import ConfigProps
from utils.SimpleThread import SimpleThread
from utils.Utils import writeFile
from yandex.Extentions import folder, filename

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
		print("[YandexContext] start search:", entry)

		def doLoad():
			result = client.search(entry)
			self.yandexData["search"] = result
			self.sendEvent("yandex.search.dataChanged")
			print("[YandexContext] search done", result)

		thread = SimpleThread(doLoad, name="LoadPlaylist")
		thread.start()

	def requestArtist(self, ev):
		client = self.client
		yd = self.yandexData
		yd["artist"] = artist = ev.get("artist")

		def doLoad():
			yd["artist"] = client.artists([artist.id])[0]
			yd["artist_brief"] = client.artists_brief_info(artist.id)
			yd["artist_albums"] = client.artists_direct_albums(artist.id)
			yd["artist_tracks"] = client.artists_tracks(artist.id)
			self.sendEvent("yandex.artist.dataChanged")
			print("[YandexContext] got artist info")

		SimpleThread(doLoad, name="requestArtist").start()

	def requestAlbum(self, ev):
		client = self.client
		yd = self.yandexData
		yd["album"] = album = ev.get("album")

		def doLoad():
			yd["album"] = client.albums_with_tracks(album.id)
			self.sendEvent("yandex.album.dataChanged")
			print("[YandexContext] got album info")

		SimpleThread(doLoad, name="requestAlbum").start()

	def requestPlaylist(self, ev):
		client = self.client
		yd = self.yandexData
		yd["playlist"] = playlist = ev.get("playlist")
		yd.setdefault("tracks", [])

		def doLoad():
			tracks = client.users_playlists(kind=playlist.kind, user_id=playlist.uid)[0].tracks
			yd["tracks"] = client.tracks([t.track_id for t in tracks])
			self.sendEvent("yandex.tracks.dataChanged")
			print("[YandexContext] got playlist info")

		SimpleThread(doLoad, name="requestPlaylist").start()

	def downloadFiles(self, ev):
		items = ev.get("items")
		client = self.client
		tracks = client.tracks(items)

		def doDownload():
			from mutagen.easyid3 import EasyID3
			easyID3List = EasyID3.valid_keys.keys()
			print(easyID3List)

			playlist = "#EXTM3U\n"
			libPath = self.env.config.get(ConfigProps.LIBRARY_PATH)
			for track in tracks:
				path = Path(libPath, folder(track))
				path.mkdir(parents=True, exist_ok=True)
				path = path.joinpath(filename(track))
				if not path.exists():
					print("[YandexContext] start download:", path)
					track.download(path)
					print("[YandexContext] downloaded:", path)

				# audio = mp3(path)
				audio = MP3(path, ID3=EasyID3)

				audio["title"] = track.title
				audio["album"] = track.albums[0].title
				audio["artist"] = track.artists[0].name
				audio.save()

				playlist += "#EXTINF:%s, %s - %s\n" % (int(audio.info.length), track.artists[0].name, track.title)
				playlist += "%s\n" % path.relative_to(Path(libPath)).as_posix()

			path = Path(libPath).joinpath("playlist.m3u8")
			writeFile(path, playlist)
			print("all files downloaded. playlist created. open playlist")
			os.startfile(path)

		SimpleThread(doDownload).start()

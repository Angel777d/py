from yandex_music import Artist, Album, Track, Playlist

_EXCLUDED = ':/?|;.<>*"'


def trackSimpleData(track: Track):
	artist = "".join([c for c in track.artists[0].name if track.artists and c not in _EXCLUDED])
	album = "".join([c for c in track.albums[0].title if track.albums and c not in _EXCLUDED])
	title = track.title
	return title, album, artist


def folder(track: Track):
	title, album, artist = trackSimpleData(track)

	if album:
		return "%s/%s" % (artist, album)
	return artist


def filename(track: Track):
	title = "".join(["_" if c in _EXCLUDED else c for c in track.title])
	return "%s.mp3" % title


def getArtistCover(artist: Artist):
	if artist.cover:
		return artist.cover.download, "artist_%s.jpg" % artist.id


def getAlbumCover(album: Album):
	if album.cover_uri:
		return album.download_cover, "album_%s.jpg" % album.id
	return getArtistCover(album.artists[0])


def getTrackCover(track: Track):
	if track.cover_uri:
		return track.download_cover, "track_%s.jpg" % track.trackId
	return getAlbumCover(track.albums[0])


def getPlaylistCover(playlist: Playlist):
	if playlist.cover:
		return playlist.cover.download, "playlist_%s_%s.jpg" % (playlist.playlistId, playlist.uid)
	return None

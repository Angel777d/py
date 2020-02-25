from yandex_music import Artist, Album, Track, Playlist


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

from yandex_music import TracksList

from model.Database import getConnection, saveYandexTrack, getYandexTrack
from model.YandexTrackInfo import YandexTrackInfo


def getTracks(trackList: TracksList):
    conn = getConnection()
    c = conn.cursor()

    result = [getEntryInfo(c, entry) for entry in trackList]

    conn.commit()
    conn.close()
    return result


def getEntryInfo(c, entry):
    value = YandexTrackInfo(entry)

    result = getYandexTrack(c, entry.track_id)
    if result:
        value.apply(result)
    else:
        value.apply(downloadEntryInfo(c, entry))

    return value


def downloadEntryInfo(c, entry):
    track = entry.track
    t_id = entry.track_id
    title = track.title
    artist = track.artists[0].name if track.artists else ""
    album = track.albums[0].title if track.albums else ""
    return saveYandexTrack(c, t_id, title, artist, album)



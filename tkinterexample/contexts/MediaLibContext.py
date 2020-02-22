from contexts.IContext import IContext
from model.Database import getConnection, addLibEntry, getLibAll
from model.MediaLibEntry import MediaLibEntry


class MediaLibContext(IContext):
    def __init__(self, env, data=None):
        IContext.__init__(self, env, data)
        self.mediaLibData = env.data.setdefault("mediaLib", {})
        self.loadAll()

    def getListenersConfig(self):
        return {"mediaLib.add.track": self.onAddTrack}

    def loadAll(self):
        conn = getConnection()
        c = conn.cursor()
        self.mediaLibData["allTracks"] = [MediaLibEntry.fromTuple(item) for item in getLibAll(c)]
        conn.close()
        print("[MediaLib] all tracks loaded:", len(self.mediaLibData["allTracks"]))
        self.sendEvent2("mediaLib.allTracksLoaded")

    def onAddTrack(self, eventName, eventData):
        entry: MediaLibEntry = eventData.get("entry")
        conn = getConnection()
        c = conn.cursor()
        addLibEntry(c, **entry.getProps())
        conn.commit()
        conn.close()

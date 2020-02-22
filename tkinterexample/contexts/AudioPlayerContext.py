from Mpg123Player import Mpg123Player
from contexts.IContext import IContext
from model.MediaLibEntry import MediaLibEntry


class AudioPlayerContext(IContext):
    def __init__(self, env, data=None):
        IContext.__init__(self, env, data)
        self.__player = Mpg123Player()

    def getListenersConfig(self):
        return {
            "audioPlayer.play": self.onPlay,
            "audioPlayer.stop": self.onStop,
            "audioPlayer.pause": self.onPause,
        }

    def onPlay(self, eventName, eventData):
        entry: MediaLibEntry = eventData.get("entry")
        print("[MediaLib] play track", entry.path)
        self.__player.play(entry.path)

    def onStop(self, eventName, eventData):
        self.__player.stop()

    def onPause(self, eventName, eventData):
        self.__player.stop()
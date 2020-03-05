from VLCPlayer import VLCPlayer
from contexts.IContext import IContext
from model import Events


class AudioPlayerContext(IContext):
	def __init__(self, env, data=None):
		IContext.__init__(self, env, data)
		self.__player = VLCPlayer()

	def getListenersConfig(self):
		return {
			Events.PLAYER_PLAY: self.onPlay,
			Events.PLAYER_STOP: self.onStop,
			Events.PLAYER_TOGGLE_PAUSE: self.onPause,
		}

	def onPlay(self, ev):
		path = ev.get("path")
		self.__player.play(path)

	def onStop(self, ev):
		self.__player.stop()
		pass

	def onPause(self, ev):
		self.__player.togglePause()
		pass

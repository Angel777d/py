from contexts.IContext import IContext
from model import Events


class StartContext(IContext):
	def __init__(self, env, data=None):
		IContext.__init__(self, env, data=None)
		self.init()

	def getListenersConfig(self):
		return {
			"app.showConfig": self.onShowConfig,
		}

	def init(self):

		self.openContext("context.audioPlayer")
		self.openContext("context.mediaLib")
		self.openContext("context.yandex.login")

		# init main app window
		self.sendEvent(Events.WINDOW_OPEN, name="window.start")
		self.sendEvent("app.initialized")
		# self.sendEvent(Events.WINDOW_OPEN, name="window.localTracks", parent="window.start")

	def onShowConfig(self, ev):
		self.sendEvent(Events.WINDOW_OPEN, name="window.config")

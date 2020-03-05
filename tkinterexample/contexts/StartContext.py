from contexts.IContext import IContext
import Events


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
		self.openContext("context.yandex.login")

		# init main app window
		self.sendEvent(Events.WINDOW_OPEN, name="window.start")
		self.sendEvent("app.initialized")

	def onShowConfig(self, ev):
		self.sendEvent(Events.WINDOW_OPEN, name="window.config")

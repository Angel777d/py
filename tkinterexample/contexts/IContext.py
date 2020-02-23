from utils.EventBus import IEventHandler
from utils.StateManager import IState


class IContext(IState, IEventHandler):
	def __init__(self, env, data=None):
		IState.__init__(self, env, data)
		IEventHandler.__init__(self, env.eventBus)

	def close(self):
		IEventHandler.close(self)
		IState.close(self)

	def openContext(self, contextName, **kwargs):
		self.sendEvent("context.open", name=contextName, **kwargs)

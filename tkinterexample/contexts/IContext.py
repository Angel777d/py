from utils.EventBus import IEventHandler
from utils.StateManager import IState


class IContext(IState, IEventHandler):
    def __init__(self, env, data=None):
        IState.__init__(self, env, data)
        IEventHandler.__init__(self, env.eventBus)

    def close(self):
        IEventHandler.close(self)
        IState.close(self)

    def openContext(self, contextName, data=None):
        eventData = {}
        if data:
            eventData.update(data)
        eventData["name"] = contextName
        self.sendEvent("context.open", eventData)

    def openWindow(self, windowName, data=None):
        eventData = {}
        if data:
            eventData.update(data)
        eventData["name"] = windowName
        self.sendEvent("win.open", eventData)

    def closeWindow(self):
        self.sendEvent("win.close")

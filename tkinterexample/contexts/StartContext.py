from contexts.IContext import IContext


class StartContext(IContext):
    def __init__(self, env, data=None):
        IContext.__init__(self, env, data=None)

    def addListeners(self, config):
        self.addEventListener("context.open", self.onContextOpen)
        self.addEventListener("context.close", self.onContextClose)
        self.addEventListener("win.open", self.onWindowOpen)
        self.addEventListener("win.close", self.onWindowClose)

        self.addEventListener("app.showConfig", lambda *args: self.sendEvent2("win.open", name="window.config"))

    def removeListeners(self):
        self.removeEventListener("context.open", self.onContextOpen)
        self.removeEventListener("context.close", self.onContextClose)
        self.removeEventListener("win.open", self.onWindowOpen)
        self.removeEventListener("win.close", self.onWindowClose)

    def onContextOpen(self, eventName, eventData):
        self.env.contextManager.openState(eventData["name"], eventData)

    def onContextClose(self, eventName, eventData):
        self.env.contextManager.closeState(eventData["name"], eventData)

    def onWindowOpen(self, eventName, eventData):
        self.env.windowsManager.openNext(eventData["name"], eventData)

    def onWindowClose(self, eventName, eventData):
        self.env.windowsManager.closeTop()

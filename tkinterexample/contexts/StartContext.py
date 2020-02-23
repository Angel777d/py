from contexts.IContext import IContext


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

        self.sendEvent("win.open", name="window.start")

    def onShowConfig(self, ev):
        self.sendEvent("win.open", name="window.config")

from utils.EventBus import IEventHandler


class IState:
    def __init__(self, env, data=None):
        self.env = env

    def close(self):
        self.env = None


class StateManager(IEventHandler):
    def __init__(self, env):
        self.env = env
        self.statesConfig = {}
        self.activeStates = {}
        IEventHandler.__init__(self, env.eventBus)

    def getListenersConfig(self):
        return {
            "context.open": self.onContextOpen,
            "context.close": self.onContextClose,
        }

    def onContextOpen(self, eventName, eventData):
        self.openState(eventData["name"], eventData)

    def onContextClose(self, eventName, eventData):
        self.closeState(eventData["name"])

    def applyConfig(self, config: dict):
        for stateName, stateClass in config.items():
            self.registerState(stateName, stateClass)
        return self

    def registerState(self, stateName, stateClass):
        assert stateName not in self.statesConfig, "there is already state named %s in config" % stateName
        self.statesConfig[stateName] = stateClass

    def openState(self, stateName, data=None):
        print("[State] open:", stateName)
        if stateName not in self.statesConfig:
            print("No state config for %s state" % stateName)
            return None

        if stateName in self.activeStates:
            print("State %s is already active" % stateName)
            return None

        stateClass = self.statesConfig.get(stateName)
        self.activeStates[stateName] = state = stateClass(self.env, data)
        return state

    def closeState(self, stateName):
        print("[State] close:", stateName)
        if stateName not in self.activeStates:
            print("State %s is not active" % stateName)
            return
        state = self.activeStates.pop(stateName)
        state.close()

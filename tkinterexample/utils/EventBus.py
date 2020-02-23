class Event:
    def __init__(self, name, data=None):
        self.name = name
        self.data = data

    def get(self, key):
        return self.data.get(key)

    def __repr__(self):
        return "%s, data: %s" % (self.name, self.data)


class EventBus:
    def __init__(self):
        self.events = {}

    def subscribe(self, eventName, callback):
        callbackList = self.events.setdefault(eventName, [])
        if callback in callbackList:
            return
        callbackList.append(callback)

    def unsubscribe(self, eventName, callback):
        callbackList = self.events.setdefault(eventName, [])
        if callback in callbackList:
            callbackList.remove(callback)

    def dispatch(self, eventName, eventData=None):
        self.dispatchEvent(Event(eventName, eventData))

    def dispatchEvent(self, ev):
        callbackList = self.events.setdefault(ev.name, [])
        print("[EventBus] dispatch:", len(callbackList), ev)
        for callback in callbackList:
            callback(ev)


class IEventHandler:
    def __init__(self, eventBus):
        self.__eventBus = eventBus
        self.__stored = {}
        config = self.getListenersConfig()
        self.addListeners(config)

    def close(self):
        self.removeListeners()
        self.clear()
        self.__eventBus = None
        self.__stored = None

    def clear(self):
        for eventName, callback in self.__stored.items():
            self.removeEventListener(eventName, callback)
        self.__stored.clear()

    def addEventListener(self, eventName, callback):
        self.__eventBus.subscribe(eventName, callback)
        self.__stored[eventName] = callback

    def removeEventListener(self, eventName, callback):
        self.__eventBus.unsubscribe(eventName, callback)

    def getListenersConfig(self):
        return {}

    def addListeners(self, config):
        for eventName, callback in config.items():
            self.addEventListener(eventName, callback)

    def removeListeners(self):
        pass

    def sendEvent(self, eventName, **kwargs):
        self.__eventBus.dispatch(eventName, kwargs)

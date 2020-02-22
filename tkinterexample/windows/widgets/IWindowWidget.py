from windows.IWindow import IWindow


class IWindowWidget:
    def __init__(self, window: IWindow):
        self.window: IWindow = window

    def sendEvent2(self, eventName, **kwargs):
        self.window.sendEvent2(eventName, **kwargs)

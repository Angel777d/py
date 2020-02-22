from tkinter import BOTH
from tkinter.ttk import Frame

from utils.EventBus import IEventHandler
from utils.StateManager import IState


class IWindow(IState, IEventHandler, Frame):

    def __init__(self, env, data=None):
        self.windowData = data if data else {}
        IState.__init__(self, env, data)
        IEventHandler.__init__(self, env.eventBus)
        Frame.__init__(self, self.env.root)

        self.elements = self.initUI()
        self.packUI()

        self.onInitialized(data)

    def getElement(self, elementName):
        return self.elements.get(elementName)

    def onInitialized(self, data):
        pass

    def initUI(self):
        pass

    def packUI(self):
        self.pack(fill=BOTH, expand=True)

    def close(self):
        self.destroy()
        IEventHandler.close(self)
        IState.close(self)
        self.elements = None

    def goBack(self):
        self.sendEvent("win.close")

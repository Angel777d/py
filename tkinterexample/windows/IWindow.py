from tkinter import BOTH
from tkinter.ttk import Frame
from typing import Dict

from model import Events
from utils.Env import Env
from utils.EventBus import IEventHandler


class IContainer:
    def __init__(self, name, parent):
        self.__name = name
        self.__children: Dict[str, IContainer] = {}
        self.__parent: IContainer = parent
        if parent:
            parent.addChild(name, self)

    @property
    def name(self):
        return self.__name

    def addChild(self, windowName, windowInstance):
        self.__children[windowName] = windowInstance

    def removeChild(self, windowName):
        return self.__children.pop(windowName)

    def closeChildren(self):
        children = [child for child in self.__children.values()]
        for child in children:
            child.close()

    def close(self):
        self.closeChildren()
        self.__parent.removeChild(self.__name)
        self.__children.clear()
        self.__children = None
        self.__parent = None

    def findWindow(self, name):
        if self.__name == name:
            return self

        for child in self.__children.values():
            result = child.findWindow(name)
            if result:
                return result

        return None


class IWidget(IEventHandler, Frame):
    def __init__(self, env, parent, **kwargs):
        self.env: Env = env
        IEventHandler.__init__(self, env.eventBus)
        Frame.__init__(self, parent, **kwargs)
        self.elements = self.initUI()
        self.onInitialized()

    def onInitialized(self):
        pass

    def close(self):
        self.destroy()
        IEventHandler.close(self)
        self.elements = None

    def getElement(self, elementName):
        return self.elements.get(elementName)

    def initUI(self):
        return {}


class IWindowContainer(IContainer):
    @property
    def viewContainer(self):
        return self


class IWindow(IWidget, IWindowContainer):
    def __init__(self, env: Env, name: str, parentWindow: IWindowContainer, **kwargs):
        IWindowContainer.__init__(self, name, parentWindow)
        IWidget.__init__(self, env, parentWindow.viewContainer, **kwargs)
        self.packUI()

    def packUI(self):
        self.pack(fill=BOTH, expand=True)

    def setData(self, data):
        pass

    def close(self):
        IWindowContainer.close(self)
        IWidget.close(self)


class RootWindow(IWindowContainer, IEventHandler):
    def __init__(self, env, config):
        self.env = env
        self.config = config
        IWindowContainer.__init__(self, "root", None)
        IEventHandler.__init__(self, env.eventBus)

    @property
    def viewContainer(self):
        return self.env.root

    def getListenersConfig(self):
        return {
            Events.WINDOW_OPEN: self.onWinOpen
        }

    def onWinOpen(self, ev):
        eventData = ev.data
        windowName = eventData.pop("name")
        parentName = eventData.pop("parent") if "parent" in eventData else None
        self.openWindow(windowName, parentName, **eventData)

    def openWindow(self, windowName, parentName, **kwargs):
        windowConfig = self.config.get(windowName)
        if not windowConfig:
            print("[RootWindow] can't find config for window:", windowName)

        windowClass, defaultParent = windowConfig
        parentName = parentName if parentName else defaultParent
        parentWindow = self.findWindow(parentName)
        if not parentWindow:
            print("[RootWindow] can't find parent window '%s' for '%s'" % (parentName, windowName))
            return

        window = windowClass(self.env, windowName, parentWindow, **kwargs)
        print("[RootWindow] open:", windowName, parentName)

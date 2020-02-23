from tkinter import BOTH, LEFT, Y, X, BOTTOM
from tkinter.ttk import Frame

from windows.IWindow import IWindow
from windows.MenuWidget import MenuWidget
from windows.PlayerWidget import PlayerWidget


class StartWindow(IWindow):

    def __init__(self, env, name, parentWindow, **kwargs):
        self.child = ""
        IWindow.__init__(self, env, name, parentWindow, **kwargs)

    @property
    def viewContainer(self):
        return self.getElement("mainFrame")

    def initUI(self):
        player = PlayerWidget(self.env, self)
        player.pack(side=BOTTOM, fill=X, expand=False)

        menu = MenuWidget(self.env, self)
        menu.pack(side=LEFT, fill=Y, expand=False)
        menu.onYandex = self.onStartClick

        mainFrame = Frame(self)
        mainFrame.pack(side=LEFT, fill=BOTH, expand=True)

        return {"mainFrame": mainFrame, "player": player}

    def onInitialized(self):
        self.sendEvent("win.open", name="window.localTracks", parent=self.name)

    def onStartClick(self):
        self.sendEvent("yandex.login")

    def addChild(self, windowName, windowInstance):
        self.closeChildren()
        IWindow.addChild(self, windowName, windowInstance)

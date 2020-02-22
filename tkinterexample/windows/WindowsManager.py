from utils.StateManager import StateManager


class WindowsManager(StateManager):
    def __init__(self, env):
        super().__init__(env)
        self.currentState = None
        self.windows = []

    def __openState(self, stateName, data=None):
        # print("WM::openState", stateName)
        if self.currentState:
            print("[WM] hide:", self.currentState)
            super().closeState(self.currentState)
            self.currentState = None

        print("[WM] show:", stateName)
        state = super().openState(stateName, data)
        if state:
            self.currentState = stateName
        return state

    def openState(self, stateName, data=None):
        raise NotImplemented

    def closeState(self, stateName):
        raise NotImplemented

    def openNext(self, name, data=None):
        self.windows.append((name, data))
        print("[WM] append window:", name, "queue:", len(self.windows))
        self.__openState(name, data)

    def closeTop(self):
        toRemove = self.windows.pop()
        print("[WM] remove window:", toRemove[0], "queue:", len(self.windows))
        if self.windows:
            name, data = self.windows[-1]
            self.__openState(name, data)
        else:
            self.__openState("")

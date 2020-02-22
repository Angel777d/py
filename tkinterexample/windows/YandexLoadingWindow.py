from time import sleep
from tkinter.ttk import Label

from utils.SimpleThread import SimpleThread
from utils.Utils import emptyHandler
from windows.IWindow import IWindow


class YandexLoadingWindow(IWindow):

    def __init__(self, env, data=None):
        super().__init__(env, data)
        self.count = 1
        self.thread = SimpleThread(self.tick, emptyHandler, "LoadingProgressThread")
        self.thread.start()

    def initUI(self):
        label = Label(self, text="Loading...")
        label.pack()
        return {"label": label}

    def tick(self):
        while self.env:
            count = self.count
            count += 1
            if count > 5:
                count = 1
            self.getElement("label").config(text="Loading" + "." * count)
            self.count = count
            sleep(1)

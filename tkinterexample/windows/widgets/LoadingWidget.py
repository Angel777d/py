from tkinter import BOTH
from tkinter.ttk import Label


class LoadingWidget(Label):
    def __init__(self, parent):
        Label.__init__(self, parent, text="Loading")
        self.initUI()

    def initUI(self):
        self.pack(fill=BOTH, expand=True)
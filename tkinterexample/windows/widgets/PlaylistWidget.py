from tkinter import Listbox, BOTH, TOP, BOTTOM, END
from tkinter.ttk import Frame, Button


class PlaylistWidget(Frame):
    def __init__(self, parent, downloadCallback):
        self.trackList = None
        Frame.__init__(self, parent)
        self.button = Button(self, text="Download", command=downloadCallback)
        self.listbox = Listbox(self)
        self.initUI()

    def initUI(self):
        self.pack(fill=BOTH, expand=True)
        self.listbox.pack(side=TOP, fill=BOTH, pady=5, expand=True)
        self.button.pack(side=BOTTOM)

    def setData(self, trackList):
        self.trackList = trackList
        self.listbox.delete(0, END)

        if not trackList:
            return

        for info in trackList:
            self.listbox.insert(END, info.title)

    def getSelectedItems(self):
        return [self.trackList[index] for index in self.listbox.curselection()]

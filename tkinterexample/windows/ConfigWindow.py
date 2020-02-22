from pathlib import Path
from tkinter import RIGHT, LEFT, filedialog, BOTTOM
from tkinter.ttk import Label, Frame, Button

from utils.Env import ConfigProps
from windows.IWindow import IWindow


class ConfigWindow(IWindow):

    def initUI(self):
        frame = Frame(self)
        frame.pack()

        libPath = self.env.config.get(ConfigProps.LIBRARY_PATH)
        label = Label(frame, text="LibraryPath: %s" % libPath)
        label.pack(side=LEFT)

        goback = Button(self, text="GoBack", command=self.goBack)
        goback.pack(side=BOTTOM)

        button = Button(frame, text="Change", command=self.onClick)
        button.pack(side=RIGHT)

        return {"label": label}

    def onClick(self):
        directory = filedialog.askdirectory()
        self.env.config.set(ConfigProps.LIBRARY_PATH, Path(directory).as_posix())

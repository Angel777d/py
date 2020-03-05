from pathlib import Path
from tkinter import RIGHT, LEFT, filedialog
from tkinter.ttk import Label, Frame, Button

from utils.Env import ConfigProps
from windows.IWindowTk import IWindowTk


class WindowConfig(IWindowTk):

	def initUI(self):
		frame = Frame(self)
		frame.pack()

		libPath = self.env.config.get(ConfigProps.LIBRARY_PATH)
		label = Label(frame, text="LibraryPath: %s" % libPath)
		label.pack(side=LEFT)

		button = Button(frame, text="Change", command=self.onClick)
		button.pack(side=RIGHT)

		return {"label": label}

	def onClick(self):
		directory = filedialog.askdirectory()
		self.env.config.set(ConfigProps.LIBRARY_PATH, Path(directory).as_posix())

from tkinter import BOTH
from tkinter.ttk import Frame

from utils.Env import Env
from utils.IWindow import IWindowContainer, IWidget, IWindow


class IWidgetTk(IWidget, Frame):
	def __init__(self, env, parent, **kwargs):
		Frame.__init__(self, parent, **kwargs)
		IWidget.__init__(self, env)

	def close(self):
		self.destroy()
		IWidget.close(self)


class IWindowTk(IWindow, Frame):
	def __init__(self, env: Env, name: str, parentWindow: IWindowContainer, **kwargs):
		Frame.__init__(self, parentWindow.viewContainer, **kwargs)
		IWindow.__init__(self, env, name, parentWindow)
		self.packUI()

	def packUI(self):
		self.pack(fill=BOTH, expand=True)

	def close(self):
		Frame.destroy(self)
		IWindow.close(self)
from tkinter import BOTH, LEFT, Y, X, BOTTOM, Canvas, RIGHT
from tkinter.ttk import Frame, Scrollbar

from ScrollSupport import ScrollElement
from model import Events
from windows.IWindow import IWindow
from windows.MenuWidget import MenuWidget
from windows.PlayerWidget import PlayerWidget


class WindowStart(IWindow, ScrollElement):

	def __init__(self, env, name, parentWindow, **kwargs):
		self.child = ""
		ScrollElement.__init__(self)
		IWindow.__init__(self, env, name, parentWindow, **kwargs)

	@property
	def viewContainer(self):
		return self.getElement("mainFrame")

	def initUI(self):
		player = PlayerWidget(self.env, self)
		player.pack(side=BOTTOM, fill=X, expand=False)

		menu = MenuWidget(self.env, self)
		menu.pack(side=LEFT, fill=Y, expand=False, padx=5)
		menu.onYandex = self.onStartClick

		container = Frame(self)
		canvas = Canvas(container)
		scrollbar = Scrollbar(container, orient="vertical", command=canvas.yview)
		scrollable_frame = Frame(canvas)

		scrollable_frame.bind(
			"<Configure>",
			lambda e: canvas.configure(
				scrollregion=canvas.bbox("all")
			)
		)

		canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
		canvas.configure(yscrollcommand=scrollbar.set)

		container.pack(side=LEFT, fill=BOTH, expand=True)
		canvas.pack(side=LEFT, fill=BOTH, expand=True)
		scrollbar.pack(side=RIGHT, fill=Y)

		self.initScroll(canvas)

		return {"mainFrame": scrollable_frame, "player": player, "canvas": canvas}

	def onScroll(self, event):
		print("WindowStart::_on_mousewheel")
		canvas = self.getElement("canvas")
		if event.num == 4 or event.delta > 0:
			canvas.yview_scroll(-1, "units")
		elif event.num == 5 or event.delta < 0:
			canvas.yview_scroll(1, "units")

	def onInitialized(self):
		self.sendEvent(Events.WINDOW_OPEN, name="window.localTracks", parent=self.name)

	def onStartClick(self):
		self.sendEvent("yandex.login")

	def addChild(self, windowName, windowInstance):
		self.closeChildren()
		IWindow.addChild(self, windowName, windowInstance)

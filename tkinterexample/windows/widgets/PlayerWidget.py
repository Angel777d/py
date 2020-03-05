from tkinter import Canvas, LEFT, BOTH, RIGHT, Label, TOP
from tkinter.ttk import Frame, Button

import Events
from windows.IWindowTk import IWidgetTk


class PlayerWidget(IWidgetTk):
	def __init__(self, env, parent, **kwargs):
		IWidgetTk.__init__(self, env, parent, **kwargs)

	def getListenersConfig(self):
		return {
			Events.PLAYER_PLAY: self.onTrackPlay
		}

	def initUI(self):
		image = Canvas(self, width=50, height=50)
		image.pack(side=LEFT)

		titleFrame = Frame(self)
		titleFrame.pack(side=LEFT, fill=BOTH)

		actionFrame = Frame(self)
		actionFrame.pack(side=RIGHT, fill=BOTH)

		title = Label(titleFrame, text="Title")
		title.pack(side=TOP)

		info = Label(titleFrame, text="Description")
		info.pack(side=TOP)

		playPause = Button(actionFrame, text=">/||", command=lambda: self.sendEvent(Events.PLAYER_TOGGLE_PAUSE))
		playPause.pack()

		return {"title": title, "info": info}

	def onTrackPlay(self, ev):
		self.getElement("title").configure(text=ev.get("title"))
		self.getElement("info").configure(text="%s (%s)" % (ev.get("artist"), ev.get("album")))

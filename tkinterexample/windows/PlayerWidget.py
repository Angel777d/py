from tkinter import Canvas, LEFT, BOTH, RIGHT, Label, TOP
from tkinter.ttk import Frame, Button

from model import Events
from model.MediaLibEntry import MediaLibEntry
from windows.IWindow import IWidget


class PlayerWidget(IWidget):
    def __init__(self, env, parent, **kwargs):
        IWidget.__init__(self, env, parent, **kwargs)

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

        playPause = Button(actionFrame, text=">/||", command=lambda: self.sendEvent2(Events.PLAYER_TOGGLE_PAUSE))
        playPause.pack()

        return {"title": title, "info": info}

    def onTrackPlay(self, eventName, eventData):
        self.showTrack(eventData.get("entry"))

    def showTrack(self, track: [MediaLibEntry, None]):
        if track:
            title: Label = self.getElement("title")
            title.configure(text=track.title)

            info: Label = self.getElement("info")
            info.configure(text="%s (%s)" % (track.artist, track.album))

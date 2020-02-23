from tkinter import Listbox, TOP, BOTH, END, BOTTOM, Canvas, SE, CENTER
from tkinter.ttk import Label, Button, Entry, Frame
from typing import List

from yandex_music import Landing, Playlist

from utils.Env import Env
from windows.IWindow import IWindow, IWindowContainer


class PersonalPlaylistWidget(Frame):
    SIZE = 200

    def __init__(self, parent, **kwargs):
        Frame.__init__(self, parent)
        self.canvas = Canvas(self, width=self.SIZE, height=self.SIZE)
        self.pack()

    def draw(self):
        c = self.canvas

        c.create_rectangle(0, 0, self.SIZE, self.SIZE, fill='gray', width=0)
        c.create_text(self.SIZE / 2, self.SIZE / 2, text="Playlist Name", justify=CENTER)  # , font="Verdana 14")
        c.create_text(self.SIZE, self.SIZE, text="Description", anchor=SE, fill="#FF00FF")
        c.bind("<Button-1>", self.onClick)

        c.pack()

    def doUpdate(self, playlist: Playlist):
        self.playlist = playlist

    def onClick(self, ev):
        pass


class YandexStartWindow(IWindow):

    def __init__(self, env: Env, name: str, parentWindow: IWindowContainer, **kwargs):
        self.playlists: List[Playlist] = []
        self.yandexData = env.data.get("yandex")
        super().__init__(env, name, parentWindow, **kwargs)
        self.onLandingLoaded()

    def initUI(self):
        label = Label(self, text="Playlists")
        label.pack()

        personal = Frame(self, height=100)
        # personal.pack(side=TOP, fill=X, expand=True)

        listbox = Listbox(self)
        listbox.pack(side=TOP, fill=BOTH, pady=5, expand=True)
        listbox.bind("<<ListboxSelect>>", self.onSelectionChanged)

        button = Button(self, text="Open", command=self.onClick)
        button.pack(side=BOTTOM)

        search = Entry(self)
        search.bind('<Return>', self.onSearch)
        search.pack()

        return {"listbox": listbox, "search": search, "personal": personal}

    def addListeners(self, config):
        self.addEventListener("yandex.landingLoaded", self.onLandingLoaded)

    def onLandingLoaded(self, *args):
        landing: Landing = self.yandexData.get("landing")
        self.showLanding(landing)

    def showLanding(self, landing: Landing):
        listbox = self.getElement("listbox")
        listbox.delete(0, END)

        if not landing:
            return

        for block in landing.blocks:
            # if block.type == 'personal-playlists':
            #     self.showPersonal(block)
            #     continue
            for entity in block.entities:
                # print("entity", entity.type, entity.data)
                if entity.type == "personal-playlist":
                    playlist: Playlist = entity.data.data
                elif entity.type == "playlist":
                    playlist: Playlist = entity.data
                else:
                    playlist = None

                if playlist:
                    listbox.insert(END, "%s: %s  (type: %s)" % (playlist.title, playlist.description, entity.type))
                    self.playlists.append(playlist)
                else:
                    # print("No playlist for entity:", entity.type, entity.data)
                    pass

        listbox.select_set(0)

    def showPersonal(self, block):
        frame = self.getElement("personal")
        for entity in block.entities:
            playlist: Playlist = entity.data.data
            widget = PersonalPlaylistWidget(frame)
            widget.doUpdate(playlist)

    def onClick(self):
        listbox = self.getElement("listbox")
        playlist = [self.playlists[index] for index in listbox.curselection()][0]
        self.sendEvent("yandex.openPlayList", playlist=playlist)

    def onSelectionChanged(self, ev):
        listbox = self.getElement("listbox")
        selection = listbox.curselection()
        print("Current selection:", selection, ev)
        pass

    def onSearch(self, ev):
        search: Entry = self.getElement("search")
        searchStr = search.get()
        print("got search string:", searchStr)
        self.sendEvent("yandex.search.request", entry=searchStr)

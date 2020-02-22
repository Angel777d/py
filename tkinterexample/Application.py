from contexts.AudioPlayerContext import AudioPlayerContext
from contexts.MediaLibContext import MediaLibContext
from contexts.StartContext import StartContext
from contexts.YandexContext import YandexContext
from contexts.YandexLoginContext import YandexLoginContext
from utils import MediaKeysListener
from utils.Env import Env
from utils.StateManager import StateManager
from windows.ConfigWindow import ConfigWindow
from windows.StartWindow import StartWindow
from windows.WindowsManager import WindowsManager
from windows.YandexLoadingWindow import YandexLoadingWindow
from windows.YandexPlaylistWindow import YandexPlaylistWindow
from windows.YandexStartWindow import YandexStartWindow
from windows.YnadexLoginWindow import YandexLoginWindow


class Application:
    def __init__(self):
        self.env = Env()
        self.yandex = None

        from tkinter import Tk
        root = Tk()
        root.geometry("800x600")
        root.title("Yandex music API example")
        self.env.root = root

        self.env.windowsManager = WindowsManager(self.env).applyConfig({
            "window.start": StartWindow,
            "window.config": ConfigWindow,
            "window.yandex.start": YandexStartWindow,
            "window.yandex.login": YandexLoginWindow,
            "window.yandex.loading": YandexLoadingWindow,
            "window.yandex.playlist": YandexPlaylistWindow,
        })

        self.env.contextManager = StateManager(self.env).applyConfig({
            "context.start": StartContext,
            "context.mediaLib": MediaLibContext,
            "context.yandex.login": YandexLoginContext,
            "context.yandex.start": YandexContext,
            "context.audioPlayer": AudioPlayerContext,
        })

        MediaKeysListener.setup({"media_play_pause": lambda: print("handlePlay")})

    def start(self):
        self.env.contextManager.openState("context.audioPlayer")
        self.env.contextManager.openState("context.mediaLib")
        self.env.contextManager.openState("context.start")
        self.env.contextManager.openState("context.yandex.login")

        self.env.windowsManager.openNext("window.start")
        # self.env.windowsManager.openNext("window.config")

        self.env.root.mainloop()

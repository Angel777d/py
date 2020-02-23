from contexts.AudioPlayerContext import AudioPlayerContext
from contexts.MediaLibContext import MediaLibContext
from contexts.StartContext import StartContext
from contexts.YandexContext import YandexContext
from contexts.YandexLoginContext import YandexLoginContext
from utils import MediaKeysListener
from utils.Env import Env
from utils.StateManager import StateManager
from windows.WindowConfig import WindowConfig
from windows.IWindow import RootWindow
from windows.WindowTracksAll import WindowTracksAll
from windows.WindowStart import WindowStart
from windows.WindowYandexLanding import WindowYandexLanding
from windows.WindowYandexPlaylist import WindowYandexPlaylist
from windows.WindowYandexLogin import WindowYandexLogin


class Application:
    def __init__(self):
        self.env = Env()
        self.yandex = None

        from tkinter import Tk
        root = Tk()
        root.geometry("800x600")
        root.title("Yandex music API example")
        self.env.root = root

        self.env.rootWindow = RootWindow(self.env, {
            "window.start": (WindowStart, "root"),
            "window.config": (WindowConfig, "window.start"),
            "window.localTracks": (WindowTracksAll, "window.start"),
            "window.yandex.login": (WindowYandexLogin, "window.start"),
            "window.yandex.landing": (WindowYandexLanding, "window.start"),
            "window.yandex.playlist": (WindowYandexPlaylist, "window.start"),
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
        self.env.contextManager.openState("context.start")
        self.env.root.mainloop()

from pynput import keyboard

from utils.Utils import emptyHandler

__KEY_TO_NAME = {
    keyboard.Key.media_next: "media_next",
    keyboard.Key.media_play_pause: "media_play_pause",
    keyboard.Key.media_previous: "media_previous",
    keyboard.Key.media_volume_down: "media_volume_down",
    keyboard.Key.media_volume_mute: "media_volume_mute",
    keyboard.Key.media_volume_up: "media_volume_up",
}

__HANDLERS = {}


def on_press(key):
    # handlerName = __KEY_TO_NAME.get(key, "None")
    # handler = __HANDLERS.get(handlerName, emptyHandler)
    # handler(key=key)
    pass


def on_release(key):
    pass


def setup(handlers: dict):
    __HANDLERS.update(handlers)
    listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    listener.start()

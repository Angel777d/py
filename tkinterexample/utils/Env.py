from utils import Defaults
from utils.Config import Config
from utils.EventBus import EventBus


class ConfigProps:
    LIBRARY_PATH = "library_path"


CONFIG_DEFAULTS = {
    ConfigProps.LIBRARY_PATH: Defaults.DEFAULT_LIBRARY_PATH,
}


class Env:
    def __init__(self):
        self.config = Config(Defaults.CONFIG_PATH, CONFIG_DEFAULTS)
        self.eventBus = EventBus()
        self.root = None

        self.windowsManager = None
        self.contextManager = None

        self.data = {}

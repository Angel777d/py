from pathlib import Path

APP_NAME = "app_name"
__USER_HOME = Path.home()

__CONFIG_FOLDER = "." + APP_NAME
__CONFIG_FILE_NAME = "config.json"
__DB_FILE_NAME = "db.sqlite"
__YANDEX_TOKEN_FILENAME = "yandex.token"

APP_PATH = Path(__USER_HOME, __CONFIG_FOLDER)
CONFIG_PATH = Path(APP_PATH, __CONFIG_FILE_NAME)
DB_PATH = Path(APP_PATH, __DB_FILE_NAME)
YANDEX_TOKEN_PATH = Path(APP_PATH, __YANDEX_TOKEN_FILENAME)

DEFAULT_LIBRARY_PATH = Path(__USER_HOME, "medialib").as_posix()

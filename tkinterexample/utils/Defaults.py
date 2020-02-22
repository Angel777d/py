from pathlib import Path

APP_NAME = "app_name"
__USER_HOME = Path.home()

__CONFIG_FOLDER = "." + APP_NAME
__CONFIG_FILE_NAME = "config.json"
__DB_FILE_NAME = "db.sqlite"
__YANDEX_TOKEN_FILENAME = "yandex.token"

CONFIG_PATH = Path(__USER_HOME, __CONFIG_FOLDER, __CONFIG_FILE_NAME)
DB_PATH = Path(__USER_HOME, __CONFIG_FOLDER, __DB_FILE_NAME)
YANDEX_TOKEN_PATH = Path(__USER_HOME, __CONFIG_FOLDER, __YANDEX_TOKEN_FILENAME)

DEFAULT_LIBRARY_PATH = Path(__USER_HOME, "medialib").as_posix()

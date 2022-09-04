import json
import logging
import pathlib

logging.basicConfig(
    filename='move_files.log',
    filemode='w',
    encoding='utf-8',
    format='[%(asctime)s] %(message)s',
    level=logging.INFO,
)

CONFIG_PATH = "config.json"

with open(CONFIG_PATH) as config:
    __configData: dict = json.JSONDecoder().decode(config.read())

logging.info(f"config loaded:\n {json.dumps(__configData, indent=4)} \n")

__rules = {}
for rule in __configData.get("rules", []):
    path = rule["targetPath"]
    extensions = rule['extensions']
    __rules.update({ext: path for ext in extensions})


def get_target(dir, filename):
    ext = pathlib.Path(filename).suffix
    return __rules.get(ext, None)


def get_watch_dir():
    return __configData.get("watchDir", pathlib.Path("~/downloads").expanduser())

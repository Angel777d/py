import os

DOWNLOADS = os.path.normpath("D:/downloads")

# rules
RULES = {}


def add_rule(path, exts):
    RULES.update({ext: path for ext in exts})


IMAGES = os.path.normpath("D:/Img")
VIDEO = os.path.normpath("D:/Movie")
TORRENTS = os.path.normpath("//Keenetic_Giga/watch")

add_rule(TORRENTS, (".torrent",))
add_rule(IMAGES, (".jpg", ".jpeg", ".png", ".gif",))
add_rule(VIDEO, (".avi", ".mp4", ".mkv",))


def get_target(dir, filename):
    ext = os.path.splitext(filename)[1]
    return RULES.get(ext, None)

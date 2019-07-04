import os
import shutil
import time

from . import rules

TIME_PERIOD = 5  # in seconds


def move(dirname, filename):
    target_dir = rules.get_target(dirname, filename)
    # print("ext", ext)
    if not target_dir:
        # print("No folder for", ext)
        return

    if not os.path.isdir(target_dir):
        # print("Error: target dir doesnt exist")
        return

    src = os.path.join(dirname, filename)
    shutil.move(src, target_dir)
    print("File moved:", src)


def move_files_task(lookup_dirs):
    for lookup_dir in lookup_dirs:
        lookup_dir = os.path.normpath(lookup_dir)
        for dirname, dirnames, filenames in os.walk(lookup_dir):
            for filename in filenames:
                move(dirname, filename)


def run(*args):
    print("Start watching files in:", args)
    while True:
        move_files_task(args)
        time.sleep(TIME_PERIOD)

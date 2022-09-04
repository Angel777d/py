import logging
import os
import shutil
import time

import rules

TIME_PERIOD = 5  # in seconds


def move(dirname, filename):
    target_dir = rules.get_target(dirname, filename)
    if not target_dir:
        logging.debug(f"no target dir can be found for: {filename}")
        return

    if not os.path.isdir(target_dir):
        logging.warning(f'target dir "{target_dir}" doesnt exist')
        return

    src = os.path.join(dirname, filename)
    try:
        shutil.move(src, target_dir)
        logging.info(f'file "{filename}" moved to "{target_dir}" dir')
    except Exception as ex:
        logging.error(f"some shit happens: {ex}")


def move_files_task(lookup_dirs):
    for lookup_dir in lookup_dirs:
        lookup_dir = os.path.normpath(lookup_dir)
        for root, dirs, files in os.walk(lookup_dir):
            for file in files:
                move(root, file)


def run():
    watch_dirs = rules.get_watch_dirs()
    logging.info(f"Start watching for: {watch_dirs}")
    while True:
        move_files_task(watch_dirs)
        time.sleep(TIME_PERIOD)

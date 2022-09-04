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
        for dirname, dirnames, filenames in os.walk(lookup_dir):
            for filename in filenames:
                move(dirname, filename)


def run(*args):
    logging.info("watch files started!")
    while True:
        move_files_task(args)
        time.sleep(TIME_PERIOD)

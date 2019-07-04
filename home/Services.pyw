# Used for running services in background

import threading

from download_processor import move_files


# from home_bot import home_bot


def run():
    lookup_dirs = [
        "D:/downloads",
    ]
    threading.Thread(target=move_files.run, args=lookup_dirs, name="download_processor").start()
    # threading.Thread(target=home_bot.run, name="home_bot").start()


run()

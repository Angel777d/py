from time import sleep

from Application import Application
from Mpg123Player import Mpg123Player

# MP3_PATH = "D:/123.mp3"
#
# player = Mpg123Player()
# player.play(MP3_PATH)
# sleep(3)
# player.togglePause()
# sleep(10)
# player.togglePause()
# sleep(3)
# player.stop()


def main():
    app = Application()
    app.start()


if __name__ == '__main__':
    main()
from threading import Thread
from time import sleep

from mpg123 import Mpg123, Out123

LIB_MPG_PATH = "mpg123/libmpg123-0.dll"
LIB_OUT_PATH = "mpg123/libout123-0.dll"


class ITrack:
    def stop(self):
        pass

    def setPause(self, value):
        pass


class Track(Thread, ITrack):
    def __init__(self, path):
        Thread.__init__(self, name="Mpg123 play")
        self.path = path
        mp3 = Mpg123(path, library_path=LIB_MPG_PATH)
        out = Out123(library_path=LIB_OUT_PATH)
        self.__frames = mp3.iter_frames(out.start)
        self.__out = out

        self.__pause = False
        self.__active = True

    def setPause(self, value):
        self.__pause = value

    def stop(self):
        self.__active = False
        self.__out = None
        self.__frames = None

    def run(self) -> None:
        while self.__active:
            if self.__pause:
                sleep(1)
                continue

            try:
                frame = next(self.__frames)
            except StopIteration:
                print("[---] track ended")
                break

            self.__out.play(frame)


class Mpg123Player:
    def __init__(self):
        self.__pause = False
        self.__track = ITrack()

    def play(self, path) -> bool:
        # TODO: handle errors
        self.stop()
        self.__pause = False
        self.__track = Track(path)
        self.__track.start()
        return True

    def stop(self):
        self.__track.stop()
        self.__track = ITrack()

    def togglePause(self):
        self.__pause = not self.__pause
        self.__track.setPause(self.__pause)

import os
from pathlib import Path

path = Path("C:/Program Files (x86)/VideoLAN/VLC")
print(path.as_posix())
os.add_dll_directory(path.as_posix())
import vlc


class PlayerStab:
	def stop(self):
		pass

	def set_pause(self, value):
		pass


class VLCPlayer:
	def __init__(self):
		self.__player = PlayerStab()
		self.__pause = False

	def play(self, path) -> bool:
		# TODO: handle errors
		self.stop()
		self.__pause = False
		self.__player.stop()
		self.__player = vlc.MediaPlayer(path.as_posix())
		self.__player.play()
		return True

	def stop(self):
		self.__player.stop()
		self.__player = PlayerStab()

	def togglePause(self):
		self.__pause = not self.__pause
		self.__player.set_pause(self.__pause)

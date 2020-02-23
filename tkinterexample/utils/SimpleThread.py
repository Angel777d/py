from threading import Thread
from types import FunctionType


class SimpleThread(Thread):
	def __init__(self, method: FunctionType, callback: FunctionType = None, name=""):
		Thread.__init__(self, name=name)
		self.method = method
		self.callback = callback

	def run(self) -> None:
		result = self.method()
		if self.callback:
			self.callback(result)

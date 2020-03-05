__root = None
__elements = []


def init(root):
	global __root
	__root = root
	__root.bind_all("<4>", _on_mousewheel)
	__root.bind_all("<5>", _on_mousewheel)
	__root.bind_all("<MouseWheel>", _on_mousewheel)


def close():
	__root.unbind("<4>")
	__root.unbind("<5>")
	__root.unbind("<MouseWheel>")


def _on_mousewheel(event):
	if not __elements:
		return

	__elements[-1].onScroll(event)


def _addElement(element):
	__elements.append(element)


def _removeElement(element):
	__elements.remove(element)


class ScrollElement:
	def __init__(self):
		self.target = None
		self.binded = False

	def initScroll(self, target):
		self.finiScroll()
		self.target = target
		self.target.bind("<Enter>", self.__bind)
		self.target.bind("<Leave>", self.__unbind)

	def finiScroll(self):
		if not self.target:
			return
		self.__unbind()
		self.target.unbind("<Enter>", self.__bind)
		self.target.unbind("<Leave>", self.__unbind)
		self.target = None
		self.binded = False

	def __bind(self, ev=None):
		if self.binded:
			return
		_addElement(self)
		self.binded = True

	def __unbind(self, ev=None):
		if not self.binded:
			return
		self.binded = False
		_removeElement(self)

	def onScroll(self, event):
		print("No scroll override")
		pass

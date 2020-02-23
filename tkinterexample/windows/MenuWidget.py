from tkinter import TOP, X, BOTTOM
from tkinter.ttk import Button, Frame

from model import Events
from windows.IWindow import IWidget
from windows.widgets.CaptionEntryWidget import CaptionEntry


class MenuWidget(IWidget):
	def getListenersConfig(self):
		return {"yandex.client.dataChanged": self.onYandexLogin}

	def initUI(self):
		frame = Frame(self)
		home = Button(frame, text="Home", command=lambda: self.sendEvent(Events.WINDOW_OPEN, name="window.localTracks"))

		home.pack(side=TOP, fill=X)
		frame.pack(side=TOP, fill=X, pady=20)

		frame = Frame(self)
		yandexLogin = Button(frame, text="Yandex Login", command=lambda: self.sendEvent("yandex.login"))
		yandexShow = Button(frame, text="Yandex Home", command=lambda: self.sendEvent("yandex.start"))
		yandexSearch = CaptionEntry(frame, "Yandex Search")
		yandexSearch.bind('<Return>', self.onSearch)

		yandexLogin.pack(side=TOP, fill=X, pady=2)
		yandexShow.pack(side=TOP, fill=X, pady=2)
		yandexSearch.pack(side=TOP, fill=X, pady=2)
		frame.pack(side=TOP, fill=X, pady=10)

		frame = Frame(self)
		config = Button(frame, text="Config", command=lambda: self.sendEvent("app.showConfig"))
		config.pack(side=TOP, fill=X)
		frame.pack(side=BOTTOM, fill=X)

		return {"yandexSearch": yandexSearch, "yandexLogin": yandexLogin, "yandexShow": yandexShow}

	def onSearch(self, ev):
		search: CaptionEntry = self.getElement("yandexSearch")
		searchStr = search.getValue()
		print("got search string:", searchStr)
		self.sendEvent("yandex.request.search", entry=searchStr)
		self.sendEvent(Events.WINDOW_OPEN, name="window.yandex.search")

	def onInitialized(self):
		self.updateYandex()

	def onYandexLogin(self, ev):
		self.updateYandex()

	def updateYandex(self):
		isYandexReady = self.env.data.get("yandex").get("client")
		if isYandexReady:
			self.getElement("yandexSearch").pack(side=TOP, fill=X, pady=2)
			self.getElement("yandexShow").pack(side=TOP, fill=X, pady=2)
			self.getElement("yandexLogin").pack_forget()
		else:
			self.getElement("yandexSearch").pack_forget()
			self.getElement("yandexShow").pack_forget()
			self.getElement("yandexLogin").pack(side=TOP, fill=X, pady=2)

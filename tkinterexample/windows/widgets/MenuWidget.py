from tkinter import TOP, X, BOTTOM
from tkinter.ttk import Button, Frame

import Events
from windows.IWindowTk import IWidgetTk
from windows.widgets.CaptionEntryWidget import CaptionEntry


class MenuWidget(IWidgetTk):
	def getListenersConfig(self):
		return {"yandex.client.dataChanged": self.onYandexLogin}

	def initUI(self):
		frame = Frame(self)
		yandexShow = Button(frame, text="Yandex Home", command=lambda: self.sendEvent("yandex.start"))
		yandexSearch = CaptionEntry(frame, "Yandex Search")
		yandexSearch.bind('<Return>', self.onSearch)

		yandexShow.pack(side=TOP, fill=X, pady=2)
		yandexSearch.pack(side=TOP, fill=X, pady=2)
		frame.pack(side=TOP, fill=X, pady=10)

		frame = Frame(self)
		config = Button(frame, text="Config", command=lambda: self.sendEvent("app.showConfig"))
		config.pack(side=TOP, fill=X)
		frame.pack(side=BOTTOM, fill=X)

		return {
			"yandexSearch": yandexSearch,
			"yandexShow": yandexShow
		}

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
		else:
			self.getElement("yandexSearch").pack_forget()
			self.getElement("yandexShow").pack_forget()

from windows.IWindowTk import IWindowTk
from windows.widgets.SimpleLoginWidget import SimpleLogin


class WindowYandexLogin(IWindowTk):
	def initUI(self):
		SimpleLogin(self, self.onLoginApply, self.close)

	def onLoginApply(self, login, password):
		self.sendEvent("yandex.login.apply", login=login, password=password)

from tkinter import Listbox, TOP, BOTH, END

from windows.IWindow import IWidget


class TrackListWidget(IWidget):
	def initUI(self):
		listbox = Listbox(self)
		listbox.pack(side=TOP, fill=BOTH, pady=5, expand=True)
		return {"listbox": listbox}

	def doUpdate(self, trackList):
		listbox = self.getElement("listbox")
		listbox.delete(0, END)

		if not trackList:
			return

		for info in trackList:
			listbox.insert(END, info.title)

	def curselection(self):
		listbox = self.getElement("listbox")
		return listbox.curselection()
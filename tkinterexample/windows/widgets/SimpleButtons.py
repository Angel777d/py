from tkinter import BOTH, BOTTOM, RIGHT, X
from tkinter.ttk import Frame, Button

from utils.Utils import emptyHandler


class SimpleButtons(Frame):
	def __init__(self, parent, okHandler=emptyHandler, cancelHandler=emptyHandler):
		Frame.__init__(self, parent)
		self.okHandler = okHandler
		self.cancelHandler = cancelHandler
		self.initUI()

	def initUI(self):
		buttonFrame = Frame(self)
		closeButton = Button(buttonFrame, text="Close", command=self.cancelHandler)
		okButton = Button(buttonFrame, text="OK", command=self.okHandler)

		self.pack(fill=BOTH, expand=True)
		buttonFrame.pack(side=BOTTOM, fill=X, expand=False)
		closeButton.pack(side=RIGHT, padx=5, pady=5)
		okButton.pack(side=RIGHT)

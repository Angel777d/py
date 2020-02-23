from tkinter import StringVar
from tkinter.ttk import Entry


class CaptionEntry(Entry):
	def __init__(self, parent, caption="Some text her", captionColor="grey", **kwargs):
		self.captionColor = captionColor
		self.defaultColor = kwargs.get("foreground", "black")
		self.caption = caption

		self.empty = True
		self.focused = False

		self.content = StringVar()
		self.content.set(caption)

		kwargs["textvariable"] = self.content
		kwargs["foreground"] = self.captionColor
		Entry.__init__(self, parent, **kwargs)
		self.content.trace("w", self.onContentChanged)

		self.bind("<FocusIn>", self.onFocusIn)
		self.bind("<FocusOut>", self.onFocusOut)

	def getValue(self):
		return self.content.get()

	def onContentChanged(self, *args, **kwargs):
		if not self.focused:
			return
		self.empty = not bool(self.content.get())
		# print("[---]", "onContentChanged", self.content.get(), self.empty)

	def onFocusIn(self, ev):
		# print("[---]", "focus in", ev)
		if self.empty:
			self.content.set("")

		self.config(foreground=self.defaultColor)
		self.focused = True

	def onFocusOut(self, ev):
		# print("[---]", "focus out", ev)
		self.focused = False
		if self.empty:
			self.content.set(self.caption)
			self.config(foreground=self.captionColor)

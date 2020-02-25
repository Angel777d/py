#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# get from https://gist.github.com/novel-yet-trivial/3eddfce704db3082e38c84664fc1fdf8

from tkinter import Canvas, LEFT, BOTH
from tkinter.ttk import Widget, Frame


class OuterFrame(Frame):
	def __init__(self, master=None, **kw):
		self.rel = None
		super().__init__(master, **kw)

	def setRelated(self, rel):
		self.rel = rel

	def destroy(self):
		self.rel.destroy()
		super().destroy()


class VerticalScrolledFrame:
	"""
	A vertically scrolled Frame that can be treated like any other Frame
	ie it needs a master and layout and it can be a master.
	:width:, :height:, :bg: are passed to the underlying Canvas
	:bg: and all other keyword arguments are passed to the inner Frame
	note that a widget layed out in this frame will have a self.master 3 layers deep,
	(outer Frame, Canvas, inner Frame) so
	if you subclass this there is no built in way for the children to access it.
	You need to provide the controller separately.
	"""

	def __init__(self, master, **kwargs):
		width = kwargs.pop('width', None)
		height = kwargs.pop('height', None)
		bg = kwargs.pop('bg', kwargs.pop('background', None))
		self.outer = OuterFrame(master, **kwargs)

		# self.vsb = Scrollbar(self.outer, orient=VERTICAL)
		# self.vsb.pack(fill=Y, side=RIGHT)
		self.canvas = Canvas(self.outer, highlightthickness=0, width=width, height=height, bg=bg)
		self.canvas.pack(side=LEFT, fill=BOTH, expand=True)
		# self.canvas['yscrollcommand'] = self.vsb.set
		# mouse scroll does not seem to work with just "bind"; You have
		# to use "bind_all". Therefore to use multiple windows you have
		# to bind_all in the current widget
		self.canvas.bind("<Enter>", self._bind_mouse)
		self.canvas.bind("<Leave>", self._unbind_mouse)
		# self.vsb['command'] = self.canvas.yview

		self.inner = Frame(self.canvas, bg=bg)
		# pack the inner Frame into the Canvas with the topleft corner 4 pixels offset
		self.canvas.create_window(4, 4, window=self.inner, anchor='nw')
		self.inner.bind("<Configure>", self._on_frame_configure)

		self.outer_attr = set(dir(Widget))

		self.outer.setRelated(self)

	def __getattr__(self, item):
		if item in self.outer_attr:
			# geometry attributes etc (eg pack, destroy, tkraise) are passed on to self.outer
			return getattr(self.outer, item)
		else:
			# all other attributes (_w, children, etc) are passed to self.inner
			return getattr(self.inner, item)

	def destroy(self):
		self._unbind_mouse()

	def _on_frame_configure(self, event=None):
		x1, y1, x2, y2 = self.canvas.bbox("all")
		height = self.canvas.winfo_height()
		self.canvas.config(scrollregion=(0, 0, x2, max(y2, height)))

	def _bind_mouse(self, event=None):
		self.canvas.bind_all("<4>", self._on_mousewheel)
		self.canvas.bind_all("<5>", self._on_mousewheel)
		self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

	def _unbind_mouse(self, event=None):
		self.canvas.unbind_all("<4>")
		self.canvas.unbind_all("<5>")
		self.canvas.unbind_all("<MouseWheel>")

	def _on_mousewheel(self, event):
		"""Linux uses event.num; Windows / Mac uses event.delta"""
		if event.num == 4 or event.delta > 0:
			self.canvas.yview_scroll(-1, "units")
		elif event.num == 5 or event.delta < 0:
			self.canvas.yview_scroll(1, "units")

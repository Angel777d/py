#!/usr/bin/python
# -*- coding: utf-8 -*-
from tkinter import BOTH, X, TOP
from tkinter.ttk import Frame

from windows.CaptionEntryWidget import CaptionEntry
from windows.SimpleButtons import SimpleButtons


class SimpleLogin(Frame):
    def __init__(self, parent, loginCallback=None, cancelCallback=None):
        self.parent = parent
        self.loginCallback = loginCallback
        self.cancelCallback = cancelCallback
        Frame.__init__(self, parent)
        self.login, self.password = self.initUI()

    def initUI(self):
        login = CaptionEntry(self, "Login", foreground="red")
        password = CaptionEntry(self, "Password", foreground="red")

        self.pack(fill=BOTH, expand=True)
        login.pack(side=TOP, fill=X, padx=5, pady=5, expand=True)
        password.pack(side=TOP, fill=X, padx=5, pady=5, expand=True)

        SimpleButtons(self, self.onApply, self.onCancel)

        return login, password

    def showError(self, message):
        # todo: implement
        pass

    def onApply(self):
        self.loginCallback(self.login.getValue(), self.password.getValue())

    def onCancel(self):
        self.cancelCallback()

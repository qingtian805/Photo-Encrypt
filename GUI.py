# -*- coding: utf-8 -*-
from pathlib import WindowsPath
from tkinter import *
from EnDecrypt import Encrypt_f, Decrypt_f
from hashlib import md5

class Utility(Frame): #button功能区
    def createWidgets(self):
        
    def __init__(self, master = None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()

class Path(Frame): #路径选择区
    def createWidgets(self):
        
    def __init__(self, master = None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()

class Terminal(Frame): #仿终端状态栏
    def createWidgets(self):
        
    def __init__(self, master = None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()

class ShowPhoto(Frame): #图像显示区
    def createWidgets(self):
        
    def __init__(self, master = None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()



window = Tk()

window.mainloop()
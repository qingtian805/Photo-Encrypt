# -*- coding: utf-8 -*-
from pathlib import WindowsPath
from tkinter import *
from EnDecrypt import Encrypt_f, Decrypt_f
from hashlib import md5

from numpy import select

class Utility(Frame): #button功能区
    varKey = StringVar()
    varKey.set("")
    def eKeyEncrypt(self):
        key = self.eKey.get()
        Encrypt_f()
    def eKeyDecrypt(self):
        key = self.eKey.get()
        Decrypt_f()
    def createWidgets(self):
        self.lKey = Label(self, text="密钥")
        self.lKey.pack(side="top")
        
        self.eKey = Entry(self)
        self.eKey.pack(side="top")

        self.bEncrypt = Button(self, text="加密", command="self.eKeyEncrypt")
        self.bEncrypt.pack(side="left")

        self.bDecrypt = Button(self, text="解密", command="self.eKeyDecrypt")
        self.bDecrypt.pack(side="right")
    def __init__(self, master = None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()

class Path(Frame): #路径选择区
    
    def createWidgets(self):
        self.ePath = Entry(self)
        self.ePath.pack(side="left")

        self.bGetPath = Button(self, text="选择")
        self.bGetPath.pack(side="left")
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
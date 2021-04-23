# -*- coding: utf-8 -*-
from EnDecrypt import Decrypt_f, Encrypt_f
from tkinter import *
from tkinter import filedialog
from hashlib import md5

from numpy import select
#这是两个临时函数，用于替代加密核心算法
def Encrypt_f(): 
    print("Encrypt")
def Decrypt_f():
    print("Decrypt")

class Utility(Frame): #button功能区
    varKey = StringVar(value="") #密钥变量
    def eKeyEncrypt(self): #加密按钮指令
        key = self.eKey.get()
        self.bEncrypt.config(command=DISABLED)
        Terminal.newNotice(notice="正在加密")
        Encrypt_f()
        self.bEncrypt.config(command=self.eKeyEncrypt)
        Terminal.newNotice(notice="加密成功")
    def eKeyDecrypt(self): #解密按钮指令
        key = self.eKey.get()
        self.bDecrypt.config(command=DISABLED)
        Decrypt_f()
        self.bDecrypt.config(command=self.eKeyDecrypt)
    def createWidgets(self):
        self.lKey = Label(self, text="密钥") #显示“密钥”
        self.lKey.pack(side="top")
        
        self.eKey = Entry(self)
        self.eKey.pack(side="top") #密钥输入框

        self.bEncrypt = Button(self, text="加密", command=self.eKeyEncrypt) #加密按钮
        self.bEncrypt.pack(side="left")

        self.bDecrypt = Button(self, text="解密", command=self.eKeyDecrypt) #解密按钮
        self.bDecrypt.pack(side="right")
    def __init__(self, master = None):
        Frame.__init__(self, master)
        self.grid(row=1, column=2) #放置在上中
        self.createWidgets()

class MessagePath(Frame): #明文路径选择区
    path = StringVar(value="") #路径变量
    def getPath(self): #按钮函数
        self.path = self.ePath.get() #尝试获取用户输入的路径，无则打开路径选择框
        if self.path != "":
            self.path = filedialog.askopenfilename()
    def createWidgets(self):
        self.ePath = Entry(self, textvariable=self.path) #左侧输入框，绑定路径变量
        self.ePath.pack(side="left")

        self.bGetPath = Button(self, text="选择文件", command="self.getPath") #右侧按钮
        self.bGetPath.pack(side="left")
    def __init__(self, master = None):
        Frame.__init__(self, master)
        self.grid(row=2, column=1) #放置在下左
        self.createWidgets()

class EncryptedPath(Frame): #密文路径选择区
    path = StringVar(value="") #路径变量
    def getPath(self): #按钮函数
        self.path = self.ePath.get() #尝试获取用户输入的路径，无则打开路径选择框
        if self.path != "":
            self.path = filedialog.askopenfilename()
    def createWidgets(self):
        self.ePath = Entry(self, textvariable=self.path) #左侧输入框，绑定路径变量
        self.ePath.pack(side="left")

        self.bGetPath = Button(self, text="选择文件", command="self.getPath") #右侧按钮
        self.bGetPath.pack(side="left")
    def __init__(self, master = None):
        Frame.__init__(self, master)
        self.grid(row=2, column=3) #放置在下右
        self.createWidgets()


class Terminal(Frame): #仿终端状态栏
    def newNotice(self, notice): #添加新消息
        self.textBar.insert(notice + "\n")
    def createWidgets(self):
        self.textBar = Text(self, state=DISABLED)
        self.textBar.pack()
    def __init__(self, master = None):
        Frame.__init__(self, master)
        self.grid(row=2, column=2) #放置在下中
        self.createWidgets()

class MessageShowPhoto(Frame): #明文图像显示区
    def showPhoto(self, path):
        image = PhotoImage
        self.cPhoto.create_image()
    def createWidgets(self):
        self.lPhoto = Label(self)
        self.lPhoto.pack()

        self.cPhoto = Canvas(self)
        self.cPhoto.pack()
    def __init__(self, master = None):
        Frame.__init__(self, master)
        self.grid(row=1, column=1) #放置在上左
        self.createWidgets()

class EncryptedShowPhoto(Frame): #密文图像显示区
    def createWidgets(self):
        self.lPhoto = Label(self)
        self.lPhoto.pack()

        self.cPhoto = Canvas(self)
        self.cPhoto.pack()
    def __init__(self, master = None):
        Frame.__init__(self, master)
        self.grid(row=1, column=3) #放置在上右
        self.createWidgets()



window = Tk()

window.mainloop()
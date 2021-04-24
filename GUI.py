# -*- coding: utf-8 -*-
from EnDecrypt import Decrypt_f, Encrypt_f
from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk
from hashlib import md5
from datetime import datetime

from numpy import select
#这是两个临时函数，用于替代加密核心算法
def Encrypt_f(lamb, x0, wpath, opath='', im=None): 
    print("Encrypt")
def Decrypt_f(lamb, x0, wpath, opath='', im=None):
    print("Decrypt")

pathOpened = False #这个定义与两个路径选择有关，如果选择了打开路径第二次则为保存路径（标记True）

class Terminal(Frame): #仿终端状态栏
    def newNotice(self, notice): #添加新消息
        self.textBar.config(state=NORMAL)
        self.textBar.insert(datetime.now().strftime("%Y-%m-%d %H:%M%S") + notice + "\n")
        self.textBar.config(state=DISABLED)
    def createWidgets(self):
        self.textBar = Text(self, state=DISABLED)
        self.textBar.pack()
    def __init__(self, master):
        Frame.__init__(self, master)
        self.grid(row=2, column=2) #放置在下中
        self.createWidgets()

class MessageShowPhoto(Frame): #明文图像显示区
    def showPhoto(self, im):
        im = im.resize((512.512), Image.ANTIALIAS)
        photo = ImageTk(im)
        self.lPhoto.config(image=photo)
    def createWidgets(self):
        self.lText = Label(self, text="明文图像")
        self.lText.pack()

        self.lPhoto = Label(self, width=512, height=512)
        self.lPhoto.pack()
    def __init__(self, master = None):
        Frame.__init__(self, master)
        self.grid(row=1, column=1) #放置在上左
        self.createWidgets()

class EncryptedShowPhoto(Frame): #密文图像显示区
    def showPhoto(self, im):
        im = im.resize((512.512), Image.ANTIALIAS)
        photo = ImageTk(im)
        self.lPhoto.config(image=photo)
    def createWidgets(self):
        self.lText = Label(self, text="密文图像")
        self.lText.pack()

        self.lPhoto = Label(self, width=512, height=512)
        self.lPhoto.pack()
    def __init__(self, master):
        Frame.__init__(self, master)
        self.grid(row=1, column=3) #放置在上右
        self.createWidgets()

class MessagePath(Frame): #明文路径选择区
    selectEpName = StringVar(value="") #路径变量
    def getPath(self):
        return self.selectEpName.get()
    def choose_ep(self): #按钮函数
        global pathOpened
        self.selectEpName = self.ePath.get() #尝试获取用户输入的路径，无则打开路径选择框
        if self.selectEpName != "": #判断用户是否在密文区选择了密文图像
            if pathOpened:
                self.selectEpName = filedialog.asksaveasfilename(title="解密图像保存为")
            else:
                self.selectEpName = filedialog.askopenfilename(title="上传要加密的图像")
    def createWidgets(self):
        self.ePath = Entry(self, width=40, textvariable=self.selectEpName) #左侧输入框，绑定路径变量
        self.ePath.pack(side="left")

        self.bGetPath = Button(self, width=6, height=1, text="选择文件", command=self.choose_ep) #右侧按钮
        self.bGetPath.pack(side="left")
    def __init__(self, master):
        Frame.__init__(self, master)
        self.grid(row=2, column=1) #放置在下左
        self.createWidgets()

class EncryptedPath(Frame): #密文路径选择区
    selectDpName = StringVar(value="") #路径变量
    def getPath(self):
        return self.selectDpName.get()
    def choose_dp(self): #按钮函数
        global pathOpened
        self.selectDpName = self.ePath.get() #尝试获取用户输入的路径，无则打开路径选择框
        if self.selectDpName != "": #判断用户是否在明文区选择了密文图像
            if pathOpened:
                self.selectDpName = filedialog.asksaveasfilename(title="加密图像保存为")
            else:
                self.selectDpName = filedialog.askopenfilename(title="上传要解密的图像")
    def createWidgets(self):
        self.ePath = Entry(self, width=40, textvariable=self.selectDpName) #左侧输入框，绑定路径变量
        self.ePath.pack(side="left")

        self.bGetPath = Button(self, width=6, height=1, text="选择文件", command=self.choose_dp) #右侧按钮
        self.bGetPath.pack(side="left")
    def __init__(self, master = None):
        Frame.__init__(self, master)
        self.grid(row=2, column=3) #放置在下右
        self.createWidgets()

class Utility(Frame): #button功能区
    varKey = StringVar(value="") #密钥变量
    def eKeyEncrypt(self, self_MessagePath: MessagePath, self_Terminal): #加密按钮指令
        key = self.eKey.get() #获得加密密钥
        self.bEncrypt.config(command=DISABLED) #设置按钮不可用，防止二次加密
        EpPath = self_MessagePath.getPath() #获得加密路径
        Terminal.newNotice(self_Terminal,"正在加密") #显示状态信息
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
    def __init__(self, master):
        Frame.__init__(self, master)
        self.grid(row=1, column=2) #放置在上中
        self.createWidgets()

    
window = Tk()

window.mainloop()
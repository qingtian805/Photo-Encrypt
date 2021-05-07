# -*- coding: utf-8 -*-
from EnDecrypt import Decrypt_f, Encrypt_f
from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk, UnidentifiedImageError
from datetime import datetime
import KeyMapping as km

from numpy import select
#这是两个临时函数，用于替代加密核心算法
#def Encrypt_f(lamb, x0, wpath, opath='', im=None): 
#    print("Encrypt")
#    return im
#def Decrypt_f(lamb, x0, wpath, opath='', im=None):
#    print("Decrypt")
#    return im

pathOpened = False #这个定义与两个路径选择有关，如果选择了打开路径第二次则为保存路径（标记True）
window = Tk() #似乎需要先定义这个后面才能跑……
photoMessage = PhotoImage()
photoEncrypted = PhotoImage()

class Terminal(Frame): #仿终端状态栏
    def newNotice(self, notice): #添加新消息
        self.textBar.config(state=NORMAL)
        self.textBar.insert("end", datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\n" + notice + "\n")
        self.textBar.config(state=DISABLED)
    def createWidgets(self):
        self.textBar = Text(self, state=DISABLED, width=40, height=5)
        self.textBar.pack()
    def __init__(self, master):
        Frame.__init__(self, master)
        self.grid(row=2, column=2) #放置在下中
        self.createWidgets()

class MessageShowPhoto(Frame): #明文图像显示区
    def showPhoto(self, path: str = '', im: Image = None):
        global photoMessage
        try:
            if im == None:
                self.im = Image.open(path)
            else: self.im = im
            resizedIm = self.im.resize((384,384), Image.ANTIALIAS)
            photoMessage = ImageTk.PhotoImage(resizedIm)
            self.lPhoto.config(image=photoMessage, width=384, height=384)
        except FileNotFoundError:
            self.terminal.newNotice("文件不存在，请输入正确的路径")
        except UnidentifiedImageError:
            self.terminal.newNotice("文件不是一个图片，请选择图像文件")
    def createWidgets(self):
        self.lText = Label(self, text="明文图像")
        self.lText.pack()

        self.lPhoto = Label(self, width=46, height=23)
        self.lPhoto.pack()
    def __init__(self, master, terminal: Terminal):
        Frame.__init__(self, master)
        self.terminal = terminal
        self.grid(row=1, column=1) #放置在上左
        self.createWidgets()

class EncryptedShowPhoto(Frame): #密文图像显示区
    def showPhoto(self, path: str = '', im: Image = None):
        global photoEncrypted
        try:
            if im == None:
                self.im = Image.open(path)
            else: self.im = im
            resizedIm = self.im.resize((384,384), Image.ANTIALIAS)
            photoEncrypted = ImageTk.PhotoImage(resizedIm)
            self.lPhoto.config(image=photoEncrypted, width=384, height=384)
        except FileNotFoundError:
            self.terminal.newNotice("文件不存在，请输入正确的路径")
        except UnidentifiedImageError:
            self.terminal.newNotice("文件不是一个图片，请选择图像文件")
    def createWidgets(self):
        self.lText = Label(self, text="密文图像")
        self.lText.pack()

        self.lPhoto = Label(self, width=46, height=23)
        self.lPhoto.pack()
    def __init__(self, master, terminal: Terminal):
        Frame.__init__(self, master)
        self.terminal = terminal
        self.grid(row=1, column=3) #放置在上右
        self.createWidgets()

class MessagePath(Frame): #明文路径选择区
    selectEpName = StringVar() #路径变量
    pathOpened = False
    def getPath(self):
        return self.selectEpName.get()
    def choose_ep(self): #按钮函数
        global pathOpened
        if self.ePath.get() == '': #尝试获取用户输入的路径，无则打开路径选择框
            self.terminal.newNotice("请输入路径或浏览")
        else: #用户输入了路径，获取
            self.selectEpName.set(self.ePath.get())
            if pathOpened ^ self.pathOpened:
                self.terminal.newNotice("已选择解密保存路径:" + self.selectEpName.get())
            else:
                self.terminal.newNotice("已选择明文文件路径:" + self.selectEpName.get())
            self.photoBar.showPhoto(self.selectEpName.get())
            pathOpened = True
            self.pathOpened = True
    def choose_ep_browser(self):
        global pathOpened
        if pathOpened ^ self.pathOpened: #判断用户是否在密文区选择了密文图像或上次在本类中打开
            self.selectEpName.set(filedialog.asksaveasfilename(title="解密图像保存为",defaultextension = ".jpg",filetypes  = [("JPG File", ".jpg"),\
                                                                                                    ("BMP File", ".bmp"),\
                                                                                                    ("PNG File", ".png"),\
                                                                                                    ("TIFF File",".tiff"),\
                                                                                                    ("All Files", ".*")]))
            self.terminal.newNotice("已选择解密保存路径:" + self.selectEpName.get())
        else:
            self.selectEpName.set(filedialog.askopenfilename(title="上传要加密的图像"))
            self.terminal.newNotice("已选择明文文件路径:" + self.selectEpName.get())
            self.photoBar.showPhoto(self.selectEpName.get())
            pathOpened = True
            self.pathOpened = True
    def createWidgets(self):
        self.ePath = Entry(self, width=40, textvariable=self.selectEpName) #左侧输入框，绑定路径变量
        self.ePath.pack(side="left")

        self.bBrowser = Button(self, width=5, height=1, text="浏览...", command=self.choose_ep_browser)
        self.bBrowser.pack(side="left")

        self.bGetPath = Button(self, width=6, height=1, text="选择文件", command=self.choose_ep) #右侧按钮
        self.bGetPath.pack(side="left")
    def __init__(self, master, terminal: Terminal, photoBar: MessageShowPhoto):
        Frame.__init__(self, master)
        self.terminal = terminal
        self.photoBar = photoBar
        self.grid(row=2, column=1) #放置在下左
        self.createWidgets()

class EncryptedPath(Frame): #密文路径选择区
    selectDpName = StringVar(value="") #路径变量
    pathOpened = False
    def getPath(self):
        return self.selectDpName.get()
    def choose_dp(self): #按钮函数
        global pathOpened
        if self.ePath.get() == "": #尝试获取用户输入的路径，无则提醒用户
            self.terminal.newNotice("请输入路径或浏览选择")
        else: #用户输入了路径，获取
            self.selectDpName.set(self.ePath.get())
            if pathOpened ^ self.pathOpened:
                self.terminal.newNotice("已选择加密保存路径:" + self.selectDpName.get())
            else:
                self.terminal.newNotice("已选择密文文件路径:" + self.selectDpName.get())
            self.photoBar.showPhoto(self.selectDpName.get())
            pathOpened = True
            self.pathOpened = True
    def choose_dp_browser(self):
        global pathOpened
        if pathOpened ^ self.pathOpened: #判断用户是否在明文区选择了明文图像或上次在本类中打开
            self.selectDpName.set(filedialog.asksaveasfilename(title="加密图像保存为",defaultextension = ".png",filetypes  = [("BMP File", ".bmp"),\
                                                                                                    ("PNG File", ".png"),\
                                                                                                    ("TIFF File",".tiff"),\
                                                                                                    ("All Files", ".*")]))
            self.terminal.newNotice("已选择加密保存路径:" + self.selectDpName.get())
        else:
            self.selectDpName.set(filedialog.askopenfilename(title="上传要解密的图像"))
            self.terminal.newNotice("已选择密文文件路径:" + self.selectDpName.get())
            self.photoBar.showPhoto(self.selectDpName.get())
            pathOpened = True
            self.pathOpened = True
    def createWidgets(self):
        self.ePath = Entry(self, width=40, textvariable=self.selectDpName) #左侧输入框，绑定路径变量
        self.ePath.pack(side="left")

        self.bBrowser = Button(self, width=5, height=1, text="浏览...", command=self.choose_dp_browser)
        self.bBrowser.pack(side="left")

        self.bGetPath = Button(self, width=6, height=1, text="选择文件", command=self.choose_dp) #右侧按钮
        self.bGetPath.pack(side="left")
    def __init__(self, master, terminal: Terminal, photoBar: EncryptedShowPhoto):
        Frame.__init__(self, master)
        self.terminal = terminal
        self.photoBar = photoBar
        self.grid(row=2, column=3) #放置在下右
        self.createWidgets()

class Utility(Frame): #button功能区
    varKey = StringVar(value="") #密钥变量
    def eKeyEncrypt(self): #加密按钮指令
        global pathOpened
        self.bEncrypt.config(command=DISABLED) #设置按钮不可用，防止二次加密
        key = self.eKey.get() #获得密钥
        im = self.mPhoto.im #获得明文图像
        DpPath = self.ePath.getPath() #获取密文路径
        self.terminal.newNotice("正在加密") #显示状态信息
        km.map(key) #映射产生加密参数
        im = Encrypt_f(km.getLamb(), km.getx0(),DpPath,im=im)
        self.ePhoto.showPhoto(im=im) #向密文图像显示投送密文Image
        self.bEncrypt.config(command=self.eKeyEncrypt)
        self.terminal.newNotice(notice="加密成功")
        pathOpened = False
        self.mPath.pathOpened = False
        self.ePath.pathOpened = False
    def eKeyDecrypt(self): #解密按钮指令
        global pathOpened
        self.bDecrypt.config(command=DISABLED) #设置按钮不可用，防止二次解密
        key = self.eKey.get() #获取密钥
        im = self.ePhoto.im #获得密文图像
        EpPath = self.mPath.getPath() #获得明文路径
        self.terminal.newNotice("正在解密") #显示状态信息
        km.map(key) #映射产生解密参数
        im = Decrypt_f(km.getLamb(), km.getx0(), EpPath, im=im)
        self.mPhoto.showPhoto(im=im)
        self.terminal.newNotice("解密成功")
        self.bDecrypt.config(command=self.eKeyDecrypt)
        pathOpened = False
        self.mPath.pathOpened = False
        self.ePath.pathOpened = False
    def createWidgets(self):
        self.lKey = Label(self, text="密钥") #显示“密钥”
        self.lKey.pack(side="top")
        
        self.eKey = Entry(self, width=30)
        self.eKey.pack(side="top") #密钥输入框

        self.bEncrypt = Button(self, text="加密", command=self.eKeyEncrypt) #加密按钮
        self.bEncrypt.pack(side="left")

        self.bDecrypt = Button(self, text="解密", command=self.eKeyDecrypt) #解密按钮
        self.bDecrypt.pack(side="right")
    def __init__(self, master, mPath: MessagePath, ePath: EncryptedPath, mPhoto: MessageShowPhoto, ePhoto: EncryptedShowPhoto, terminal: Terminal):
        Frame.__init__(self, master)
        self.mPath = mPath
        self.ePath = ePath
        self.mPhoto = mPhoto
        self.ePhoto = ePhoto
        self.terminal = terminal
        self.grid(row=1, column=2) #放置在上中
        self.createWidgets()

window.title("基于混沌算法的图像加解密")
mTerminal = Terminal(window)
mMessageShowPhoto = MessageShowPhoto(window, mTerminal)
mEncryptedShowPhoto = EncryptedShowPhoto(window, mTerminal)
mMessagePath = MessagePath(window, mTerminal, mMessageShowPhoto)
mEncryptedPath = EncryptedPath(window, mTerminal, mEncryptedShowPhoto)
mUtility = Utility(window, mMessagePath, mEncryptedPath, mMessageShowPhoto, mEncryptedShowPhoto, mTerminal)
window.mainloop()
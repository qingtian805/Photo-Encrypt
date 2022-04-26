# -*- coding: utf-8 -*-
from EnDecrypt import Decrypt_f, Encrypt_f
from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk, UnidentifiedImageError
from datetime import datetime
import KeyMapping as km

from numpy import select
#这是两个临时函数，用于替代加密核心算法
#def Encrypt_f(lamb, x0, opath, wpath): 
#    print("Encrypt")
#def Decrypt_f(lamb, x0, opath, wpath):
#    print("Decrypt")

window = Tk() #似乎需要先定义这个后面才能跑……
photoMessage = PhotoImage()
photoEncrypted = PhotoImage()

#两个列表，存储可以加密、解密的文件类型
MESSAGE_FILE_TYPES =  [("JPG File", ".jpg"),("BMP File", ".bmp"),("PNG File", ".png"),("TIFF File",".tiff"),("All Files", ".*")]
ENCRYPTED_FILE_TYPES = [("BMP File", ".bmp"),("PNG File", ".png"),("TIFF File",".tiff"),("All Files", ".*")]

class Terminal(Frame): #仿终端状态栏
    def newNotice(self, notice): #添加新消息
        self.textBar.config(state=NORMAL)
        self.textBar.insert("0.0", datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\n" + notice + "\n")
        self.textBar.config(state=DISABLED)

    def createWidgets(self):
        self.textBar = Text(self, state=DISABLED, width=40, height=5)
        self.textBar.pack()

    def __init__(self, master):
        Frame.__init__(self, master)
        self.grid(row=2, column=2) #放置在下中
        self.createWidgets()

class MessageShowPhoto(Frame): #明文图像显示区
    def showPhoto(self, im):#将图像显示图像
        global photoMessage
        width = im.size[0]
        height = im.size[1]
        if(width >= height):
            #若图像宽大于等于高
            ratio = height / width
            resizedIm = im.resize((384, int(384 * ratio)), Image.ANTIALIAS)
        else:
            #若图像高大于宽
            ratio = width / height
            resizedIm = im.resize((int(384 * ratio), 384), Image.ANTIALIAS)
        photoMessage = ImageTk.PhotoImage(resizedIm)#转换为TK可以显示的格式
        self.lPhoto.config(image=photoMessage, width=384, height=384)#设置TK以显示图像

    def clearPhoto(self): #清除图像
        self.lPhoto.destroy()
        self.lPhoto = Label(self, width=46, height=20)
        self.lPhoto.pack(side="top")

    def createWidgets(self):
        self.lText = Label(self, text="明文图像")
        self.lText.pack(side="bottom")

        self.lPhoto = Label(self, width=46, height=20)
        self.lPhoto.pack(side="top")

    def __init__(self, master, terminal: Terminal):
        Frame.__init__(self, master)
        self.terminal = terminal
        self.grid(row=1, column=1) #放置在上左
        self.createWidgets()

class EncryptedShowPhoto(Frame): #密文图像显示区
    def showPhoto(self, im):#将图像显示图像
        global photoEncrypted
        self.im = im
        width = self.im.size[0]
        height = self.im.size[1]
        if(width >= height):
            #若图像宽大于等于高
            ratio = height / width
            resizedIm = self.im.resize((384, int(384 * ratio)), Image.ANTIALIAS)
        else:
            #若图像高大于宽
            ratio = width / height
            resizedIm = self.im.resize((int(384 * ratio), 384), Image.ANTIALIAS)
        photoEncrypted = ImageTk.PhotoImage(resizedIm)#转换为TK可以显示的格式
        self.lPhoto.config(image=photoEncrypted, width=384, height=384)#设置TK以显示图像
        self.im.close()#关闭图像文件

    def clearPhoto(self): #清除图像
        self.lPhoto.destroy()
        self.lPhoto = Label(self, width=46, height=20)
        self.lPhoto.pack(side="top")

    def createWidgets(self):
        self.lText = Label(self, text="密文图像")
        self.lText.pack(side="bottom")

        self.lPhoto = Label(self, width=46, height=20)
        self.lPhoto.pack(side="top")

    def __init__(self, master, terminal: Terminal):
        Frame.__init__(self, master)
        self.terminal = terminal
        self.grid(row=1, column=3) #放置在上右
        self.createWidgets()

class MessagePath(Frame): #明文路径选择区
    selectEpName = StringVar(value="") #路径变量
    exist = False #用于指示路径是否准备就绪

    def getPath(self):
        return self.selectEpName.get()

    def lock(self):
        #将所有按钮设为不可用
        self.bOpen.config(state=DISABLED)
        self.bSave.config(state=DISABLED)

    def reset(self):
        #重置变量
        self.exist = False
        self.selectEpName.set("")
        #重置按钮状态
        self.bOpen.config(state=NORMAL)
        self.bSave.config(state=NORMAL)

    def choose_ep(self): #按钮函数
        path = self.ePath.get()#获取用户输入

        if path == '': #无路径，提示用户输入路径并返回
            self.terminal.newNotice("请选择明文路径")
            return
        
        #获取到了路径
        try:
            #尝试打开图像文件，如果成功则将图像传至显示后关闭fp
            im = Image.open(path)
            self.photoBar.showPhoto(im)
            im.close()
            #设置标识与反馈
            self.exist = True #设置文件存在标识
            self.terminal.newNotice("设置明文文件路径:" + path) #在终端显示提示

        #异常处理
        except FileNotFoundError:
            #若文件不存在，设置标识
            self.exist = False
            self.terminal.newNotice("设置明文文件路径:" + path)
        except UnidentifiedImageError:
            #文件类型错误，无法打开
            self.exist = False
            self.terminal.newNotice("未支持的图像类型")
        except:
            self.exist = False
            self.terminal.newNotice("未知错误，请检查程序权限以及文件路径")
        
    def choose_ep_open(self):
        #弹出对话窗让用户选择路径
        path = filedialog.askopenfilename(title="选择明文文件",defaultextension = ".png",filetypes  = MESSAGE_FILE_TYPES)
        #将文件名传入Entry
        self.selectEpName.set(path)
        #后续交由choose_ep()函数处理
        self.choose_ep()
    
    def choose_ep_save(self):
        #弹出对话窗让用户选择路径
        path = filedialog.asksaveasfilename(title="明文保存位置",defaultextension = ".png",filetypes  = MESSAGE_FILE_TYPES)
        #将文件名传入Entry
        self.selectEpName.set(path)
        #后续交由choose_ep()函数处理
        self.choose_ep()

    def createWidgets(self):
        self.ePath = Entry(self, width=40, textvariable=self.selectEpName, state="disable") #左侧输入框，绑定路径变量
        self.ePath.pack(side="left")

        self.bOpen = Button(self, width=5, height=1, text="打开...", command=self.choose_ep_open)
        self.bOpen.pack(side="left")

        self.bSave = Button(self, width=6, height=1, text="保存到...", command=self.choose_ep_save) #右侧按钮
        self.bSave.pack(side="left")

    def __init__(self, master, terminal: Terminal, photoBar: MessageShowPhoto):
        Frame.__init__(self, master)
        self.terminal = terminal
        self.photoBar = photoBar
        self.grid(row=2, column=1) #放置在下左
        self.createWidgets()

class EncryptedPath(Frame): #密文路径选择区
    selectDpName = StringVar(value="") #路径变量
    exist = False #用于指示路径是否已经准备就绪

    def getPath(self):
        return self.selectDpName.get()

    def lock(self):
        #将所有按钮设为不可用
        self.bOpen.config(state=DISABLED)
        self.bSave.config(state=DISABLED)
    
    def reset(self):
        #重置变量
        self.exist = False
        self.selectDpName.set("")
        #重置按钮状态
        self.bOpen.config(state=NORMAL)
        self.bSave.config(state=NORMAL)

    def choose_dp(self): #按钮函数
        path = self.ePath.get()#获取用户输入

        if path == '': #无路径，提示用户输入路径并返回
            self.terminal.newNotice("请选择密文路径")
            return
        
        #获得到路径
        try:
            #尝试打开图像文件，如果成功则将图像传至显示后关闭fp
            im = Image.open(path)
            self.photoBar.showPhoto(im)
            im.close()
            #设置标识与反馈
            self.exist = True
            self.terminal.newNotice("设置密文文件路径:" + path) #在终端显示提示

        #异常处理
        except FileNotFoundError:
            #若文件不存在，设置标识
            self.exist = False
            self.terminal.newNotice("设置密文文件路径:" + path)
        except UnidentifiedImageError:
            #文件类型错误，无法打开
            self.exist = False
            self.terminal.newNotice("未支持的图像类型")
        except:
            self.exist = False
            self.terminal.newNotice("未知错误，请检查程序权限以及文件路径")

    def choose_dp_open(self):
        #弹出对话窗让用户选择路径
        path = filedialog.askopenfilename(title="选择密文文件",defaultextension = ".png",filetypes  = ENCRYPTED_FILE_TYPES)
        #将文件名传入Entry
        self.selectDpName.set(path)
        #后续交由choose_ep()函数处理
        self.choose_dp()
    
    def choose_dp_save(self):
        #弹出对话窗让用户选择路径
        path = filedialog.asksaveasfilename(title="密文保存位置",defaultextension = ".png",filetypes  = ENCRYPTED_FILE_TYPES)
        #将文件名传入Entry
        self.selectDpName.set(path)
        #后续交由choose_ep()函数处理
        self.choose_dp()
    
    def createWidgets(self):
        self.ePath = Entry(self, width=40, textvariable=self.selectDpName, state="disable") #左侧输入框，绑定路径变量
        self.ePath.pack(side="left")

        self.bOpen = Button(self, width=5, height=1, text="打开...", command=self.choose_dp_open)
        self.bOpen.pack(side="left")

        self.bSave = Button(self, width=6, height=1, text="保存到...", command=self.choose_dp_save) #右侧按钮
        self.bSave.pack(side="left")
        
    def __init__(self, master, terminal: Terminal, photoBar: EncryptedShowPhoto):
        Frame.__init__(self, master)
        self.terminal = terminal
        self.photoBar = photoBar
        self.grid(row=2, column=3) #放置在下右
        self.createWidgets()

class Utility(Frame): #button功能区
    varKey = StringVar(value="") #密钥变量

    def lock(self):
        self.bDecrypt.config(state=DISABLED)
        self.bEncrypt.config(state=DISABLED)

    def reset(self):
        #重设按钮状态
        self.bDecrypt.config(state=NORMAL)
        self.bEncrypt.config(state=NORMAL)
        self.bReset.config(state=DISABLED)
        #将Key设置为空
        self.varKey.set("")
    
    def reset_all(self):
        self.reset()
        self.ePath.reset()
        self.mPath.reset()
        self.ePhoto.clearPhoto()
        self.mPhoto.clearPhoto()

    def eKeyEncrypt(self): #加密按钮指令
        key = self.eKey.get() #获得密钥
        MpPath = self.mPath.getPath() #获取明文路径
        EpPath = self.ePath.getPath() #获取密文路径

        #检查明文路径
        if not self.mPath.exist:
            self.terminal.newNotice("错误！请设置正确的明文路径")
            return
        #检查密文路径
        if len(EpPath) < 1 or EpPath.isspace():
            self.terminal.newNotice("错误！请设置正确的密文路径")
            return
        #检查密钥
        if len(key) < 1:
            self.terminal.newNotice("错误！请输入密钥")
            return

        #开始加密
        self.terminal.newNotice("正在加密...") #显示状态信息
        self.lock()
        self.mPath.lock()
        self.ePath.lock()
        self.master.update()#更新tkinter
        
        km.map(key) #映射产生加密参数
        Encrypt_f(km.getLamb(), km.getx0(), MpPath, EpPath)

        #尝试打开密文
        try:
            im = Image.open(EpPath)
            self.ePhoto.showPhoto(im) #向密文图像显示投送密文Image
            im.close()

            self.terminal.newNotice("加密成功")
        except:
            self.terminal.newNotice("未知错误，密文未能写入。请检查软件权限和密文路径")

        #开放reset
        self.bReset.config(state=NORMAL)

    def eKeyDecrypt(self): #解密按钮指令
        key = self.eKey.get() #获取密钥
        MpPath = self.mPath.getPath() #获得明文路径
        EpPath = self.ePath.getPath() #获得密文路径

        #检查密文路径
        if not self.ePath.exist:
            self.terminal.newNotice("错误！请设置正确的密文路径")
            return
        #检查明文路径
        if len(MpPath) < 1 or MpPath.isspace():
            self.terminal.newNotice("错误！请设置正确的明文路径")
            return
        #检查密钥
        if len(key) < 1:
            self.terminal.newNotice("错误！请输入密钥")
            return

        #开始解密
        self.terminal.newNotice("正在解密...") #显示状态信息
        self.lock()
        self.mPath.lock()
        self.ePath.lock()
        self.master.update()#更新tkinter

        km.map(key) #映射产生解密参数
        Decrypt_f(km.getLamb(), km.getx0(), EpPath, MpPath)

        try:
            im = Image.open(MpPath)
            self.mPhoto.showPhoto(im)
            im.close()
            
            self.terminal.newNotice("解密成功")
        except:
            self.terminal.newNotice("未知错误，明文未能写入。请检查软件权限和明文路径")

        #开放reset
        self.bReset.config(state=NORMAL)

    def createWidgets(self):
        self.lKey = Label(self, text="密钥") #显示“密钥”
        self.lKey.pack(side="top")
        
        self.eKey = Entry(self, width=30)
        self.eKey.pack(side="top") #密钥输入框

        self.bEncrypt = Button(self, text="加密", command=self.eKeyEncrypt) #加密按钮
        self.bEncrypt.pack(side="left")

        self.bDecrypt = Button(self, text="解密", command=self.eKeyDecrypt) #解密按钮
        self.bDecrypt.pack(side="right")
        
        self.bReset = Button(self, text="重置", command=self.reset_all, state=DISABLED) #重置按钮
        self.bReset.pack(side="bottom")

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
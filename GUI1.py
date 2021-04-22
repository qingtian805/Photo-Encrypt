# -*- coding: utf-8 -*-
from pathlib import WindowsPath
from tkinter import *
import tkinter.filedialog
# from EnDecrypt import Encrypt_f, Decrypt_f
from hashlib import md5

window = Tk()

#class Utility(Frame):  # button功能区
    #def createWidgets(self):

#def __init__(self, master=None):
        #Frame.__init__(self, master)
        #self.pack()
        #self.createWidgets()

class Path(Frame):  # 路径选择区
    def choose_ep(self):  # 选择加密图片
        selectepname = tkinter.filedialog.askopenfilename(title='上传加密图片')  # 上传加密图片
        self.e1.set(selectepname)

    def choose_dp(self):  #选择解密图片
        selectdpname = tkinter.filedialog.askopenfilename(title='上传解密图片')  #  上传解密图片
        self.e2.set(selectdpname)

    def createWidgets(self):  # 选择文件按钮及显示框
        self.e1 = tkinter.StringVar()
        self.e2 = tkinter.StringVar()
        self.e_entry1 = tkinter.Entry(window, width=40, textvariable=self.e1).place(x=30, y=550)
        self.up_button1 = tkinter.Button(window, width=10, height=1, text="上传加密图片", command=self.choose_ep).place(x=320, y=550)
        self.e_entry2 = tkinter.Entry(window, width=40, textvariable=self.e2).place(x=1000, y=550)
        self.up_button2 =tkinter.Button(window, width=10, height=1, text="上传解密图片", command=self.choose_dp).place(x=1290, y=550)

    def __init__(self, master=None):
        super().__init__().__init__(self, master)
        self.pack()
        self.createWidgets()

path = Path(window)

#class Terminal(Frame):  # 仿终端状态栏
    #def createWidgets(self):

#def __init__(self, master=None):
        #Frame.__init__(self, master)
        #self.pack()
        #self.createWidgets()


#class ShowPhoto(Frame):  # 图像显示区
    #def createWidgets(self):

#def __init__(self, master=None):
        #Frame.__init__(self, master)
        #self.pack()
        #self.createWidgets()

# 设置窗口居中
width = 1400
height = 700
screenwidth = window.winfo_screenwidth()
screenheight = window.winfo_screenheight()
chicun = '%dx%d+%d+%d' % (width, height, (screenwidth-width)/2, (screenheight-height)/2)
window.geometry(chicun)
window.mainloop()
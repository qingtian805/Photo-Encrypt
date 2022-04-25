from tkinter.constants import NONE
from PIL import Image
import numpy as np

def logistic_f(lamb, x): #logistic生成器，输入lambda和当前状态，返回下一个状态
    x = lamb * x * (1 - x)
    return x

def Encrypt_f(lamb: float, x0: float, opath: str, wpath: str): #加密主函数，opath打开图像路径，wpath保存图像路径，存储路径，lamb，x0是加密参数
    im = Image.open(opath) #初始化变量

    x1 = logistic_f(lamb, x0)
    r3 = int(x1 * 0xFFFFFFFF) % 0xFF
    x1 = logistic_f(lamb, x1)
    r2 = int(x1 * 0xFFFFFFFF) % 0xFF
    x1 = logistic_f(lamb, x1)
    r1 = int(x1 * 0xFFFFFFFF) % 0xFF

    im = np.array(im) #转化为数组格式
    width, length = im.shape[0], im.shape[1]
    try: #获得数组大小
        height = im.shape[2]
    except IndexError:
        height = 1
    
    if height == 1: #开始处理
        for i in range(width): #灰度图像模式
            for j in range(length):
                x1 = logistic_f(lamb, x1)
                r3 = r2
                r2 = r1
                r1 = int(x1 * 0xFFFFFFFF) % 0xFF
                im[i][j] = (r2 ^ (im[i][j] - r3 + 8) ^ r1) % 256
    else:
        for i in range(width): #彩色图像模式
            for j in range(length):
                for z in range(height):
                    x1 = logistic_f(lamb, x1)
                    r3 = r2
                    r2 = r1
                    r1 = int(x1 * 0xFFFFFFFF) % 0xFF
                    im[i][j][z] = (r2 ^ (im[i][j][z] - r3 + 8) ^ r1) % 256
    im = Image.fromarray(im)
    im.save(wpath, quality = 100)

def Decrypt_f(lamb: float, x0: float, opath: str, wpath: str): #解密主函数，opath打开图像路径，wpath保存图像路径，lamb，x0是加密参数
    im = Image.open(opath) #初始化变量

    x1 = logistic_f(lamb, x0)
    r3 = int(x1 * 0xFFFFFFFF) % 0xFF
    x1 = logistic_f(lamb, x1)
    r2 = int(x1 * 0xFFFFFFFF) % 0xFF
    x1 = logistic_f(lamb, x1)
    r1 = int(x1 * 0xFFFFFFFF) % 0xFF

    im = np.array(im) #转化为数组格式
    width, length = im.shape[0], im.shape[1]
    try: #获得数组大小
        height = im.shape[2]
    except IndexError:
        height = 1
    
    if height == 1: #开始处理
        for i in range(width): #灰度图像模式
            for j in range(length):
                x1 = logistic_f(lamb, x1)
                r3 = r2
                r2 = r1
                r1 = int(x1 * 0xFFFFFFFF) % 0xFF
                im[i][j] = ((r2 ^ im[i][j] ^ r1) + r3 - 8) % 256
    else:
        for i in range(width): #彩色图像模式
            for j in range(length):
                for z in range(height):
                    x1 = logistic_f(lamb, x1)
                    r3 = r2
                    r2 = r1
                    r1 = int(x1 * 0xFFFFFFFF) % 0xFF
                    im[i][j][z] = ((r2 ^ im[i][j][z] ^ r1) + r3 - 8) % 256
    im = Image.fromarray(im)
    im.save(wpath, quality = 100)
    

#def test_main() 下面是测试代码用的类，这个做标识符
#path = ("/home/kevin/git-photo-encryption/lena51.bmp", "/home/kevin/git-photo-encryption/lena.bmp")
#path = ("/home/kevin/git-photo-encryption/lenacolor.tiff", "/home/kevin/git-photo-encryption/lena.tiff")
#path = ("/home/kevin/git-photo-encryption/lena.bmp", "/home/kevin/git-photo-encryption/lenade.bmp")
#path = ("/home/kevin/git-photo-encryption/lena.tiff", "/home/kevin/git-photo-encryption/lenade.tiff")
#lamb1 = 3.75431
#lamb2 = 3.89775
#x1 = 0.6472
#x2 = 0.3854
#Encrypt_f(lamb2, x2, "/home/kevin/git-photo-encryption/lena51.bmp", "/home/kevin/git-photo-encryption/lenae.bmp")
#Decrypt_f(lamb2, x2, "/home/kevin/git-photo-encryption/lenae.bmp", "/home/kevin/git-photo-encryption/lenad.bmp")
#Encrypt_f(lamb1, x1, "/home/kevin/git-photo-encryption/lenacolor.tiff", "/home/kevin/git-photo-encryption/lenacolore2.tiff")
#Decrypt_f(lamb1, x1, "/home/kevin/git-photo-encryption/lenacolore2.tiff", "/home/kevin/git-photo-encryption/lenacolord.tiff")
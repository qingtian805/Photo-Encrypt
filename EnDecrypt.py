from pathlib import WindowsPath
from PIL import Image
import numpy as np

r1 = 0
lamb1 = 3.897
x = 0

def logistic_f(lamb, x): #logistic生成器，输入lambda和当前状态，返回下一个状态
    x = lamb * x * (1 - x)
    return x

def Encrypt_f(path, lamb, x0): #加解密主函数，path图像路径，存储路径，lamb，x0是加密参数
    global x,lamb1
    im = Image.open(path[0])
    x = x0
    lamb1 = lamb
    im = np.array(im)
    try:
        width, length, height = im.shape[0], im.shape[1], im.shape[2]
    except IndexError:
        height = 1
        width, length = im.shape[0], im.shape[1]
    
    if height == 1:
        for i in range(width):
            for j in range(length):
                x = logistic_f(lamb1, x)
                r1 = int(256 * x) % 256
                im[i][j] = ((im[i][j] ^ r1) - (height * 8)) % 256
    else:
        for i in range(width):
            for j in range(length):
                x = logistic_f(lamb1, x)
                r1 = int(256 * x) % 256
                for z in range(height):
                    im[i][j][z] = ((im[i][j] ^ r1) - (height * 8)) % 256
    im = Image.fromarray(im)
    im.save(path[1])

def Decrypt_f(path, lamb, x0): #解密主函数，path图像路径，lamb，x0是加密参数
    global x,lamb1
    Image.open(path)
    x = x0
    lamb1 = lamb
    

#def test_main() 下面是测试代码用的类，这个做标识符
path = ("/home/kevin/lena51.bmp", "/home/kevin/lena.bmp")
#path = ("/home/kevin/lenacolor.tiff", "/home/kevin/lena.tiff")
lamb2 = 3.897
x = 0.343
Encrypt_f(path, lamb2, x)
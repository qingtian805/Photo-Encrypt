from PIL import Image
import numpy as np

def logistic_f(lamb, x): #logistic生成器，输入lambda和当前状态，返回下一个状态
    x = lamb * x * (1 - x)
    return x

def Encrypt_f(path, lamb, x0): #加密主函数，path图像路径，存储路径，lamb，x0是加密参数
    im = Image.open(path[0]) #初始化变量
    x1 = x0
    lamb1 = lamb
    r1 = int(51200 * x1) % 256
    x1 = logistic_f(lamb1, x1)
    r2 = r1
    r1 = int(51200 * x1) % 256
    x1 = logistic_f(lamb1, x1)
    r3 = r2
    r2 = r1
    r1 = int(51200 * x1) % 256


    im = np.array(im) #转化为数组格式
    try: #获得数组大小
        width, length, height = im.shape[0], im.shape[1], im.shape[2]
    except IndexError:
        height = 1
        width, length = im.shape[0], im.shape[1]
    
    if height == 1: #开始处理
        for i in range(width): #灰度图像模式
            for j in range(length):
                x1 = logistic_f(lamb1, x1)
                r3 = r2
                r2 = r1
                r1 = int(51200 * x1) % 256
                im[i][j] = r2 ^ ((im[i][j] - r3 + 8) ^ r1) % 256
    else:
        for i in range(width): #彩色图像模式
            for j in range(length):
                x1 = logistic_f(lamb1, x1)
                r3 = r2
                r2 = r1
                r1 = int(51200 * x1) % 256
                for z in range(height):
                    im[i][j][z] = (r2 ^ (im[i][j][z] - r3 + 24) ^ r1) % 256
    im = Image.fromarray(im)
    im.save(path[1])

def Decrypt_f(path, lamb, x0): #解密主函数，path图像路径，lamb，x0是加密参数
    global x,lamb1
    Image.open(path)
    x = x0
    lamb1 = lamb
    

#def test_main() 下面是测试代码用的类，这个做标识符
#path = ("/home/kevin/lena51.bmp", "/home/kevin/lena.bmp")
#path = ("/home/kevin/lenacolor.tiff", "/home/kevin/lena.tiff")
#lamb2 = 3.89775
#x = 0.3854
#Encrypt_f(path, lamb2, x)
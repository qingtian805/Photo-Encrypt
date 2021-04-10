from PIL import Image
import numpy as np
import logistic as log

#设置三个生成器的参数,lamb>3.569945673
x = [0.343, 0.564, 0.9766]
lamb = [3.897, 3.694, 3.572]

def generator1():
    global x, lamb
    return int(256 * log.logistic_f(lamb, x, 0)) % 256
def generator2():
    global x, lamb
    return int(256 * log.logistic_f(lamb, x, 1)) % 256
def generator3():
    global x, lamb
    return int(256 * log.logistic_f(lamb, x, 2)) % 256

im = Image.open("/home/kevin/lena51.bmp")#读取文件与信息
width = im.width
height = im.height
#mode = im.mode 这个是L，8×1

im = np.array(im)#转换格式为数组
for i in range(width):
    for j in range(height):
        r1 = generator1()
        r2 = generator2()
        r3 = generator3()
        im[i][j] = ((r1 ^ im[i][j] ^ r2) + 8 - r3) % 256

print(im)
im = Image.fromarray(im)
#
# im.show()
im.save("/home/kevin/lena.bmp")

#logistic.py
logistic_lamb = 3.7
logistic_x = 0.5
def logistic_set(lamb, seed): #logistic 设置函数，并检测lambda与初值的合理性
    global logistic_lamb , logistic_x
    if (lamb < 3.569945673) | (lamb > 4.0):
        print("Error! Illegal lambda!")
        return 0
    if (seed < 0) | (seed > 1.0):
        print("Error! illegal seed!")
        return 0
    logistic_lamb = lamb
    logistic_x = seed

def logistic_f(): #logistic 运行函数，产生序列中的下一个值并返回
    global logistic_lamb , logistic_x
    logistic_x = logistic_lamb * logistic_x * (1 - logistic_x)
    return logistic_x
def logistic_f(lamb, x, No): #临时增加的函数，以允许使用多个logistic生成器,No为生成器序号，参数需要由主程序定义
    x[No] = lamb[No] * x[No] * (1 - x[No])
    return x[No]
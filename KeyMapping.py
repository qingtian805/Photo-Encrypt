from zlib import crc32

decline = 0xFFFFFFFF
lamb = 0
x0 = 0

def map(strKey: str):
    global lamb, x0
    crc = crc32(strKey.encode())
    x0 = crc/decline
    lamb = 3.57 + 0.43 * x0

def getLamb():
    return lamb
def getx0():
    return x0
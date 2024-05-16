from Crypto.Cipher import AES
from Crypto.Util.number import *
from Crypto.Util.Padding import pad

from mpmath import mp
from os import urandom

import json
import random

FLAG = b'crypto{????????????????????????}'

mp.dps = 200

# y^2 = x^3 - x
def lift_x(x):
    return mp.sqrt(x**3 - x)

def double(pt):
    x, y = pt
    m = (3*x*x - 1)/(2 * y)
    xf = m*m - 2*x
    yf = -(y + m*(xf - x))
    return (xf, yf)

def add(pt1, pt2):
    x1, y1 = pt1
    x2, y2 = pt2
    m = (y1 - y2)/(x1 - x2)
    xf = m*m - x1 - x2
    yf = -(y1 + m*(xf - x1))
    return (xf, yf)

def scalar_multiply(pt, m):
    if m == 1:
        return pt
    half_mult = scalar_multiply(pt, m // 2)
    ans = double(half_mult)
    if m % 2 == 1:
        ans = add(ans, pt)
    return ans

key = urandom(16)
iv = urandom(16)
cipher = AES.new(key, AES.MODE_CBC, iv)
plaintext = pad(FLAG, 16)
ciphertext = cipher.encrypt(plaintext)

N = bytes_to_long(key)

gx = mp.mpf(1 + random.random())
gy = lift_x(gx)
G = (gx, gy)
P = scalar_multiply(G, N)

json.dump({
    'gx': str(G[0]),
    'gy': str(G[1]),
    'px': str(P[0]),
    'py': str(P[1]),
    'ciphertext': ciphertext.hex(),
    'iv': iv.hex()
}, open('output.txt', 'w'))


# "gx": "1.15939524880832589559531697886995971202850341796875", 
#  "gy": "0.63171256444643032392780992695525219049591162225190317013257297329770648576821328127894482837966831464341245854394869021441094534520252153121771214144624262228503025100001998247467928012492847829951495", 
#  "px": "1052.1869486109503324827555468817188804055933729601321435932864694301534931492427433020783168479195188024409373571681097603398390379320742186401833284576176214641603772370675124838606986281131453644941",
#  "py": "34130.226434169760878074808301335090475271836563983186858174748793301185920507814323732035620490086239117019147179225251544229354849757884152095399018744815803126126630119173317092410331587882005521149", 
#  "ciphertext": "a104b68d30a207eabf293324fbde64f8d628fb07068058c1e76e670e7e805fc567f739185bbe6cbb44f09013173ee653",
#  "iv": "485f9a1e4a3b19348367280df13f9e77"
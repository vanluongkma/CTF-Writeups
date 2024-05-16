from sage.all import*
from pwn import *
from json import *
from Crypto.Util.number import *
from fastecdsa.point import Point

# secp256r1 parameters https://neuromancer.sk/std/secg/secp256r1
p = 0xffffffff00000001000000000000000000000000ffffffffffffffffffffffff
a = 0xffffffff00000001000000000000000000000000fffffffffffffffffffffffc
b = 0x5ac635d8aa3a93e7b3ebbd55769886bc651d06b0cc53b0f63bce3c3e27d2604b
F = GF(p)
E = EllipticCurve(F, [a, b])
a = E.order()
G = E(0x6B17D1F2E12C4247F8BCE6E563A440F277037D812DEB33A0F4A13945D898C296,
                    0x4FE342E2FE1A7F9B8EE7EB4A7C0F9E162BCE33576B315ECECBB6406837BF51F5)
public = E(0x3B827FF5E8EA151E6E51F8D0ABF08D90F571914A595891F9998A5BD49DFA3531, 0xAB61705C502CA0F7AA127DEC096B2BBDC9BD3B4281808B3740C320810888592A)

print(public * (a + 1) == public)

print(E.order())
g = Point(0x3B827FF5E8EA151E6E51F8D0ABF08D90F571914A595891F9998A5BD49DFA3531, 0xAB61705C502CA0F7AA127DEC096B2BBDC9BD3B4281808B3740C320810888592A)
# d = inverse(public[0], a)
# print(d)
# def sign_point(g, d):
#     return g * d

# print(sign_point(G, d))
f = connect("socket.cryptohack.org", 13382, level = 'debug')
# f = process(["python3", "13382.py"])

f.recvline()
a = ({
    "private_key": 115792089210356248762697446949407573529996955224135760342422259061068512044370,
    "host": "www.bing.com",
    "curve": "secp256r1",
    "generator": [0x3B827FF5E8EA151E6E51F8D0ABF08D90F571914A595891F9998A5BD49DFA3531, 0xAB61705C502CA0F7AA127DEC096B2BBDC9BD3B4281808B3740C320810888592A]

})


f.sendline(dumps(a))
f.recvline()
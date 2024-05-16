from sage.all import *
from hashlib import sha256
from Crypto.Util.number import *
from output import p, poly

flag = b"ngungungu"
flag_int = bytes_to_long(flag)
flag_hash = bytes_to_long(sha256(flag).digest())
print(flag_int)
print(flag_hash)

p = getPrime(40)
print(p)
P = PolynomialRing(GF(p), name="x")
x = P.gen()
poly = (P.random_element(10) ** 2) * (x - flag_int) * (x - flag_hash)
print(p)
print(list(poly))
print(x-flag_hash)
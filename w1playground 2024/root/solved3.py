from sage.all import *
from hashlib import sha256
from Crypto.Util.number import *
from output import p, poly

solutions = []
i = 0

P = PolynomialRing(GF(p), name="x")
f = P(poly)
root = f.roots()
print(root)
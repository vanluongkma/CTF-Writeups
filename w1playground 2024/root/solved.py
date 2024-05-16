from sage.all import *
from hashlib import sha256
from Crypto.Util.number import *
from keys_and_messages_701dba5b1a84cb168547ec18227a7740.keys_and_messages.out import p, poly


P = PolynomialRing(GF(p), name="x")
poly = P(poly)
root = poly.roots()
print(root)
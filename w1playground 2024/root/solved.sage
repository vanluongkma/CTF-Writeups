from sage.all import *
from Crypto.Util.number import *
from output import p, poly

P = PolynomialRing(GF(p), name="x")
f = P(poly)
f.roots()

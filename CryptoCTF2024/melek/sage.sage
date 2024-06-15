from Crypto.Util.number import long_to_bytes
from output import enc

e, p, PT = enc
F = GF(p)
R = F['x']
poly = R.lagrange_polynomial(PT)
ct = poly.coefficients()[0]
m = int((ct^(Zmod(p - 1)(e // 2)^-1)).sqrt())

print(long_to_bytes(m))
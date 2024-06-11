from hashlib import sha1
from Crypto.Util.number import *
from ecdsa import ellipticcurve
from ecdsa.ecdsa import curve_256, generator_256, Public_key, Private_key
from random import randint
from sage.all import *
from output import SIGs, P, flag

G = generator_256
q = 115792089210356248762697446949407573529996955224135760342422259061068512044369
a = -3
b = curve_256.b()
p = curve_256.p()

E = EllipticCurve(GF(p), [a, b])
G = E(int(G.x()), int(G.y()))
B = 2 ** (256 - 96)

Mtilde = [B, 0]
Rtilde = [0, B / q]

for sig in SIGs:
    m, r, s = sig['msg'].encode(), int(sig['r'], 16), int(sig['s'], 16)

    m = int(sha1(m).hexdigest(), 16)

    Mtilde += [m * inverse(s, q) % q]
    Rtilde += [r * inverse(s, q) % q]

Mtilde = matrix(QQ, 1, len(Mtilde), Mtilde)
Rtilde = matrix(QQ, 1, len(Rtilde), Rtilde)

Pdiag = -q * identity_matrix(QQ, len(SIGs))


Z = matrix(QQ, len(SIGs), 2, [0 for i in range(len(SIGs)*2)] )

M = block_matrix([[Z, Pdiag]])
M = block_matrix([[Mtilde], [Rtilde], [M]])

P = E(int(P[0]), int(P[1]))
flag = E(int(flag[0]), int(flag[1]))
L = M.LLL()

found = 0

for row in L.rows():
	if found:
		break
	for i in range(len(SIGs)):
		if found:
			break
		m, r, s = sig['msg'].encode(), int(sig['r'], 16), int(sig['s'], 16)
		m = int(sha1(m).hexdigest(), 16)
		solk = row[i + 2]
		if solk == 0: 
			continue
		for k in [solk, -solk]:
			d = inverse(r, q) * (int(k) * s - m) % q
			if int(d) * G == P:
				print("Private key found!", d)
				flag = flag * int(inverse(int(d), q))
				print(long_to_bytes(int(flag[0])))
				found = 1
				break
from hashlib import sha1
from Crypto.Util.number import *
from ecdsa import ellipticcurve
from ecdsa.ecdsa import curve_256, generator_256, Public_key, Private_key
from random import randint
from sage.all import *


SIGs = [
    {'msg': 'I have hidden the secret flag as a point of an elliptic curve using my private key.', 'r': '0x91f66ac7557233b41b3044ab9daf0ad891a8ffcaf99820c3cd8a44fc709ed3ae', 's': '0x1dd0a378454692eb4ad68c86732404af3e73c6bf23a8ecc5449500fcab05208d'},
    {'msg': 'The discrete logarithm problem is very hard to solve, so it will remain a secret forever.', 'r': '0xe8875e56b79956d446d24f06604b7705905edac466d5469f815547dea7a3171c', 's': '0x582ecf967e0e3acf5e3853dbe65a84ba59c3ec8a43951bcff08c64cb614023f8'},
    {'msg': 'Good luck!', 'r': '0x566ce1db407edae4f32a20defc381f7efb63f712493c3106cf8e85f464351ca6', 's': '0x9e4304a36d2c83ef94e19a60fb98f659fa874bfb999712ceb58382e2ccda26ba'}
]

G = generator_256
q = 115792089210356248762697446949407573529996955224135760342422259061068512044369
a = -3
b = curve_256.b()
p = curve_256.p()

E = EllipticCurve(GF(p), [a, b])
G = E(int(G.x()), int(G.y()))
B = 2 ** (256 - 96)

# We construct the first two rows of the lattice
Mtilde = [B, 0]
Rtilde = [0, B / q]

for sig in SIGs:
    m, r, s = sig['msg'].encode(), int(sig['r'], 16), int(sig['s'], 16)

    m = int(sha1(m).hexdigest(), 16)

    Mtilde += [m * inverse(s, q) % q]
    Rtilde += [r * inverse(s, q) % q]

Mtilde = matrix(QQ, 1, len(Mtilde), Mtilde)
Rtilde = matrix(QQ, 1, len(Rtilde), Rtilde)

Pdiag = -q * identity_matrix(QQ, len(SIGs));

# We construct the lower left n x 2 zero block matrix
Z = matrix(QQ, len(SIGs), 2, [0 for i in range(len(SIGs)*2)] )

# We construct the final matrix assembling all blocks
M = block_matrix([[Z, Pdiag]])
M = block_matrix([[Mtilde], [Rtilde], [M]])

P = (48780765048182146279105449292746800142985733726316629478905429239240156048277, 74172919609718191102228451394074168154654001177799772446328904575002795731796)
flag = (16807196250009982482930925323199249441776811719221084165690521045921016398804, 72892323560996016030675756815328265928288098939353836408589138718802282948311)

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
		# we skip the first two vector components we used to improve LLL
		solk = row[i + 2]
		if solk == 0: 
			continue
		# LLL might have swapped the sign of found short vectors
		for k in [solk, -solk]:
			d = inverse(r, q) * (int(k) * s - m) % q
			if int(d) * G == P:
				print("Private key found!", d)
				flag = flag * int(inverse(int(d), q))
				print(long_to_bytes(int(flag[0])))
				found = 1
				break
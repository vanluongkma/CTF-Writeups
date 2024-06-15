from sage.all import *
from typing import Tuple
from  hashlib import sha256
from Crypto.Cipher import AES
from Crypto.Util.number import *
from Crypto.Util.Padding import pad
from Crypto.Random import get_random_bytes
import re
from pwn import *
from tqdm import *
p = 0x01ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff
K = GF(p)
a = K(0x01fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffc)
b = K(0x0051953eb9618e1c9a1f929a21a0b68540eea2da725b99b315f3b8b489918ef109e156193951ec7e937b1652c0bd3bb1bf073573df883d2c34f1ef451fd46b503f00)
E = EllipticCurve(K, (a, b))
G = E(0x00c6858e06b70404e9cd9e3ecb662395b4429c648139053fb521f828af606b4d3dbaa14b5e77efe75928fe1dc127a2ffa8de3348b3c1856a429bf97e7e31c2e5bd66, 0x011839296a789a3bc0045c8a5fb42c7d1bd998f54449579b446817afbd17273e662c97ee72995ef42640c550b9013fad0761353c7086a272c24088be94769fd16650)
E.set_order(0x01fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffa51868783bf2f966b7fcc0148f709a5d03bb5c9b8899c47aebb6fb71e91386409 * 0x1)
n = G.order()
q = n
arr = []
B = 2 ** (q.nbits()-8)
def digest(msg) -> int:
    if isinstance(msg, str):
        msg = msg.encode()
    return int.from_bytes(sha256(msg).digest(), byteorder='big')
io = process(["python3", "main.py"])
io.recvuntil(b">> ")
io.sendline(b'!2')
for i in tqdm(range(100)):
    io.recvuntil(b">> ")
    msg = str(i)
    io.sendline(msg.encode())
    io.recvuntil(b"Signature (r,s): ")
    res = io.recvline().decode().strip().replace("(","").replace(")","").split(", ")
    r = int(res[0])
    s = int(res[1])
    arr.append({
        'msg': msg,
        'r': str(r),
        's': str(s)
    })
io.sendline(b"!exit")
io.recvuntil(b">> ")
io.sendline(b'!4')
io.recvuntil(b"Encrypted Flag: ")
res = bytes.fromhex(io.recvline().decode().strip())
iv = res[:16]
ct = res[16:]
print(iv,ct)


Mtilde = [B, 0]
Rtilde = [0, B / q]

for sig in arr:
    m, r, s = sig['msg'].encode(), int(sig['r']), int(sig['s'])

    m = digest(m)
    print(m)
    Mtilde += [m * inverse(s, q) % q]
    Rtilde += [r * inverse(s, q) % q]

Mtilde = matrix(QQ, 1, len(Mtilde), Mtilde)
Rtilde = matrix(QQ, 1, len(Rtilde), Rtilde)

Pdiag = -q * identity_matrix(QQ, len(arr));

Z = matrix(QQ, len(arr), 2, [0 for i in range(len(arr)*2)] )

# We construct the final matrix assembling all blocks
M = block_matrix([[Z, Pdiag]])
M = block_matrix([[Mtilde], [Rtilde], [M]])

L = M.LLL()

found = 0
for row in L.rows():
    if found:
        break
    for i in range(len(arr)):
        if found:
            break
        
        m, r, s = sig['msg'].encode(), int(sig['r']), int(sig['s'])

        m = digest(m)
        solk = row[i + 2]
        if solk == 0: 
            continue
        for k in [solk, -solk]:
            d = inverse(r, q) * (int(k) * s - m) % q
            AES_KEY = sha256(long_to_bytes(int(d))).digest()
            cipher = AES.new(AES_KEY, AES.MODE_CBC, iv)
            flag = cipher.decrypt(ct)
            if b'L3AK{' in flag:
                print(flag)
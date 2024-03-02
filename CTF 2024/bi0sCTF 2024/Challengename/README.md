## Challengename
```python3
from ecdsa.ecdsa import Public_key, Private_key
from ecdsa import ellipticcurve
from hashlib import md5
import random
import os
import json

flag = open("flag", "rb").read()[:-1]

magic = os.urandom(16)

p = 0xffffffff00000001000000000000000000000000ffffffffffffffffffffffff
a = ###REDACTED###
b = ###REDACTED###
G = ###REDACTED###

q = G.order()

def bigsur(a,b):
    a,b = [[a,b],[b,a]][len(a) < len(b)]
    return bytes([i ^ j for i,j in zip(a,bytes([int(bin(int(b.hex(),16))[2:].zfill(len(f'{int(a.hex(), 16):b}'))[:len(a) - len(b)] + bin(int(b.hex(),16))[2:].zfill(len(bin(int(a.hex(), 16))[2:]))[:len(bin(int(a.hex(), 16))[2:]) - len(bin(int(b.hex(), 16))[2:])][i:i+8], 2) for i in range(0,len(bin(int(a.hex(), 16))[2:]) - len(bin(int(b.hex(), 16))[2:]),8)]) + b)])

def bytes_to_long(s):
    return int.from_bytes(s, 'big')

def genkeys():
    d = random.randint(1,q-1)
    pubkey = Public_key(G, d*G)
    return pubkey, Private_key(pubkey, d)

def sign(msg,nonce,privkey):
    hsh = md5(msg).digest()
    nunce = md5(bigsur(nonce,magic)).digest()
    sig = privkey.sign(bytes_to_long(hsh), bytes_to_long(nunce))
    return json.dumps({"msg": msg.hex(), "r": hex(sig.r), "s": hex(sig.s)})

def enc(privkey):
    x = int(flag.hex(),16)
    y = pow((x**3 + a*x + b) % p, (p+3)//4, p)
    F = ellipticcurve.Point('--REDACTED--', x, y)
    Q = F * privkey.secret_multiplier
    return (int(Q.x()), int(Q.y()))

pubkey, privkey = genkeys()
print("Public key:",(int(pubkey.point.x()),int(pubkey.point.y())))
print("Encrypted flag:",enc(privkey))

# Public key: (99122053878685444817852582103585646482441799670468212049632161370423019963573, 49681263796445807694244738028189208770171168855624587289690892802435841601423)
# Encrypted flag: (22455982735997721923198309515515820680837002550923840212531066823876108860098, 49955453626898315794129063911602706078234097783588068635922441060010795905908)

nonces = set()

for _ in '01':
    try:
        msg = bytes.fromhex(input("Message: "))
        nonce = bytes.fromhex(input("Nonce: "))
        if nonce in nonces:
            print("Nonce already used")
            continue
        nonces.add(nonce)
        print(sign(msg,nonce,privkey))
    except ValueError:
        print("No hex?")
        exit()
```
 - Chall này tôi nhận được 2 điểm từ đường cong: Public key là **dG** và Encrypt flag là **dF**
 - Từ 2 điểm trên ta có $$y_1^2 = x_1^3 + ax_1 + b$$ $$y_2^2 = x_2^3 + ax_2 + b$$ $$(y_1^2 - y_2^2) - (x_1^3 - x_2^3) = a(x_1-x_2)$$
 - Ta có a, b được tính bằng
```sage
sage: p = 0xffffffff00000001000000000000000000000000ffffffffffffffffffffffff
....: x1=99122053878685444817852582103585646482441799670468212049632161370423019963573
....: y1=49681263796445807694244738028189208770171168855624587289690892802435841601423
....: x2=22455982735997721923198309515515820680837002550923840212531066823876108860098
....: y2=49955453626898315794129063911602706078234097783588068635922441060010795905908
....:
....: a=Mod(((y1^2 - y2^2)-(x1^3 - x2^3))*inverse_mod((x1-x2),p),p)
....: b=Mod(y2^2 - x2^3 - a*x2, p)
sage: a, b
(115792089210356248762697446949407573530086143415290314195533631308867097853948,
 41058363725152142129326129780047268409114441015993725554835256314039467401291)
sage:
```
 - Ta có curve của bài
```sage
sage: p = 0xffffffff00000001000000000000000000000000ffffffffffffffffffffffff
....: a = 115792089210356248762697446949407573530086143415290314195533631308867097853948
....: b =  41058363725152142129326129780047268409114441015993725554835256314039467401291
....: E = EllipticCurve(GF(p), [a, b])
....: E.order()
115792089210356248762697446949407573529996955224135760342422259061068512044369
sage:
```
 - Ở đây hàm **bigsur** trông rất dài nhưng thực chất nó là phép xor. Nếu chúng ta chọ **nonce1 = b"\x00"** và **nonce2 = b"\x00\x00"** thì sẽ có thể lấy cùng một **nunce** trong hàm **sign()** mà server ký message
 - Để tìm lại private key **d** tôi sử dụng [️ECDSA Nonce Reuse Attack](https://crypto.stackexchange.com/questions/71764/is-it-safe-to-reuse-a-ecdsa-nonce-for-two-signatures-if-the-public-keys-are-diff)
 - Chúng ta có **r1 = r2 = R**, **(r1, s1)** là chữ ký của $m_1$, **(r2, s2)** là chữ ký của $m_2$ khi đó chúng ta có $$s_1 * k - H(m_1) = s_2 * H(m_2) = R * privatekey$$ $$k = \frac{s_1 - s_2}{(H(m_1) - H(m_2)}$$ $$privatekey = \frac{s_1 * k - H(m_1)}{R}$$
 - Khi có **privatekey** ta dễ dàng tìm lại **F** bằng phép tính $F = private^-1 * Q$
 - Solution bằng sage
```python3
from hashlib import md5
from Crypto.Util.number import *
from sage.all import *

def inverse_mod(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('Modular inverse does not exist')
    else:
        return x % m

def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

def recover_private_key(H_m1, H_m2, r, s1, s2, q):
    Hm1 = bytes_to_long(md5(H_m1).digest())
    Hm2 = bytes_to_long(md5(H_m2).digest())
    r_inv = inverse_mod(r, q)
    d = ((inverse_mod(s1 - s2, q) * (Hm1 * s2 - Hm2 * s1) % q) * r_inv) % q
    return d

x1=99122053878685444817852582103585646482441799670468212049632161370423019963573
y1=49681263796445807694244738028189208770171168855624587289690892802435841601423
x2=22455982735997721923198309515515820680837002550923840212531066823876108860098
y2=49955453626898315794129063911602706078234097783588068635922441060010795905908
p = 0xffffffff00000001000000000000000000000000ffffffffffffffffffffffff
a = 115792089210356248762697446949407573530086143415290314195533631308867097853948
b = 41058363725152142129326129780047268409114441015993725554835256314039467401291
E = EllipticCurve(GF(p), [a, b])
G = E(x1, y1)
n = int(E.order())

H_m1 = b"Fidethus"
H_m2 = b"Cylabus"

r = 0x39504995bcf174284cc4013aaae44454d349629d864c4b41456f8ecd1143c4b0  
s1 = 0xa6c917eb8ff4d2b8e5424c6c01ac6e1b2c67bb48a362c3fcb9cde05d252836c3 
s2 = 0x5c012f1f87731cec692375afdb56b6b38b80f935ab9d9d29cf531d528fed7703 
q = int(E.order())


d = recover_private_key(H_m1, H_m2, r, s1, s2, q)
print(d)

d_inverse=inverse_mod(d,n)
Q = E(22455982735997721923198309515515820680837002550923840212531066823876108860098, 49955453626898315794129063911602706078234097783588068635922441060010795905908)
F = d_inverse*Q
print(int(F[0]))
```
> FLAG : bi0sctf{https://bit.ly/3I0zwtG}
